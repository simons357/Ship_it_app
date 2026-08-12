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

Live GitHub copy of the site (this branch):  
https://github.com/simons357/Ship_it_app/tree/cursor/titan-x-business-plan-7465/titan-x-web

Apps folder:  
https://github.com/simons357/Ship_it_app/tree/cursor/titan-x-business-plan-7465/titan-x-web/apps

## Base44.app + Replit + public sites → GitHub → Vercel

Live `*.base44.app`, `*.replit.app`, and `solenne.ai` frontends are mirrored into `titan-x-web/apps/`.

**Already running:** GitHub Action `Sync Base44 and Replit apps to GitHub` copies them twice a day (and on manual run). Those commits deploy to Vercel after the import above.

**Claude.ai:** artifacts are not public unless you hit Publish and get a `claude.ai/public/artifacts/…` URL. Kyrana is already on GitHub (`simons357/kyrana-oracle`). Other Claude-built apps cannot be copied from the Claude account itself.

**Optional, for editable Base44 source:** in each Base44 app, GitHub icon → connect to `simons357/Ship_it_app`. Same for Replit: Git panel → Connect to GitHub.
