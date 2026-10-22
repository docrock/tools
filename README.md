# Doc Rock Tools

Free, private, single-file web tools. Live at **https://docrock.github.io/tools/**

| Tool | Link | What it does |
|---|---|---|
| Atmos Rewards Points Calculator | [/atmos-calculator/](https://docrock.github.io/tools/atmos-calculator/) | Atmos points + status from Alaska, Hawaiian and partner flights, credit cards and manual entries, with great-circle airport mileage and a route map. |

## House rules for every tool

- **One self-contained HTML file.** No outside scripts, fonts, analytics or APIs. A Content-Security-Policy meta tag makes the browser block any network request.
- **No personal data kept.** Inputs live in page memory only. The only thing allowed in `localStorage` is a cosmetic preference such as the color theme.
- **Brand-safe.** Colors and motifs may be *inspired by* airlines, but no logos, trademarks used as branding, or official fonts. Every tool carries a "not affiliated" line.
- **Sources cited.** Every rate links to the airline's official page and shows the date it was last checked.

## Atmos calculator layout

```
atmos-calculator/
  index.html          ← built page (what GitHub Pages serves). Don't edit by hand.
  src/template.html   ← page markup, styles and logic
  data/rates.json     ← earning rates from Alaska's published Atmos charts
  data/airports.txt   ← ~9,000 airports from OurAirports (public domain)
  data/land.json      ← world outline from Natural Earth (public domain)
  tools/prepare_data.py  ← regenerates data/ from raw sources
  tools/build.py         ← inlines data/ into src/template.html → index.html
```

Rebuild after editing the template or data:

```bash
python3 atmos-calculator/tools/build.py
```

Earning rates were last checked July 16, 2026. Update `data/rates.json` (or rerun `prepare_data.py`) when Alaska changes its charts.

See [ROADMAP.md](ROADMAP.md) for what's next.
