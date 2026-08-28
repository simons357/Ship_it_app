/**
 * Copy this file + `chatvault/js/search.mjs` into another product.
 * Missing fields are empty. This is a local ranker over *your* corpus,
 * not a web crawler and not the ChatVault PWA.
 */
import { searchVault, SEARCH_ENGINE_VERSION } from "../../chatvault/js/search.mjs";

const records = [
  {
    id: "note-1",
    title: "Euler identity as a definitional fact",
    content_text: "e^{iπ} + 1 = 0",
    raw_content: "e^{iπ} + 1 = 0",
    search_tags: ["euler"],
  },
  {
    id: "note-2",
    title: "Weekly lab logistics",
    content_text: "Someone mentioned Euler while booking the seminar room.",
    raw_content: "",
    search_tags: ["ops"],
  },
];

const { engine, hits } = searchVault(records, "euler identity");
if (engine !== "chatvault-hybrid-0.2.0") throw new Error(engine);
if (hits[0]?.entry.id !== "note-1") throw new Error("title hit should rank first");

console.log(SEARCH_ENGINE_VERSION);
for (const h of hits) {
  console.log(`${h.score.toFixed(2)}\t${h.entry.id}\t${h.entry.title}`);
}
