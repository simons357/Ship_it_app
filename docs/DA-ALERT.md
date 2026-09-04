# Alerts (plain language + what to do)

`python3 scripts/da_machine.py alert`

When something **significant** flips, DA writes a note you
can read, and a one-line text. It also says what to do next.

A new catalog page is not a text. A flip on a watched claim
is.

---

## What gets a text

| Watch | In plain words |
|---|---|
| Track B as a whole | the hard fluid equations, no extra damping |
| B4b | does Hardy eat the nasty tube term? |
| B5b | does the extra \(1/r^2\) piece beat the tube source? |
| classical regularity | are those equations always smooth? |
| Track A checker | the easier, damped equations |
| full GCD floor | the dead prime-matrix slogan |
| \(F\) | a public formula for the measured numbers |
| destination | spectrum, not a bag of numbers |

If one of those goes pass → fail, fail → pass, or open →
something else, you get:

1. **TEXT** — one or two sentences
2. **WHAT IT MEANS** — no specialist chops required
3. **WHAT TO DO** — one next move
4. **DO NOT** — the usual misread (ToE, the other tracks)

---

## How it reaches you

The briefing is always written:

- `results/DA-ALERT.txt` — the words
- `results/da_alert.json` — the same, typed

A **phone** text needs a sender you attach. Set

```bash
export DA_ALERT_WEBHOOK="https://your-sms-or-chat-bridge"
```

DA will POST `{sms, plain, next}` only when `significant`
is true. No phone number lives in this repo. Do not commit
one.

Until that hook is set, the file *is* the text. When you
run `trackb`, `check`, `pipe`, `ground`, or `alert`, the
machine updates the watch list.

The first run is a **baseline**. It does not pretend a
discovery happened.

---

## What is not a text

New vocabulary pages. A daily arXiv title. Re-running
`desk`. Cosmo saying 16/16. A pairing of famous names.

Those can sit in the log. They do not wake you.
