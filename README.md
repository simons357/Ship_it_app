# Jonathan Simons — Intro Portfolio

Presentation-ready portfolio for intros and partner meetings.

**Spine:** I manage complexity.  
**Rooms:** Art · Prime Field Technologies · Patents · Apps.

## Preview locally

```bash
python3 -m http.server 8080
```

Open http://localhost:8080

## What’s here

| Path | Purpose |
| --- | --- |
| `index.html` | Intro site (hero → intro path → four rooms → contact) |
| `PRESENTATION.md` | Speaking notes for the room |
| `partner-packet/` | Deep vault: inventory, intros, brochures, briefs |
| `styles.css` / `script.js` | Site chrome |

## Make this its own GitHub repo (recommended)

This branch currently lives on `Ship_it_app` for convenience. Portfolio should stand alone.

```bash
# 1) On GitHub: create an empty public repo, e.g. simons357/simons-portfolio
# 2) Then:
git clone https://github.com/simons357/Ship_it_app.git
cd Ship_it_app
git checkout cursor/intro-portfolio-e279
git remote add portfolio https://github.com/simons357/simons-portfolio.git
git push portfolio cursor/intro-portfolio-e279:main
```

Enable **GitHub Pages** on that repo (main / root).

## Suggestions

1. Keep Ship it as a product repo; keep this as the intro glass.
2. One ask per meeting.
3. Three live links max in an intro.
4. Art early — same spine, visible.
5. Math and claims stay black-boxed until NDA / fit is clear.

## Contact

js@primefieldtechnologies.com · https://primefield.tech/
