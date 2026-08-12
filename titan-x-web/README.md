# TITAN-X site

Live file to send: `TITAN-X-FINAL-Investor-Plan.pdf`

## Auto-deploy (GitHub → Vercel)

Do this **once** in the browser (this agent cannot log into Vercel for you):

1. Open https://vercel.com/new
2. Import **simons357/Ship_it_app**
3. Leave Root Directory as the repo root (`vercel.json` already serves `titan-x-web/`)
4. Set Production Branch to `main` (or this working branch until you merge)
5. Deploy

After that, every GitHub push that changes the PDF or site updates Vercel automatically. No manual upload.

## Replit → GitHub → Vercel

Field Lock and NAV-42 are mirrored from `*.replit.app` into `titan-x-web/apps/`.

**Already running in this repo:** GitHub Action `Sync Replit apps to GitHub` copies the live Replit frontends twice a day (and on manual run). That commit then deploys to Vercel once the import above is done.

**Optional, for real source (not just the published frontend):** in each Replit, Git panel → Connect to GitHub → push to `simons357/Ship_it_app`. Same Vercel import then deploys those commits too.
