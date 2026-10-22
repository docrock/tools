# Roadmap: Doc Rock Tools

The goal is one private, ad-free calculator per major loyalty program, grouped by alliance, all sharing the same airport mileage engine and the same house rules (see [README](README.md)). The long-term payoff is **Phase 6**: type a flight once and see which program you should credit it to.

Track progress on the **Tools** GitHub Project board and in [issues](https://github.com/docrock/tools/issues).

---

## ✅ Phase 0: Atmos Rewards v1 (shipped)

- Alaska + Hawaiian + 32 partners, both booking channels, every cabin and fare class
- Saver 2026 date rules, 500-mile minimum, elite bonuses, award-flight status points
- Credit cards, manual entries, status-tier and milestone progress
- Great-circle airport mileage (Vincenty/WGS-84), multi-leg routes, route map
- North Pacific and Aloha themes, light/dark, zero network requests

## Phase 1: Shared engine (do this before adding programs)

Turn the Atmos page into a program-agnostic engine so every new program is mostly a data file.

- [ ] Split the shared pieces out of `atmos-calculator/src/template.html`: airports, distance math, map, privacy banner, theme system, footer.
- [ ] One `programs/<program>/rates.json` per program, using a common schema.
- [ ] Support the three earning models every program uses:
  - **Distance × fare-class %** (Atmos, JAL, Korean, Aeroplan on partners, most partner charts)
  - **Revenue-based**: dollars spent × multiplier by status, with caps and excluded taxes/fees (Delta, United, American, JetBlue, Southwest, BA, Flying Blue)
  - **Zone/segment tables**: fixed amounts by distance band (Qantas, Avios on partners)
- [ ] Track the status currency separately per program (status points, MQDs, PQPs, Loyalty Points, XP, tier points…).
- [ ] Build-time tests that reproduce each program's own published worked examples before release.
- [ ] Optional ticket-price input, which revenue-based programs need.

## Phase 2: oneworld (Alaska's alliance)

| Program | Airline | Earning model | Notes |
|---|---|---|---|
| AAdvantage | American | Revenue (AA) / distance (partners) | Loyalty Points drive status |
| JAL Mileage Bank | Japan Airlines | Distance × fare class | FLY ON points for status |
| British Airways Club | British Airways | Revenue (Avios + tier points) | Partner flights use zone tables |
| Qantas Frequent Flyer | Qantas | Zone/fare-class tables | Status credits |
| Asia Miles / Cathay | Cathay Pacific | Distance × fare class | Status points |
| Privilege Club | Qatar Airways | Distance/zone by fare class | Qpoints; Avios currency |

## Phase 3: SkyTeam

| Program | Airline | Earning model | Notes |
|---|---|---|---|
| SkyMiles | Delta | Revenue by status | MQDs drive Medallion status |
| Flying Blue | Air France / KLM | Revenue (miles) + XP by distance band | XP tables by cabin and distance |
| SKYPASS | Korean Air | Distance × fare class | Also an Atmos partner, so reuse the airport data |
| Flying Club | Virgin Atlantic | Distance × fare class | Tier points |
| Club Premier | Aeroméxico | Revenue / partner tables | Check after the Phase 1 engine |

## Phase 4: Star Alliance

| Program | Airline | Earning model | Notes |
|---|---|---|---|
| MileagePlus | United | Revenue by status | PQPs/PQFs drive Premier status |
| Aeroplan | Air Canada | Revenue (AC) / distance × fare class (partners) | Status Qualifying Credits |
| ANA Mileage Club | ANA | Distance × fare class | Premium Points |
| Miles & More | Lufthansa Group | Revenue / distance tables | Points and qualifying points |
| KrisFlyer | Singapore Airlines | Distance × fare class | Elite miles |
| Miles&Smiles | Turkish Airlines | Distance × fare class | Status miles |

## Phase 5: Independent airlines

| Program | Airline | Earning model | Notes |
|---|---|---|---|
| TrueBlue | JetBlue | Revenue by fare | Tiles (Mosaic). Blue Sky partnership with United |
| Rapid Rewards | Southwest | Revenue by fare type | A-List tier qualifying points |

## Phase 6: "Where should I credit this flight?"

- [ ] Enter a flight once (route, airline, fare class, price) and see the earnings in every eligible program side by side.
- [ ] Highlight the best program for points and the best one for status progress.
- [ ] A per-alliance view: which programs a given operating airline can credit to.

## Parking lot

- [ ] **Notion embed.** Add the calculator as an `/embed` block on a Notion page or database.
- [ ] **Newsletter link.** Swap the Community placeholder on the newsletter button for a real Kit signup link.
- [ ] **Hosting.** A custom domain such as `tools.<domain>` pointing at GitHub Pages, plus Squarespace Code Block iframes for the site.
- [ ] **Affiliate slots.** Fill the sidebar and divider slots with real Amazon/travel affiliate links (tag `infophreak-20`), text links only to keep zero network requests.
- [ ] **Rate freshness.** Re-verify every program's rates quarterly and bump the "last checked" date.

---

### Checklist for adding any program

1. Collect the official earning pages (primary sources only) and save their URLs in the rates file.
2. Encode rates in the shared schema, with `verified` dates.
3. Reproduce the program's published worked examples as tests.
4. Pick brand-*inspired* colors: no logos, no trademarked names as branding, no official fonts.
5. Add the "not affiliated" line and the "last checked" date.
6. Confirm zero network requests on the built page and no sideways scrolling at 375 px.
