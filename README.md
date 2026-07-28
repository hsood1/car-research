# Car Picks 2026

Compact-SUV comparison for two buyers with different constraints, evaluated on a 10-year hold.

**Live site:** https://hsood1.github.io/car-research/

## Vehicles

| Vehicle | Buyer 1 | Buyer 2 |
|---|---|---|
| Toyota RAV4 XLE Premium (hybrid) | new only | new only |
| Mazda CX-50 Hybrid Premium | new + used | new + used |
| Honda CR-V Hybrid Sport-L | new + used | new + used |
| Chevrolet Equinox LT (gas) | — | new + used |

The RAV4 is new-only because 2026 is an all-new 6th generation — any used RAV4 is a
5th-gen car, a different and less efficient vehicle, not a discount on the same product.
The other three are unchanged within their current generation, so used units are directly
comparable.

## Buyers

- **Buyer 1 — San Diego, CA.** Hybrid required, FWD acceptable, 80,000 mi over 10 years,
  $5.25/gal, 7.75% tax, no trade-in. Budget $30–40k.
- **Buyer 2 — Memphis, TN, driving in Michigan year-round.** AWD required, gas acceptable,
  120,000 mi over 10 years, $3.50/gal, ~7% tax after the single-article cap, $15,000 trade-in.

## Files

- `index.html` — the comparison page. Two buyer tabs, each with a *Best car* / *Best deal* toggle.
- `tco.py` — the 10-year cost model behind the tables. Run with `python3 tco.py`.

## Method

Net 10-year cost = out-the-door price + loan interest + fuel + estimated maintenance − resale
at year 10. Used loans modeled at 5.29% (super-prime, 60 months); new at each brand's posted
promotional rate.

Prices verified July 28, 2026 against manufacturer press releases, Monroney window stickers,
CDTFA and Tennessee Department of Revenue rate tables, Experian's Q1 2026 State of the
Automotive Finance Market, and live dealer inventory. Used prices are observed asking prices,
not transaction prices.

**Softest inputs, in order:** 10-year resale values, the estimated employee price on the
Equinox, and maintenance. Resale drives the ranking more than any other assumption — a $2,000
swing reorders the middle of both tables.

Not financial advice.
