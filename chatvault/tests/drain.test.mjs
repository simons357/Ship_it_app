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
  ingestNoticeForResults,
  looksLikeChatGptExport,
  looksLikeDaAudit,
  loadInboxFromRepo,
  postInboxExport,
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

test("ingestNamedSource files audio, video, pdf, image, and text as human records", () => {
  const wav = ingestNamedSource("voice.wav", { mime: "audio/wav", size: 64 });
  assert.equal(wav.kind, "media");
  assert.equal(wav.entries[0].origin_class, "human_record");
  assert.equal(wav.entries[0].source_type, "audio");
  assert.equal(wav.entries[0].source_ai, "human");
  assert.equal(wav.entries[0].file_url, "");
  assert.match(wav.entries[0].raw_content, /metadata-only/);
  assert.match(wav.entries[0].summary, /CLI --ingest-chatvault/);
  assert.equal(wav.entries[0].raw_content.includes("\u0000"), false);

  const mp4 = ingestNamedSource("clip.mp4", { mime: "video/mp4", size: 2048 });
  assert.equal(mp4.entries[0].origin_class, "human_record");
  assert.equal(mp4.entries[0].source_type, "movie");

  const pdf = ingestNamedSource("paper.pdf", { mime: "application/pdf", size: 512 });
  assert.equal(pdf.entries[0].origin_class, "human_record");
  assert.equal(pdf.entries[0].source_type, "pdf");

  const pic = ingestNamedSource("scan.png", {
    mime: "image/png",
    size: 40,
    dataUrl: "data:image/png;base64,iVBORw0KGgo=",
  });
  assert.equal(pic.entries[0].origin_class, "human_record");
  assert.equal(pic.entries[0].source_type, "picture");
  assert.match(pic.entries[0].file_url, /^data:image\/png/);

  const letter = ingestNamedSource("field-note.txt", { text: "Dear colleague, the recording is on the bench." });
  assert.equal(letter.entries[0].origin_class, "human_record");
  assert.equal(letter.entries[0].source_type, "letter");
  assert.match(letter.entries[0].raw_content, /recording is on the bench/);

  assert.equal(looksLikeChatGptExport({ mime: "audio/wav" }), false);
  const notice = ingestNoticeForResults([wav, mp4], { fileCount: 2 });
  assert.match(notice, /Indexed 2/);
  assert.match(notice, /binary not stored in the browser vault/);
});

test("a wav is never treated as a ChatGPT conversation dump", () => {
  const riff = "RIFF....WAVEfmt ";
  const wav = ingestNamedSource("conversations.wav", { mime: "audio/wav", size: riff.length, text: riff });
  assert.equal(wav.kind, "media");
  assert.equal(wav.entries[0].source_type, "audio");
  assert.equal(wav.entries[0].origin_class, "human_record");
  assert.equal(wav.entries[0].source_ai, "human");
});

test("loadInboxFromRepo merges chatvault-export sidecars", async () => {
  const stub = ingestNamedSource("lab.wav", { mime: "audio/wav", size: 32 }).entries[0];
  const bundle = exportVault([stub]);
  const fetchImpl = async (url) => {
    if (url === "/api/inbox") {
      return {
        ok: true,
        json: async () => ({ format: "chatvault-inbox-index", files: [{ name: "lab.json", url: "/chatvault/inbox/lab.json" }] }),
      };
    }
    if (url === "/chatvault/inbox/lab.json") {
      return { ok: true, json: async () => bundle };
    }
    return { ok: false, status: 404, json: async () => ({}) };
  };
  const loaded = await loadInboxFromRepo(fetchImpl);
  assert.equal(loaded.entries.length, 1);
  assert.equal(loaded.entries[0].origin_class, "human_record");
  assert.equal(loaded.entries[0].source_type, "audio");
});

test("postInboxExport posts JSON only", async () => {
  const entry = ingestNamedSource("clip.mp4", { mime: "video/mp4", size: 99 }).entries[0];
  const fetchImpl = async (url, opts) => {
    assert.equal(url, "/api/inbox");
    assert.equal(opts.method, "POST");
    const body = JSON.parse(opts.body);
    assert.equal(body.format, "chatvault-export");
    assert.equal(body.entries[0].source_type, "movie");
    return { ok: true, json: async () => ({ ok: true, count: 1, written: ["x.json"] }) };
  };
  const posted = await postInboxExport(exportVault([entry]), fetchImpl);
  assert.equal(posted.count, 1);
});
