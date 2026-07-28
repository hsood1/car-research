# Cash vs finance-and-invest. Rule: finance iff effective APR < AFTER-TAX yield on the cash.
def pmt(P, apr, n):
    if apr == 0: return P/n
    r = apr/12/100
    return P*r/(1-(1+r)**-n)

def irr_monthly(P0, pay, n):
    """APR at which paying 'pay' x n months is equivalent to keeping P0 today."""
    lo, hi = -0.5, 60.0
    for _ in range(200):
        mid = (lo+hi)/2; r = mid/12/100
        pv = pay*n if r == 0 else pay*(1-(1+r)**-n)/r
        if pv > P0: lo = mid
        else: hi = mid
    return (lo+hi)/2

print("="*100)
print("AFTER-TAX YIELD ON A 4.00% CD  (interest is ordinary income, fully taxable)")
print("="*100)
print(f"{'situation':<46}{'marginal':>10}{'after-tax':>12}")
for lbl, fed, st in [
    ("Buyer 1  CA, 22% fed + 9.3% CA",           22, 9.3),
    ("Buyer 1  CA, 24% fed + 9.3% CA  <- central",24, 9.3),
    ("Buyer 1  CA, 32% fed + 10.3% CA",          32, 10.3),
    ("Buyer 2  TN domicile, 22% fed, no state",  22, 0),
    ("Buyer 2  TN domicile, 24% fed, no state",  24, 0),
    ("Buyer 2  MI domicile, 24% fed + 4.25% MI", 24, 4.25),
]:
    m = fed+st
    print(f"{lbl:<46}{m:>9.1f}%{4.0*(1-m/100):>11.2f}%")

print("\n"+"="*100)
print("EFFECTIVE COST OF EACH FINANCING OFFER  (rebates forfeited by financing are priced in)")
print("="*100)
print(f"{'offer':<40}{'cash outlay':>12}{'payment':>10}{'term':>6}{'EFF APR':>10}   verdict vs 2.7-3.0%")

def offer(lbl, price, tax_rate, tax_fixed, apr, n, rebate_if_cash, finance_bonus=0):
    # Manufacturer rebates do NOT reduce the CA/TN taxable price.
    tax = price*tax_rate + tax_fixed
    cash_outlay  = price - rebate_if_cash + tax
    financed     = price - finance_bonus + tax
    p            = pmt(financed, apr, n)
    eff          = irr_monthly(cash_outlay, p, n)
    return lbl, cash_outlay, p, n, eff

rows = [
  offer("CX-50 Hyb Prem  0%/36 (lose $1,500)", 39645,.0775,0, 0.0, 36, 1500),
  offer("CX-50 Hyb Prem  2.9%/60 (lose $1,500)",39645,.0775,0, 2.9, 60, 1500),
  offer("RAV4 XLE Prem FWD  4.99%/48",         37550,.0775,0, 4.99,48, 0),
  offer("RAV4 XLE Prem FWD  5.99%/72",         37550,.0775,0, 5.99,72, 0),
  offer("CR-V Sport-L FWD  3.49%/60 +$750",    40175,.0775,0, 3.49,60, 0, 750),
  offer("Equinox LT AWD  0%/36 (no rebate)",   34845,.07,  88, 0.0, 36, 0),
  offer("used car, super-prime  5.29%/60",     31000,.0775,0, 5.29,60, 0),
]
for lbl, co, p, n, eff in rows:
    v = "FINANCE + CD" if eff < 2.67 else ("too close to call" if eff < 3.10 else "PAY CASH")
    print(f"{lbl:<40}{co:>12,.0f}{p:>10,.0f}{n:>6}{eff:>9.2f}%   {v}")

print("\n"+"="*100)
print("DOLLARS AT STAKE  (gain from financing instead of paying cash, over the loan term)")
print("="*100)
print(f"{'offer':<40}{'@2.67% CA':>12}{'@3.04% TN':>12}")
for lbl, co, p, n, eff in rows:
    out=[]
    for y in (2.67, 3.04):
        r=y/12/100; bal=co
        for _ in range(n): bal = bal*(1+r) - p
        out.append(bal)
    print(f"{lbl:<40}{out[0]:>12,.0f}{out[1]:>12,.0f}")

