# 10-year TCO model. All [EST] residuals flagged.
def loan_interest(principal, apr, months):
    if principal <= 0: return 0.0, 0.0
    if apr == 0: return 0.0, principal/months
    r = apr/12/100
    pmt = principal*r/(1-(1+r)**-months)
    return pmt*months - principal, pmt

def run(label, price, dest_incl, tax_rate, tax_fixed, trade, down, apr, months, cash_rebate,
        mpg, miles_total, gas, maint_10yr, orig_msrp, resid_pct, note=""):
    taxable = max(0, price - cash_rebate - trade)
    tax = taxable*tax_rate + tax_fixed
    otd = price - cash_rebate + tax
    financed = max(0, otd - trade - down)
    interest, pmt = loan_interest(financed, apr, months)
    fuel = miles_total/mpg*gas
    resid = orig_msrp*resid_pct
    net = otd - trade + interest + fuel + maint_10yr - resid
    return dict(label=label, price=price, otd=round(otd), financed=round(financed),
                pmt=round(pmt), interest=round(interest), fuel=round(fuel),
                maint=maint_10yr, resid=round(resid), net=round(net), note=note)

def show(title, rows):
    print("\n"+"="*112); print(title); print("="*112)
    print(f"{'option':<44}{'price':>8}{'OTD':>9}{'pmt':>7}{'int':>8}{'fuel':>8}{'maint':>7}{'resid':>8}{'NET10':>9}")
    for r in sorted(rows, key=lambda x: x['net']):
        print(f"{r['label']:<44}{r['price']:>8,}{r['otd']:>9,}{r['pmt']:>7,}{r['interest']:>8,}"
              f"{r['fuel']:>8,}{r['maint']:>7,}{r['resid']:>8,}{r['net']:>9,}")
        if r['note']: print(f"    ^ {r['note']}")

# ---------------- BUYER 1 — San Diego, CA. 80,000 mi / 10 yr. $5.25/gal. 7.75% tax. no trade.
K = dict(dest_incl=True, tax_rate=.0775, tax_fixed=0, trade=0, miles_total=80000, gas=5.25)
kn=[]
# NEW
kn.append(run("NEW CX-50 Hyb Premium (0%/36mo)",      39645,1,.0775,0,0,0,0.0,36,0,     38,80000,5.25,7000,39645,.28,"0% is 36mo ONLY -> forfeits $1,500 cash"))
kn.append(run("NEW CX-50 Hyb Premium ($1.5k cash/60)",39645,1,.0775,0,0,0,4.6,60,1500,  38,80000,5.25,7000,39645,.28,"credit union 4.6%, keeps rebate"))
kn.append(run("NEW RAV4 XLE Prem FWD (4.99%/48)",     37550,1,.0775,0,0,0,4.99,48,0,    43,80000,5.25,6000,37550,.35,"no rebate exists; watch dealer markup"))
kn.append(run("NEW CR-V Hyb Sport-L FWD (3.49%/60)",  40175,1,.0775,0,0,0,3.49,60,750,  40,80000,5.25,6500,40175,.32,"OVER $40k budget w/ destination"))
# USED (current gen)
kn.append(run("USED 25 CX-50 Hyb Prem ~8k mi",        32500,1,.0775,0,0,0,5.29,60,0,    38,80000,5.25,7500,39645,.24,"~4-6 exist in 150mi; mostly 60-95mi away"))
kn.append(run("USED 25 CX-50 Hyb Prem PLUS ~28k mi",  30215,1,.0775,0,0,0,5.29,60,0,    38,80000,5.25,7500,41945,.22,"MORE equipment than new Premium"))
kn.append(run("USED 25 CR-V Hyb Sport-L ~25k mi",     33200,1,.0775,0,0,0,5.29,60,0,    40,80000,5.25,7000,40175,.28,"only 8% off new = weak"))
kn.append(run("USED 24 CR-V Hyb Sport-L ~30k mi",     29000,1,.0775,0,0,0,5.29,60,0,    40,80000,5.25,7500,37645,.25,"25% off; HondaTrue CPO ~$340 = best CPO value"))
show("BUYER 1 — San Diego, CA | 80,000 mi over 10 yr | $5.25/gal | 7.75% tax | no trade | $0 down", kn)

# ---------------- BUYER 2 — Memphis, TN → Michigan. 120,000 mi / 10 yr. $3.50/gal. 7% + $88. $15k trade.
un=[]
un.append(run("NEW Equinox LT AWD +ConvPkgII (0%/36)",34845,1,.07,88,15000,0,0.0,36,0,  26,120000,3.50,8500,34845,.20,"$2,050 pkg REQUIRED for power seat"))
un.append(run("NEW Equinox LT AWD @ employee price [EST]",      31600,1,.07,88,15000,0,0.0,36,0,  26,120000,3.50,8500,34845,.20,"employee price UNVERIFIED"))
un.append(run("NEW RAV4 XLE Prem AWD (4.99%/48)",     38950,1,.07,88,15000,0,4.99,48,0, 41,120000,3.50,7000,38950,.30,"local asking runs ~$41k, not MSRP"))
un.append(run("NEW CX-50 Hyb Premium (0%/36mo)",      39645,1,.07,88,15000,0,0.0,36,0,  38,120000,3.50,8000,39645,.24,""))
un.append(run("NEW CR-V Hyb Sport-L AWD (3.49%/60)",  41675,1,.07,88,15000,0,3.49,60,750,37,120000,3.50,7500,41675,.27,"dest now $1,450 -> $41,675 sticker"))
un.append(run("USED 25 Equinox LT AWD ~30k mi",       27500,1,.07,88,15000,0,5.29,60,0, 26,120000,3.50,9000,32495,.16,"VIN-check for power seat! most are 6-way manual"))
un.append(run("USED 26 CR-V Sport-L AWD ~1-5k mi",    38000,1,.07,88,15000,0,5.29,60,0, 37,120000,3.50,7500,41675,.26,"~$3.7k under new, 2 exist within 230mi"))
un.append(run("USED 25 CX-50 Hyb Prem ~15k mi",       33000,1,.07,88,15000,0,5.29,60,0, 38,120000,3.50,8500,39645,.22,"2 in Memphis metro; 250mi search needed"))
show("BUYER 2 — Memphis, TN → Michigan | 120,000 mi over 10 yr | $3.50/gal | 7%+$88 | $15,000 trade | $0 down", un)
