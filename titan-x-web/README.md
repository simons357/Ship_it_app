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