print("\n"+"="*104)
print("10-YEAR NET COST UNDER THE OPTIMAL CASH/FINANCE STRATEGY  (was: everything financed)")
print("="*104)
def net(lbl, price, tax_r, tax_f, trade, rebate, fin_gain, mpg, miles, gas, maint, msrp, resid, strat):
    tax = price*tax_r + tax_f
    otd = price - rebate + tax - (trade*tax_r)   # trade credit on tax base
    return dict(l=lbl, otd=round(otd-trade), fuel=round(miles/mpg*gas), m=maint,
                res=round(msrp*resid), gain=fin_gain, s=strat,
                net=round(otd - trade + miles/mpg*gas + maint - msrp*resid - fin_gain))

def tbl(title, rows):
    print("\n"+title); print("-"*104)
    print(f"{'option':<42}{'OTD':>9}{'fuel':>8}{'maint':>7}{'resale':>8}{'CD gain':>9}{'NET10':>9}  strategy")
    for r in sorted(rows, key=lambda x:x['net']):
        print(f"{r['l']:<42}{r['otd']:>9,}{r['fuel']:>8,}{r['m']:>7,}{r['res']:>8,}{r['gain']:>9,}{r['net']:>9,}  {r['s']}")

b1=[
 net("RAV4 XLE Premium FWD",        37550,.0775,0,0,0,   0,43,80000,5.25,6000,37550,.35,"CASH"),
 net("CX-50 Hybrid Premium",        39645,.0775,0,0,0, 227,38,80000,5.25,7000,39645,.28,"FINANCE 0%/36 + CD"),
 net("CR-V Sport-L FWD",            40175,.0775,0,0,750,320,40,80000,5.25,6500,40175,.32,"finance 3.49% (toss-up)"),
 net("2024 CR-V Sport-L ~30k used", 29000,.0775,0,0,0,   0,40,80000,5.25,7500,37645,.25,"CASH"),
 net("2025 CX-50 Prem Plus ~28k used",30215,.0775,0,0,0, 0,38,80000,5.25,7500,41945,.22,"CASH"),
 net("2025 CX-50 Premium ~8k used", 32500,.0775,0,0,0,   0,38,80000,5.25,7500,39645,.24,"CASH"),
]
tbl("BUYER 1 - San Diego | 80,000 mi | $5.25/gal | 7.75% tax | no trade", b1)

b2=[
 net("RAV4 XLE Premium AWD",        38950,.07,88,15000,0,   0,41,120000,3.50,7000,38950,.30,"CASH"),
 net("CX-50 Hybrid Premium",        39645,.07,88,15000,0, 481,38,120000,3.50,8000,39645,.24,"FINANCE 0%/36 + CD"),
 net("Equinox LT AWD + Conv Pkg II",34845,.07,88,15000,0,1858,26,120000,3.50,8500,34845,.20,"FINANCE 0%/36 + CD"),
 net("Equinox LT AWD @ employee [EST]",31600,.07,88,15000,0,1858,26,120000,3.50,8500,34845,.20,"FINANCE 0%/36 + CD"),
 net("CR-V Sport-L AWD",            41675,.07,88,15000,750,320,37,120000,3.50,7500,41675,.27,"finance 3.49% (toss-up)"),
 net("2025 CX-50 Hyb Prem ~15k used",33000,.07,88,15000,0,   0,38,120000,3.50,8500,39645,.22,"CASH"),
 net("2025 Equinox LT AWD ~30k used",27500,.07,88,15000,0,   0,26,120000,3.50,9000,32495,.16,"CASH"),
]
tbl("BUYER 2 - Memphis | 120,000 mi | $3.50/gal | 7%+$88 | $15,000 trade", b2)
