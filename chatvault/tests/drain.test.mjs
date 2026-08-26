import { test } from "node:test";
import assert from "node:assert/strict";
import { ingestPaste, exportVault } from "../js/engine.mjs";
import {
  classifyFilename,
  conversationsFromExport,
  ingestChatGptExport,
  ingestDaAudit,
  ingestMediaStub,
  ingestNamedSource,
  looksLikeChatGptExport,
  looksLikeDaAudit,
  pullDaDrain,
} from "../js/drain.mjs";

function chatgptConversation(title, user, assistant) {
  return {
    title,
    create_time: 1_700_000_000,
    current_node: "n3",
    mapping: {
      n1: {
        id: "n1",
        parent: null,
        children: ["n2"],
        message: { author: { role: "system" }, content: { parts: ["sys"] } },
      },
      n2: {
        id: "n2",
        parent: "n1",
        children: ["n3"],
        message: { author: { role: "user" }, content: { parts: [user] } },
      },
      n3: {
        id: "n3",
        parent: "n2",
        children: [],
        message: { author: { role: "assistant" }, content: { parts: [assistant] } },
      },
    },
  };
}

test("classifyFilename maps pictures, movies, audio, pdf, and text", () => {
  assert.equal(classifyFilename("shot.png"), "picture");
  assert.equal(classifyFilename("clip.MP4"), "movie");
  assert.equal(classifyFilename("voice.wav"), "audio");
  assert.equal(classifyFilename("paper.PDF"), "pdf");
  assert.equal(classifyFilename("notes.md"), "text");
  assert.equal(classifyFilename("unknown.bin"), "other");
});

test("ChatGPT conversations.json walker keeps origin as AI", () => {
  const conv = chatgptConversation(
    "Token bucket",
    "How do I design a rate limiter?",
    "Use a token bucket and a refill interval."
  );
  assert.equal(looksLikeChatGptExport(conv), true);
  assert.equal(looksLikeChatGptExport([conv]), true);
  assert.equal(looksLikeChatGptExport({ conversations: [conv] }), true);
  assert.equal(conversationsFromExport({ conversations: [conv] }).length, 1);

  const { entries, errors, kind } = ingestChatGptExport({ conversations: [conv] });
  assert.equal(kind, "chatgpt");
  assert.equal(errors.length, 0);
  assert.equal(entries.length, 1);
  assert.equal(entries[0].origin_class, "ai_generated");
  assert.equal(entries[0].source_ai, "ChatGPT");
  assert.equal(entries[0].source_type, "transcript");
  assert.match(entries[0].raw_content, /token bucket/i);
  assert.match(entries[0].raw_content, /rate limiter/i);
  assert.equal(
    entries[0].key_claims.every((c) => c.status !== "PROVED"),
    true
  );
});

test("DA audit JSON drains as a human FRA record, never a proof", () => {
  const audit = {
    input_expression: "∇²Φ = 4π G ρ",
    canonical_sfe_status: "unresolved",
    highest_evidence_label: "representation",
    narrative: "Poisson gravity is represented. This is not a derivation and not a proof.",
  };
  assert.equal(looksLikeDaAudit(audit), true);
  const { entries, kind } = ingestDaAudit(audit);
  assert.equal(kind, "da_audit");
  assert.equal(entries.length, 1);
  assert.equal(entries[0].origin_class, "human_record");
  assert.equal(entries[0].source_type, "da_audit");
  assert.equal(entries[0].source_ai, "DomainArchitect");
  assert.match(entries[0].summary, /Not a proof/i);
  assert.equal(entries[0].key_claims.length, 0);
  assert.equal(entries[0].theorems.length, 0);

  const bundle = {
    format: "chatvault-export",
    schema_version: "chatvault-engine-0.3.0",
    source: "domain-architect",
    entries: entries,
  };
  assert.equal(looksLikeDaAudit(bundle), true);
  const wrapped = ingestDaAudit(bundle);
  assert.equal(wrapped.kind, "bundle");
  assert.equal(wrapped.entries[0].origin_class, "human_record");
});

test("media stubs are human_record and movies stay metadata-only", () => {
  const movie = ingestMediaStub({
    filename: "lab.mp4",
    mime: "video/mp4",
    size: 50_000_000,
  });
  assert.equal(movie.kind, "media");
  assert.equal(movie.entries[0].origin_class, "human_record");
  assert.equal(movie.entries[0].source_type, "movie");
  assert.equal(movie.entries[0].source_ai, "human");
  assert.equal(movie.entries[0].file_url, "");
  assert.match(movie.entries[0].raw_content, /metadata-only/);

  const pic = ingestNamedSource("photo.png", {
    mime: "image/png",
    size: 1200,
    dataUrl: "data:image/png;base64,aaa",
  });
  assert.equal(pic.entries[0].origin_class, "human_record");
  assert.equal(pic.entries[0].source_type, "picture");
  assert.match(pic.entries[0].file_url, /^data:image\/png/);
});

test("ingestNamedSource infers origin for ChatGPT JSON, DA JSON, and letters", () => {
  const conv = chatgptConversation("Limiter", "hello", "token bucket reply");
  const chatgpt = ingestNamedSource("conversations.json", {
    text: JSON.stringify([conv]),
    mime: "application/json",
  });
  assert.equal(chatgpt.kind, "chatgpt");
  assert.equal(chatgpt.entries[0].origin_class, "ai_generated");

  const da = ingestNamedSource("audit.json", {
    text: JSON.stringify({
      input_expression: "x=y",
      canonical_sfe_status: "unresolved",
      narrative: "identity only",
    }),
    mime: "application/json",
  });
  assert.equal(da.entries[0].origin_class, "human_record");
  assert.equal(da.entries[0].source_type, "da_audit");

  const letter = ingestNamedSource("note.md", {
    text: "TITLE: Paper note\nSOURCE_TYPE: paper\n\nHandwritten margin note.",
  });
  assert.equal(letter.entries[0].origin_class, "human_record");
  assert.equal(letter.entries[0].source_type, "paper");
});

test("pullDaDrain imports a chatvault-export from loopback", async () => {
  const local = ingestPaste("TITLE: Drain probe\nSOURCE_AI: DomainArchitect\nSOURCE_TYPE: da_audit\n\nFRA note.");
  const payload = exportVault([local]);
  payload.source = "domain-architect";
  const fetchImpl = async (url) => {
    assert.match(url, /127\.0\.0\.1:7847\/queue|localhost:7847\/queue/);
    return { ok: true, json: async () => payload };
  };
  const result = await pullDaDrain(fetchImpl);
  assert.equal(result.entries.length, 1);
  assert.equal(result.entries[0].origin_class, "human_record");
  assert.equal(result.count, 1);
});
