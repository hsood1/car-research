# CLAUDE.md — car-research

Single-page car comparison for two buyers, published to GitHub Pages at
**https://hsood1.github.io/car-research/** from `main`.

## Layout

Everything lives in `index.html` — markup, CSS and JS in one file, no build step and
no dependencies. Push to `main` and GitHub Pages redeploys.

| File | What it is |
|---|---|
| `index.html` | The whole site. Data, model and rendering. |
| `model.py` | Standalone Python that reproduces the cost model. Use it to sanity-check the JS. |
| `cash-vs-finance.py` | The finance-vs-invest arbitrage model. |
| `tco.py` | Earlier total-cost model, superseded by `model.py`. |

## The two buyers

Referred to as **Buyer K** and **Buyer U** — never by name.

| | Buyer K | Buyer U |
|---|---|---|
| Market | San Diego, CA | Memphis, TN → living in Michigan |
| Cars shown | **3** (RAV4, CX-50, CR-V) | **4** (+ Equinox) |
| Requirement | Hybrid, FWD ok | AWD |
| Mileage | 100,000 over 10 years | 100,000 over 10 years |
| Tax | 7.75%, $85 doc cap | 7%+$88, $799–958 doc |
| Trade | none | Accord, slider 0–30k, default 20k |
| Yield | 3.28% (3-yr Treasury, CA-exempt) | 3.38% (5-yr CD, no state tax) |

**Buyer K sees three cars.** Don't write copy that says "all four" on his side, and
don't score the Equinox in his serviceability panel.

Each page must stand alone — no CA-vs-TN comparisons. California facts on K's page,
Tennessee facts on U's.

## Structure of index.html

Data objects near the top of `<script>`, then the model, then rendering:

- `COLORS` / `INTERIORS` — palettes. Exterior entries are `[name, hex, urlTemplate]`;
  interiors are `[name, hex, accentHex, url]`. **The URL index differs** — exterior is
  `col[2]`, interior is `col[3]`. `stage()` handles this with `col.length>3?col[3]:col[2]`.
- `VIEWS` — the frame token substituted into `{V}` in an exterior URL. All four are set
  to the frame that gives the same **front-three-quarter** angle.
- `MEDIA` — YouTube video IDs, keyed by car.
- `IMGNOTE` — per-car disclosure shown under the specs when the imagery isn't exactly
  the right trim.
- `CARS` — per buyer. `fair` is the negotiated selling price before rebates; `cash` is
  manufacturer customer cash; `grad` is college-grad money; `emp` is GM employee price.
- `DEALS` — per region. Fourth field is `kind|explanation` where kind is
  `ok` / `win` / `no` / `none` / `ask`.
- `CHK` — the verify-before-signing list.

## Rules that keep tripping things up

- **Fair value is pre-rebate.** Edmunds and KBB both publish a negotiated selling price
  and exclude customer cash; TrueCar and CR Build & Buy net incentives out. Never stack
  a rebate onto a TrueCar-style number.
- **Customer cash and subvented APR are either/or** at Mazda and GM. The cost model
  handles this by pricing a cash path and a finance path separately and taking the better.
- **Financing only wins when the loan rate beats the after-tax yield.** Don't assume 0%
  is free — Mazda's costs the $1,500 rebate, which prices it at ~2.33%.
- **Only report verified images.** Every image URL on the page was confirmed to return
  200 with an image content-type. A broken image is worse than none; there's an SVG
  fallback that hides itself once a real photo loads.
- **Mazda publishes only one exterior cutout** across all CX-50 trims, so its exteriors
  are photographs with their own background while the other three are cutouts on a
  CSS-built scene.
- edmunds.com and kbb.com serve bot-detection walls. Do not try to defeat them — use
  search snippets or other sources.

## Verifying a change

No test suite. Before pushing:

```bash
node -e 'const h=require("fs").readFileSync("index.html","utf8");new Function(h.match(/<script>([\s\S]*)<\/script>/)[1]);console.log("JS OK")'
```

Then load the page and check, for **both** buyers across **all** views, that
`document.documentElement.scrollWidth <= window.innerWidth` at 375px. Mobile is a real
responsive layout, not a stripped fallback — there's no "view on desktop" banner.
