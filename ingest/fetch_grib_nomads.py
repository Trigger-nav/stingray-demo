#!/usr/bin/env python3
"""
Stingray ingestion layer — raw GRIB2 pull from NOAA NOMADS (production path).

Downloads GFS-Wave GRIB2 subsets (significant wave height, primary wave
direction) plus GFS 10m wind for the western Med corridor, directly from
NOAA's NOMADS grib-filter endpoint. No API key required. This is the
production-shaped path: onboard, these files are the input to the
bias-correction stage (architecture §6); bandwidth-optimised by variable,
level, and bounding-box subsetting at the server.

Parsing GRIB2 requires eccodes/cfgrib (pip install cfgrib, needs the
eccodes binary). The demo pipeline (fetch_weather.py) avoids that
dependency; this script demonstrates acquisition only.

Usage:  python3 fetch_grib_nomads.py [output_dir]
Stdlib only for the download itself.
"""
import urllib.request, urllib.parse, datetime, os, sys

BBOX = dict(leftlon=6, rightlon=11, toplat=44.5, bottomlat=40.5)
FCST_HOURS = range(0, 31, 3)   # f000..f030 3-hourly

def latest_cycle(now=None):
    """Most recent GFS cycle likely to be fully published (~5h latency)."""
    now = now or datetime.datetime.utcnow()
    ref = now - datetime.timedelta(hours=5)
    cyc = (ref.hour // 6) * 6
    return ref.strftime("%Y%m%d"), f"{cyc:02d}"

def fetch(url, dest):
    req = urllib.request.Request(url, headers={"User-Agent": "stingray-prototype/0.1"})
    with urllib.request.urlopen(req, timeout=120) as r, open(dest, "wb") as f:
        f.write(r.read())
    return os.path.getsize(dest)

def main(outdir="grib_data"):
    os.makedirs(outdir, exist_ok=True)
    date, cyc = latest_cycle()
    print(f"GFS cycle {date}/{cyc}z, {len(list(FCST_HOURS))} forecast steps")
    for fh in FCST_HOURS:
        # --- GFS-Wave: Hs + primary wave direction ---
        wave_q = urllib.parse.urlencode({
            "file": f"gfswave.t{cyc}z.global.0p16.f{fh:03d}.grib2",
            "lev_surface": "on", "var_HTSGW": "on", "var_DIRPW": "on",
            "subregion": "", **BBOX, "dir": f"/gfs.{date}/{cyc}/wave/gridded"})
        # --- GFS: 10m wind ---
        wind_q = urllib.parse.urlencode({
            "file": f"gfs.t{cyc}z.pgrb2.0p25.f{fh:03d}",
            "lev_10_m_above_ground": "on", "var_UGRD": "on", "var_VGRD": "on",
            "subregion": "", **BBOX, "dir": f"/gfs.{date}/{cyc}/atmos"})
        for name, q in [(f"wave_f{fh:03d}.grib2", wave_q), (f"wind_f{fh:03d}.grib2", wind_q)]:
            base = ("https://nomads.ncep.noaa.gov/cgi-bin/filter_gfswave.pl" if name.startswith("wave")
                    else "https://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_0p25.pl")
            dest = os.path.join(outdir, name)
            try:
                kb = fetch(f"{base}?{q}", dest) // 1024
                print(f"  {name}: {kb} KB")
            except Exception as e:
                print(f"  {name}: FAILED ({e})")
    print("Done. Parse with cfgrib/eccodes; feed to bias-correction stage.")

if __name__ == "__main__":
    main(*sys.argv[1:])
