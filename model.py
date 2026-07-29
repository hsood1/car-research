import json
def pmt(P,apr,n):
    if P<=0: return 0.0
    if apr==0: return P/n
    r=apr/1200; return P*r/(1-(1+r)**-n)
def interest(P,apr,n): return pmt(P,apr,n)*n-P
def grow(P0,pay,n,y):
    r=y/1200; b=P0
    for _ in range(n): b=b*(1+r)-pay
    return b

# ---- verified yields, 28 Jul 2026 ----
FED=24.0
Y={'CA':{'treas3y':4.31,'cd36':4.35,'st':9.3},'TN':{'treas3y':4.31,'cd60':4.45,'st':0.0}}
ca_treas=4.31*(1-FED/100)                    # CA exempt on Treasuries
ca_cd   =4.35*(1-(FED+9.3)/100)
tn_cd   =4.45*(1-FED/100)
print(f"BEST AFTER-TAX YIELD")
print(f"  Buyer 1 CA: 3-yr Treasury 4.31% (state-exempt) -> {ca_treas:.2f}%   [CD 4.35% -> {ca_cd:.2f}%]")
print(f"  Buyer 2 TN: 5-yr CD 4.45% (no state tax)       -> {tn_cd:.2f}%")
YIELD={'A':ca_treas,'B':tn_cd}

CARS={'A':[
 dict(k='rav4',n='Toyota RAV4 XLE Premium',dr='FWD',msrp=37695,fair=37695,cash=0,
      apr=[(4.99,48),(5.99,60),(6.99,72)],mpg=43,maint=6000,resid=.35,hyb=0),
 dict(k='cx50',n='Mazda CX-50 Hybrid Premium',dr='AWD',msrp=39645,fair=38600,cash=1500,
      apr=[(0,36),(2.9,60),(3.9,72)],mpg=38,maint=7000,resid=.28,hyb=0),
 dict(k='crv',n='Honda CR-V Hybrid Sport-L',dr='FWD',msrp=40175,fair=38800,cash=0,
      apr=[(3.49,36),(4.49,60),(5.49,72)],mpg=40,maint=6500,resid=.32,hyb=0)],
 'B':[
 dict(k='rav4',n='Toyota RAV4 XLE Premium',dr='AWD',msrp=39095,fair=39095,cash=0,
      apr=[(4.99,48),(5.99,60),(6.99,72)],mpg=41,maint=7000,resid=.30,hyb=1),
 dict(k='cx50',n='Mazda CX-50 Hybrid Premium',dr='AWD',msrp=39645,fair=38600,cash=1500,
      apr=[(0,36),(2.9,60),(3.9,72)],mpg=38,maint=8000,resid=.24,hyb=1),
 dict(k='crv',n='Honda CR-V Hybrid Sport-L',dr='AWD',msrp=41675,fair=40251,cash=0,
      apr=[(2.49,36),(3.49,60),(4.49,72)],mpg=37,maint=7500,resid=.27,hyb=1),
 dict(k='eqx',n='Chevrolet Equinox LT + Conv II',dr='AWD',msrp=34845,fair=33200,cash=0,emp=32250,
      apr=[(0,36),(2.9,48),(3.9,60)],mpg=26,maint=8500,resid=.20,hyb=0)]}

CFG={'A':dict(tax=.0775,fee=85+620,miles=80000,gas=5.25,hybfee=0,trade=0),
     'B':dict(tax=.07,   fee=88+799+158,miles=120000,gas=3.50,hybfee=1000,trade=20000)}

for b in ('A','B'):
    c=CFG[b]; y=YIELD[b]
    print(f"\n{'='*104}\nBUYER {b}  |  after-tax yield {y:.2f}%  |  {c['miles']:,} mi  |  ${c['gas']}/gal\n{'='*104}")
    print(f"{'vehicle':<34}{'MSRP':>8}{'fair':>8}{'cash':>7}{'net':>8}{'loAPR':>13}{'loPay':>13}{'verdict':>10}")
    out=[]
    for v in CARS[b]:
        base=v.get('emp',v['fair'])
        lo=min(v['apr'],key=lambda t:t[0]); pay=min(v['apr'],key=lambda t:pmt(base*1.08,t[0],t[1]))
        # cash path keeps the rebate; finance path forfeits it
        netcash=base-v['cash']
        taxable=base
        due_cash=netcash+taxable*c['tax']+c['fee']-c['trade']*(1+c['tax'] if b=='B' else 1)
        due_cash=netcash+taxable*c['tax']+c['fee']-c['trade']-(c['trade']*c['tax'] if b=='B' else 0)
        due_fin =base   +taxable*c['tax']+c['fee']-c['trade']-(c['trade']*c['tax'] if b=='B' else 0)
        best=None
        for apr,n in v['apr']:
            g=grow(due_cash,pmt(due_fin,apr,n),n,y)
            if best is None or g>best[0]: best=(g,apr,n)
        g,ba,bn=best
        fuel=c['miles']/v['mpg']*c['gas']; res=v['msrp']*v['resid']
        up=v['maint']+v['hyb']*c['hybfee']
        net10=due_cash+fuel+up-res-max(0,g)
        out.append((net10,v,due_cash,due_fin,g,ba,bn,lo,pay,fuel,up,res))
        print(f"{v['n']+' '+v['dr']:<34}{v['msrp']:>8,}{v['fair']:>8,}{v['cash']:>7,}{netcash:>8,.0f}"
              f"{f'{lo[0]}%/{lo[1]}':>13}{f'{pay[0]}%/{pay[1]}':>13}"
              f"{('FIN '+str(ba)+'%/'+str(bn)) if g>0 else 'CASH':>10}")
    print(f"\n  {'10-YEAR NET (best strategy)':<40}{'OTD':>10}{'fuel':>9}{'upkeep':>9}{'resale':>9}{'gain':>8}{'NET':>10}")
    for net10,v,dc,df,g,ba,bn,lo,pay,fuel,up,res in sorted(out):
        print(f"  {v['n']+' '+v['dr']:<40}{dc:>10,.0f}{fuel:>9,.0f}{up:>9,.0f}{res:>9,.0f}{max(0,g):>8,.0f}{net10:>10,.0f}")

print(f"\n{'='*104}\nFINANCE vs CASH DETAIL — interest PAID vs interest EARNED\n{'='*104}")
for b in ('A','B'):
    c=CFG[b]; y=YIELD[b]
    print(f"\nBuyer {b} (yield {y:.2f}%)")
    print(f"  {'vehicle / option':<44}{'financed':>10}{'pay/mo':>9}{'int PAID':>10}{'int EARNED':>12}{'net':>9}")
    for v in CARS[b]:
        base=v.get('emp',v['fair'])
        dc=(base-v['cash'])+base*c['tax']+c['fee']-c['trade']-(c['trade']*c['tax'] if b=='B' else 0)
        df=base+base*c['tax']+c['fee']-c['trade']-(c['trade']*c['tax'] if b=='B' else 0)
        for apr,n in v['apr']:
            p=pmt(df,apr,n); ip=interest(df,apr,n); g=grow(dc,p,n,y)
            ie=ip+g   # earned = net gain + what you paid in interest
            print(f"  {v['n'][:22]+' '+str(apr)+'%/'+str(n):<44}{df:>10,.0f}{p:>9,.0f}{ip:>10,.0f}{ie:>12,.0f}{g:>+9,.0f}")
