#!/usr/bin/env python3
"""Turn raw source files into the compact data files the calculator bundles.

Usage: prepare_data.py <ourairports airports.csv> <natural-earth land.geojson> <rates-source.json>

Airports: OurAirports (public domain). Land outlines: Natural Earth 1:110m (public domain).
Earning rates: Alaska Airlines' published Atmos Rewards charts (sources listed in rates.json).
"""
import csv, json, sys, pathlib

DATA = pathlib.Path(__file__).resolve().parent.parent / "data"
RANK = {"large_airport": 0, "medium_airport": 1, "small_airport": 2, "seaplane_base": 3}


def airports(path):
    best = {}
    for r in csv.DictReader(open(path, encoding="utf-8")):
        code = r["iata_code"].strip().upper()
        if len(code) != 3 or r["type"] not in RANK:
            continue
        prev = best.get(code)
        if prev and RANK[prev["type"]] <= RANK[r["type"]]:
            continue
        best[code] = r
    lines = []
    for code, r in sorted(best.items()):
        clean = lambda s: s.replace("|", "/").replace("\n", " ").strip()
        lines.append("|".join([
            code, clean(r["name"]), clean(r["municipality"]), r["iso_country"],
            f'{float(r["latitude_deg"]):.4f}'.rstrip("0").rstrip("."),
            f'{float(r["longitude_deg"]):.4f}'.rstrip("0").rstrip("."),
            str(RANK[r["type"]]),
        ]))
    (DATA / "airports.txt").write_text("\n".join(lines), encoding="utf-8")
    print(f"airports: {len(lines)}")


def land(path):
    gj = json.load(open(path))
    rings = []
    for f in gj["features"]:
        g = f["geometry"]
        polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
        for poly in polys:
            ring = [[round(x, 1), round(y, 1)] for x, y in poly[0]]
            if len(ring) > 3:
                rings.append(ring)
    (DATA / "land.json").write_text(json.dumps(rings, separators=(",", ":")))
    print(f"land rings: {len(rings)}")


def rates(path):
    src = json.load(open(path))
    pct = lambda v: round(v * 100)
    charts = {}
    for key, c in src["flight_earning_charts"].items():
        charts[key] = {
            "label": c["name"],
            "note": c.get("user_note", ""),
            "min": c.get("minimum_earning_distance", 0),
            "from": c.get("valid_from"),
            "manual": bool(c.get("manual_only")),
            "byCabin": bool(c.get("hide_booking_class")),
            "src": c.get("source_url", "https://www.alaskaair.com/atmosrewards/content/earn-points/flights"),
            "cabins": [
                {"name": cab["name"], "classes": [
                    {"codes": codes, "base": pct(r["base_earn_pct"]), "bonus": pct(r["fare_bonus_pct"]), "status": pct(r["status_earn_pct"])}
                    for codes, r in cab["booking_classes"].items() if "base_earn_pct" in r
                ]}
                for cab in c["cabin_options"]
            ],
        }
    out = {
        "verified": src["calculator_contract"]["verified_at"],
        "statusLevels": [{"key": s["key"], "name": s["name"].split(" (")[0], "bonus": pct(s["bonus_pct"])} for s in src["status_levels"]],
        "tiers": [{"name": t["name"], "points": t["points"], "oneworld": t["oneworld_tier"]} for t in src["status_thresholds"]],
        "milestones": [m["points"] for m in src["status_milestones"]["thresholds"]],
        "airlines": [{"key": a["key"], "name": a["name"], "code": a["iata_code"], "group": a["type"], "via": a["rules"]} for a in src["airlines"]],
        "charts": charts,
        "cards": [{
            "key": c["key"], "name": c["name"], "relBonus": pct(c.get("relationship_bonus_pct", 0)),
            "statusPer": c["status_point_ratio"]["spend"], "anniversary": c.get("anniversary_status_points", 0),
            "note": c.get("user_note", ""),
            "src": c.get("source_url"),
            "cats": [{"key": k["key"], "label": k["label"], "rate": k["rate"], "cap": k.get("annual_spend_cap")} for k in c["spend_categories"]],
        } for c in src["credit_cards"]],
        "sources": {
            "flights": "https://www.alaskaair.com/atmosrewards/content/earn-points/flights",
            "partners": "https://www.alaskaair.com/atmosrewards/content/partners/airlines",
            "saver": "https://www.alaskaair.com/content/travel-info/flight-experience/saver",
            "award": "https://www.alaskaair.com/atmosrewards/content/use-points/award-charts",
            "status": "https://www.alaskaair.com/atmosrewards/content/earn-points/status-points-guide",
        },
    }
    (DATA / "rates.json").write_text(json.dumps(out, indent=1))
    print(f"charts: {len(charts)}, airlines: {len(out['airlines'])}, cards: {len(out['cards'])}")


if __name__ == "__main__":
    airports(sys.argv[1]); land(sys.argv[2]); rates(sys.argv[3])
