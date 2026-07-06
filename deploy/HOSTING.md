# Hosting the Stingray demo

The demo is fully static (one HTML file + `livewx.js`), so any static host works. Three options, by effort:

## 1. Netlify Drop — 2 minutes, no repo
Go to https://app.netlify.com/drop and drag the `prototype/` folder in. You get a shareable URL immediately (free account keeps it permanent; you can set a custom subdomain like `stingray-demo.netlify.app`). Weather stays whatever `livewx.js` contained at upload — re-run `ingest/fetch_weather.py` and re-drop to refresh.

## 2. GitHub Pages + auto-refreshing live weather — recommended
1. Create a GitHub repo and push the Stingray folder.
2. Copy `prototype/deploy/github-pages.yml` to `.github/workflows/deploy.yml`.
3. Repo Settings → Pages → Source: **GitHub Actions**.

The workflow deploys on every push **and every 6 hours re-runs the weather fetcher**, so the online demo's "Live" scenario always shows the current Med forecast — the full ingestion pipeline running unattended, which is a nice demo point in itself. URL: `https://<user>.github.io/<repo>/stingray_planner.html`.

Note: free GitHub Pages sites are public. Private Pages requires GitHub Enterprise.

## 3. Cloudflare Pages + Access — if you need a password
Same static deploy via Cloudflare Pages, then put Cloudflare Access (free tier) in front to restrict by email — appropriate once you're showing investors/partners under NDA.

## Caveats for a public URL
- The footer already states data is synthetic and not for navigation — keep it.
- `livewx.js` at the repo root of `prototype/` is required next to the HTML file.
- If the demo will carry real branding publicly, consider registering it under a subdomain of stingraymarinetechnology.com (e.g. `demo.stingraymarinetechnology.com` — both Netlify and Cloudflare support custom domains on free tiers; add a CNAME in your Wix DNS settings).
