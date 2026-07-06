# Stingray — Passage & Performance Optimisation (demo)

Interactive prototype for [Stingray Marine Technology](https://www.stingraymarinetechnology.com): multi-objective passage and vessel-setup optimisation for superyachts. All vessel, chart and routing data are **synthetic — not for navigation**; recommendations are advisory only.

**[Open the demo](stingray_planner.html)**

- `stingray_planner.html` — the demo (fully static, works offline)
- `livewx.js` — weather field for the "Live" scenario; regenerated every 6 hours by the deploy workflow via `ingest/fetch_weather.py` (Open-Meteo, ECMWF/NOAA models)
- `ingest/fetch_grib_nomads.py` — production-path raw GRIB2 acquisition from NOAA NOMADS
- `deploy/HOSTING.md` — hosting notes

© Stingray Marine Technology 2026
