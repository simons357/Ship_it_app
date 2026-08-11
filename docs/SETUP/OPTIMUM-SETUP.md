# Optimum setup — Cursor + GitHub (for Jonathan)

## Why Cursor feels weird

| ChatGPT / Grok | Cursor |
| --- | --- |
| Conversation in the cloud | Opens **one folder** of real files |
| Remembers chat (sort of) | Sees only what’s in that folder |
| No “repo” | Works with **GitHub** (your free file cabinet) |

**“Goes to GitHub automatically”:**  
- **Cloud Agents** (what you’ve been using) can save to GitHub for you.  
- **Desktop Cursor** needs: Open Folder → work → commit → push.  
- Other AI apps often keep stuff in *their* cloud — not your GitHub. That’s why nothing shows up “automatically” unless you (or an agent) put it there.

**“Tons of code”:** You’re often inside `Ship_it_app`, which is software. Document projects (AquaQuartz, Anesthesia) should live in quieter folders/repos — mostly PDFs and notes, not app code.

---

## Optimum layout — one idea, one home

| GitHub repo | What’s in it | Cursor: Open Folder |
| --- | --- | --- |
| **`Ship_it_app`** | Software app only (long term) | When building the app |
| **`AquaQuartz`** | Water brand, brochures, venues *(split later)* | When working AquaQuartz |
| **`Simons-Anesthesia`** | Papers, teaching, Vigilant Patch, CV | When working anesthesia |
| **`PrimeField`** *(optional)* | LLC, trademarks, contracts | Company admin only |

**Rule:** Don’t put AquaQuartz and Anesthesia and app code all in one pile forever.

---

## How you work each day

1. Decide: *Today I’m on Anesthesia* (or AquaQuartz, or Ship It).  
2. Cursor → **File → Open Folder** → that project’s folder.  
3. Brainstorm anywhere → paste keepers into that folder’s `docs/` or `drafts/`.  
4. When something is ready to email → **PDF** into `outreach/`.  
5. **Commit + push** (save to GitHub).

One open folder = one project. Switch projects = Open Folder again.

---

## This week

| # | Do this |
| --- | --- |
| 1 | Send AquaQuartz PDF (already done file). |
| 2 | Use **`docs/anesthesia/`** (created for you below) — drop papers/CV there. |
| 3 | When ready: GitHub → New repo **`Simons-Anesthesia`** (private) → copy `docs/anesthesia/` into it → Open Folder that repo forever after. |
| 4 | Later: same for **`AquaQuartz`** (copy `docs/aquaquarts/`). |

---

## Where things are **right now** (inside Ship_it_app)

```
Ship_it_app/
  docs/
    SETUP/           ← this playbook
    aquaquarts/      ← AquaQuartz (PDF to send is here)
    anesthesia/      ← Anesthesia home (NEW — use this)
```

That’s orderly enough to work. Splitting into separate GitHub repos is the upgrade after you’re sending PDFs, not before.
