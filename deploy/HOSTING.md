# Hosting the Stingray demo

The demo UI is fully static (one HTML file), so any static host works for
*it* — but ticket B2 made the demo a real client of the `api/` planner
service, so it needs a running planner instance to actually compute plans.
Two things to stand up, not one:

## Part 1 — the planner API

Run `api/` (ticket B1) somewhere reachable from wherever you host the UI —
a small cloud VM is enough (see `docs/plans/ticket-B1.md`/`deploy/README.md`
for the install/service setup). Two settings the deployed demo specifically
depends on:

- **`STINGRAY_CORS_ORIGINS`** — must include the exact origin the UI is
  served from (e.g. `https://<user>.github.io`), or the browser's CORS
  preflight rejects every request. Defaults to `http://localhost:8080`
  (local dev only) if unset.
- **Mixed content (HTTPS required once the UI is deployed):** GitHub
  Pages (and most static hosts) serve over HTTPS. Browsers silently block
  an HTTPS page from fetching a plain-HTTP resource ("mixed content") —
  no error banner, requests just never fire. So once you deploy the UI
  publicly, the API must also be reachable over HTTPS (e.g. behind Caddy
  with an automatic cert, per `deploy/README.md`'s cloud-role setup), and
  `stingray_planner.html`'s `API_BASE` constant (top of the `id="shared"`
  script block) must be updated from the `http://localhost:8000` dev
  default to that HTTPS URL before/at deploy time.

## Part 2 — the demo UI static host

Three options, by effort:

### 1. Netlify Drop — 2 minutes, no repo
Go to https://app.netlify.com/drop and drag the `prototype/` folder in. You get a shareable URL immediately (free account keeps it permanent; you can set a custom subdomain like `stingray-demo.netlify.app`).

### 2. GitHub Pages — recommended
1. Create a GitHub repo and push the Stingray folder.
2. Copy `prototype/deploy/github-pages.yml` to `.github/workflows/deploy.yml`.
3. Repo Settings → Pages → Source: **GitHub Actions**.

The workflow deploys on every push. URL: `https://<user>.github.io/<repo>/stingray_planner.html`.

Note: free GitHub Pages sites are public. Private Pages requires GitHub Enterprise.

### 3. Cloudflare Pages + Access — if you need a password
Same static deploy via Cloudflare Pages, then put Cloudflare Access (free tier) in front to restrict by email — appropriate once you're showing investors/partners under NDA.

## Caveats for a public URL
- The footer already states chart/geography data is synthetic and not for navigation — keep it.
- Update `API_BASE`/`STINGRAY_CORS_ORIGINS` together (Part 1) — a mismatch is the most likely cause of "the demo loads but never shows a plan."
- The shared demo credential (`API_AUTH` in `stingray_planner.html`) is a deliberate, scoped exception to normal secret-handling — GitHub Pages has no secret-injection mechanism and the demo data is synthetic/non-sensitive. Rotate it (both here and in the API's configured credentials) if it leaks or the demo goes fully public.
- If the demo will carry real branding publicly, consider registering it under a subdomain of stingraymarinetechnology.com (e.g. `demo.stingraymarinetechnology.com` — both Netlify and Cloudflare support custom domains on free tiers; add a CNAME in your Wix DNS settings).
