# Old papers — lookup, upload, and what I already pulled

**For:** Jonathan Simons  
**Date:** 25 August 2026

You looked them up. The chat uploader failed. That is on this channel, not on you. Nothing from that batch reached this VM.

What actually landed in chat earlier: Paper2 TeX, Paper2 June PDF, and the Overleaf audit. That is all.

---

## How to send a file so it actually arrives

Do **not** attach the whole Desktop pack, a zip of many papers, or a folder. That is the usual way this chat errors.

**Working methods (pick one):**

1. **One small `.tex` per message.** Caption with the book name (`GCD Paper1`, `anesthesia`, `PAPER_A`). Send the next file after I confirm it filed.
2. **Paste the TeX** into the message if it is under ~100 KB.
3. **Public Zenodo** — I can fetch those myself. You do not need to re-upload them.

If the paperclip errors again: paste the **exact error text**, or put the file in the git repo on your Mac (`docs/papers/…`) and push. I can read git. I cannot read a failed attachment.

---

## What I pulled from Zenodo so you do not have to re-upload

| Book | File in git | Public DOI |
|---|---|---|
| Q6 / inverse-GCD (current) | `docs/papers/gcd/04_q6_inverse_gcd.pdf` | [10.5281/zenodo.22050962](https://doi.org/10.5281/zenodo.22050962) |
| Ring + SND (current) | `docs/papers/ring/02_ring_lemma_snd_conditional.pdf` | [10.5281/zenodo.22050976](https://doi.org/10.5281/zenodo.22050976) |
| Stack errata | `docs/papers/status-errata/06_status_errata.pdf` | [10.5281/zenodo.22045484](https://doi.org/10.5281/zenodo.22045484) |
| May swirl PDF | `docs/papers/swirl/zenodo-may/PhiRenorm_TrackB.pdf` | [10.5281/zenodo.20405405](https://doi.org/10.5281/zenodo.20405405) |
| May swirl short TeX | `docs/papers/swirl/zenodo-may/Simons_PhiRenorm_Axisymmetric.tex` | [10.5281/zenodo.20405597](https://doi.org/10.5281/zenodo.20405597) |
| Paper2 August TeX | `docs/papers/ns-snd/` | (from you, in chat) |
| Paper2 June FIXED PDF | `docs/papers/ns-snd/Paper2_NS_Regularity_SND_FIXED.pdf` | (from you; SHA `7de9444d…`) |
| Paper2 Mac “SND 2” PDF | `docs/papers/ns-snd/Paper2_NS_Regularity_SND.pdf` | (from you; not the Zenodo bytes) |
| Paper2 Zenodo “implies” | `docs/papers/ns-snd/zenodo-20272545/` | [10.5281/zenodo.20272545](https://doi.org/10.5281/zenodo.20272545) — **claim withdrawn** |
| Paper2 August 1 audit | `docs/papers/ns-snd/NS_PAPER2_CONDITIONAL_AUDIT_AUG1_2026.md` | (from you) |
| Swirl 22 August | `docs/papers/swirl/Simons_PhiRenorm_Swirl_2026-08-22.tex` | (already on this branch) |

Ring SND in that PDF is \(\inf J/X\ge c_*\). Paper2 SND is closeness of a GCD mix to \(\mu\). Same letters, two definitions.

The June Paper2 PDF cites `10.5281/zenodo.19842060` as GCD Paper1. Live Zenodo at that DOI is a **superseded Ring/SND** paper, not that title. `10.5281/zenodo.19842061` currently resolves to an unrelated record. Do not hunt those two as Paper1.

Withdrawn GCD prize paper (history only): [10.5281/zenodo.20271457](https://doi.org/10.5281/zenodo.20271457).

---

## Still useful from your Mac (only if different from the PDFs above)

Send **one** of these, as `.tex`, if you still want the pack source rather than the Zenodo PDF:

| What | Pack name |
|---|---|
| GCD Paper1 updated source | `GCD_Spectral_Paper1_UPDATED_2026-08-14.tex` |
| PAPER_A inverse-GCD source | `PAPER_A_Inverse_GCD_CORRECTED.tex` |
| PAPER_B Möbius \(Q_6\) source | `PAPER_B_Mobius_GCD_Q6.tex` |
| Ring June 19 source | `c8a03f315_RingLemma_Simons_June19_2026.tex` | **still not in this VM** under that pack name. |
| RingLemma_Final TeX | `492e0654f_RingLemma_Final.tex` | **filed** as [`docs/papers/ring/RingLemma_Final.tex`](../papers/ring/RingLemma_Final.tex). April 2026 *Borromean Triads* face; June 20-ish drop. **Not** a compile of the 21 Aug Zenodo PDF. **Not** FIXED.tex. **Not** Clay. Map: [`docs/papers/ring/FACES.md`](../papers/ring/FACES.md). |
| June Paper2 **source** of the FIXED PDF | `Paper2_NS_Regularity_SND_FIXED.tex` | **still not in this VM.** A message that is only the filename is not an attachment. Send the `.tex` as one file, or paste it, or git-push it. Caption: “this is the source of the June FIXED PDF.” Do not merge it with the August TeX. |
| June 14 Clay-submit (historical / withdrawn-claim only) | `2f30e8c4f_NS_ClaySubmit_Jonathan_Simons_2026-06-14.tex` | **still not in this VM.** Selecting a Mac path is not an attachment. Send this **one** `.tex` file. Do not zip. Caption: “June 14 ClaySubmit, historical face.” **Not** FIXED. **Not** August. Classical regularity stays **NOT CLAIMED** even if that draft claimed Clay. |
| Anesthesia face | `PAPER1_REBUILT_Coherence_Index.md` |
| Pack swirl complete (older than 22 August) | `NS_PhiRenorm_complete.tex` | **filed** as [`docs/papers/swirl/NS_PhiRenorm_complete.tex`](../papers/swirl/NS_PhiRenorm_complete.tex). April 2026 *Conditional Reduction*. Older than 22 August. **Not** a compile of the 22 August TeX. Same title family as [`Simons_PhiRenorm_Swirl_2026-06-30.pdf`](../papers/swirl/Simons_PhiRenorm_Swirl_2026-06-30.pdf). |

If the 21 August Zenodo PDFs **are** those pack faces, skip the hunt. Caption the drop: “this is newer than the 21 August Zenodo PDF” or “this is the same.”

Also filed from the later six-file drop (still older than 22 August, **not** a compile of that TeX): `Simons_PhiRenorm_Swirl_2026-06-30.pdf`, `PhiRenorm_FINAL_v2.tex`. Map: [`docs/papers/swirl/FACES.md`](../papers/swirl/FACES.md).

---

## Do not send

April `CLAY_FINAL`, `SERPENT_FINAL`, `WHAT_I_FOUND`, unconditional `simons_ns_overleaf` mains, zips of the whole pack, SFE/HB/QStack dumps.

Shahmurov: cite only. I can fetch arXiv if needed. You do not upload him.
