import json, pathlib, urllib.request, concurrent.futures as cf
D = pathlib.Path(__file__).parent; K = (D/'.env').read_text().split('=')[1].strip()
def get(svc, a, b, q=''):
    u = f'http://openapi.seoul.go.kr:8088/{K}/json/{svc}/{a}/{b}/{q}'
    for _ in range(3):
        try: return json.load(urllib.request.urlopen(u, timeout=40))[svc]
        except Exception as e: err = e
    print('fail', svc, a, q, err); return {'row': []}
def all_rows(svc, q=''):
    n = get(svc, 1, 1, q).get('list_total_count', 0)
    with cf.ThreadPoolExecutor(12) as ex:
        parts = ex.map(lambda a: get(svc, a, a+999, q).get('row', []), range(1, n+1, 1000))
    return [r for p in parts for r in p]
jobs = {'sel_now': ('VwsmTrdarSelngQq', '20262'), 'sel_old': ('VwsmTrdarSelngQq', '20232'),
        'flp_now': ('VwsmTrdarFlpopQq', '20262'), 'flp_old': ('VwsmTrdarFlpopQq', '20232'),
        'ix': ('VwsmTrdarIxQq', '20262'), }
for name, (svc, q) in jobs.items():
    rows = all_rows(svc, q)
    if name.startswith('sel'): rows = [r for r in rows if r['SVC_INDUTY_CD'] == 'CS100010']
    json.dump(rows, open(D/'data'/f'{name}.json', 'w', encoding='utf-8'), ensure_ascii=False)
    print(name, len(rows), (rows[0] if rows and name in ('relm',) else ''))
