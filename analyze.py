import json, pathlib, statistics as st
D = pathlib.Path(__file__).parent/'data'; L = lambda n: json.load(open(D/f'{n}.json', encoding='utf-8'))
relm = {r['TRDAR_CD']: r for r in L('relm')}
idx = lambda n, f: {r['TRDAR_CD']: r for r in L(n)}
sn, so, fn, fo, ix = idx('sel_now',0), idx('sel_old',0), idx('flp_now',0), idx('flp_old',0), idx('ix',0)
wn, wo = {}, {}
for r in L('wrc'):
    if r['STDR_YYQU_CD'] == '20262': wn[r['TRDAR_CD']] = r['TOT_WRC_POPLTN_CO']
    if r['STDR_YYQU_CD'] == '20232': wo[r['TRDAR_CD']] = r['TOT_WRC_POPLTN_CO']
rows = []
for c in sn:
    if c not in so or c not in fn or c not in fo or not wo.get(c) or c not in relm: continue
    a, b = sn[c], so[c]
    if b['THSMON_SELNG_AMT'] < 3e8: continue      # 3년 전 분기 매출 3억 미만(너무 작은 상권) 제외
    rows.append(dict(cd=c, nm=a['TRDAR_CD_NM'], gu=relm[c]['SIGNGU_CD_NM'], dong=relm[c]['ADSTRD_CD_NM'], type=a['TRDAR_SE_CD_NM'],
        sales=a['THSMON_SELNG_AMT'], g_sales=a['THSMON_SELNG_AMT']/b['THSMON_SELNG_AMT']-1,
        g_flp=fn[c]['TOT_FLPOP_CO']/fo[c]['TOT_FLPOP_CO']-1, wrc=wn.get(c, 0), g_wrc=wn.get(c, 0)/wo[c]-1,
        morning=a['TMZON_06_11_SELNG_AMT']/a['THSMON_SELNG_AMT'], ix=ix.get(c, {}).get('TRDAR_CHNGE_IX_NM', '')))
def pr(key):
    s = sorted(r[key] for r in rows)
    for r in rows: r['p_'+key] = sum(v <= r[key] for v in s)/len(s)
for k in ('g_sales', 'g_flp', 'g_wrc', 'sales', 'morning'): pr(k)
# 성장성 70% (매출·유동인구·직장인구 성장), 규모 15%, 모닝 수요 15%
for r in rows: r['score'] = round(100*(.3*r['p_g_sales'] + .2*r['p_g_flp'] + .2*r['p_g_wrc'] + .15*r['p_sales'] + .15*r['p_morning']), 1)
rows.sort(key=lambda r: -r['score'])
for i, r in enumerate(rows): r['rank'] = i+1
json.dump(rows, open(D/'scored.json', 'w', encoding='utf-8'), ensure_ascii=False)
print('후보 상권 수', len(rows))
f = lambda r: f"{r['rank']:>3} {r['score']:5} {r['gu']} {r['dong']} | {r['nm']} | 매출 {r['sales']/1e8:.1f}억 ({r['g_sales']*100:+.0f}%) 유동 {r['g_flp']*100:+.0f}% 직장 {int(r['wrc'])}({r['g_wrc']*100:+.0f}%) 모닝 {r['morning']*100:.0f}% {r['ix']}"
for r in rows[:15]: print(f(r))
print('--- 용산구')
for r in rows:
    if r['gu'] == '용산구': print(f(r))
