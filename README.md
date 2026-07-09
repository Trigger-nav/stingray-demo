# Stingray — Passage & Performance Optimisation (demo)

Interactive prototype for [Stingray Marine Technology](https://www.stingraymarinetechnology.com): multi-objective passage and vessel-setup optimisation for superyachts. Chart/geography data is synthetic; vessel, routing and weather now come from a real Stingray planner API (ticket B2) — **not for navigation**; recommendations are advisory only.

**[Open the demo](stingray_planner.html)** — requires a running `api/` planner instance; the page won't compute plans without one (see `deploy/HOSTING.md`).

- `stingray_planner.html` — the demo UI (fully static, no build step; the planner "brain" is a real API, not client-side)
- `ingest/fetch_grib_nomads.py` — production-path raw GRIB2 acquisition from NOAA NOMADS (reference artefact for `api/`'s cloud role — not invoked by this demo or its deploy workflow)
- `deploy/HOSTING.md` — hosting notes

© Stingray Marine Technology 2026
