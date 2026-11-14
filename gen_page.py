import json, pathlib
D = pathlib.Path(__file__).parent
S = json.load(open(D/'slides.json', encoding='utf-8'))

def sec(s):
    items = ''.join(f'<div class="c"><b>{a}</b><p>{b}</p></div>' for a, b in s['items'])
    return f'<div class="k">{s["kicker"]}</div><h2>{s["title"]}</h2><div class="g">{items}</div>'

def script(s):
    return f'<details><summary>발표 대본</summary><p>{" ".join(s["say"])}</p></details>'

# ---------- 02 인테리어: 평면도 ----------
FLOOR = '''<figure class="fig"><svg viewBox="0 0 800 420" role="img" aria-label="40평 매장 평면도: 입구 픽업존, 카운터, 바 테이블, 1인석, 창가 소파존, 오픈 키친">
<rect x="10" y="10" width="780" height="400" rx="14" class="wall"/>
<rect x="30" y="300" width="200" height="90" rx="10" class="z1"/><text x="130" y="340">픽업 존</text><text x="130" y="366" class="s">모바일 주문 3분 픽업</text>
<rect x="30" y="30" width="200" height="250" rx="10" class="z2"/><text x="130" y="140">오픈 키친</text><text x="130" y="166" class="s">베이킹 · 진열</text>
<rect x="250" y="30" width="240" height="70" rx="10" class="z3"/><text x="370" y="72">카운터 · 쇼케이스</text>
<rect x="250" y="120" width="240" height="160" rx="10" class="z4"/><text x="370" y="196">바 테이블 · 1인석</text><text x="370" y="222" class="s">콘센트 · 평일 업무/미팅</text>
<rect x="510" y="30" width="260" height="360" rx="10" class="z5"/><text x="640" y="200">창가 소파존</text><text x="640" y="226" class="s">주말 체류 · 단체석</text>
<rect x="250" y="300" width="240" height="90" rx="10" class="z6"/><text x="370" y="350">화장실 · 창고</text>
<path d="M30 410h200" class="door"/><text x="130" y="404" class="s">▲ 입구 (대로변)</text>
</svg><figcaption>40평 매장 존 배치 (예시). 평일 동선은 입구 → 픽업 존, 주말 동선은 카운터 → 창가 소파존</figcaption></figure>'''

# ---------- 03 메뉴판 ----------
MENU = [('모닝 (~11시)', [('모닝 세트 (아메리카노+소금빵)', '6,900'), ('아메리카노', '4,500'), ('소금빵', '3,500')]),
        ('시그니처', [('봉은 흑임자 라떼', '6,500'), ('크림 브륄레 크루아상', '5,800'), ('카페라떼', '5,300')]),
        ('런치', [('잠봉뵈르', '9,500'), ('치아바타 샌드위치', '8,900'), ('수프 + 빵 세트', '9,900')]),
        ('주말 · 선물', [('캐러멜 휘낭시에 박스 (6입)', '16,000'), ('시그니처 원두 200g', '18,000'), ('홀케이크', '38,000')])]
menu_html = '<div class="menu">' + ''.join(
    f'<div class="mc"><h3>{h}</h3>' + ''.join(f'<div class="mi"><span>{n}</span><i></i><b>{p}</b></div>' for n, p in rows) + '</div>'
    for h, rows in MENU) + '</div><p class="note">가격은 강남 일대 스페셜티 카페의 일반적인 가격대를 기준으로 정한 예시 값이에요.</p>'

# ---------- 04 손익: 시나리오 + 계산기 ----------
# 고정비(월): 임대료 800, 인건비 1,300, 기타 550 = 2,650만 원 / 변동비: 원가 32%
SCN = [('비관', 130), ('기본', 180), ('낙관', 230)]
FIX, COGS, INV = 2650, 0.32, 40000
rows = ''
for name, day in SCN:
    rev = day * 30; op = rev * (1 - COGS) - FIX
    import math
    pay = '손익분기 수준' if op < rev*0.01 else f'{math.ceil(INV/op)}개월'
    rows += f'<tr class="{"base" if name=="기본" else ""}"><td>{name}</td><td>{day:,}만</td><td>{rev:,}만</td><td>{op:,.0f}만</td><td>{op/rev*100:.0f}%</td><td>{pay}</td></tr>'
bep_m = FIX / (1 - COGS)
PNL = f'''<table class="t"><thead><tr><th>시나리오</th><th>일 매출</th><th>월 매출</th><th>월 영업이익</th><th>이익률</th><th>투자 회수</th></tr></thead><tbody>{rows}</tbody></table>
<div class="bep"><b>손익분기점</b> 월 매출 약 <strong>{bep_m:,.0f}만 원</strong> (하루 약 {bep_m/30:,.0f}만 원). 고정비 월 2,650만 원(임대료 800 · 인건비 1,300 · 기타 550) ÷ 공헌이익률 68%</div>
<div class="calc"><h3>🧮 직접 계산해 보기</h3>
<label>일 평균 매출 <output id="o_day"></output><input id="day" type="range" min="80" max="320" step="10" value="180"></label>
<label>원가율 <output id="o_cogs"></output><input id="cogs" type="range" min="25" max="40" step="1" value="32"></label>
<label>월 임대료 <output id="o_rent"></output><input id="rent" type="range" min="400" max="1500" step="50" value="800"></label>
<label>월 인건비 <output id="o_labor"></output><input id="labor" type="range" min="800" max="2500" step="25" value="1300"></label>
<label>초기 투자 <output id="o_inv"></output><input id="inv" type="range" min="25000" max="70000" step="1000" value="40000"></label>
<div class="res"><div><small>월 매출</small><b id="r_rev"></b></div><div><small>월 영업이익</small><b id="r_op"></b></div><div><small>이익률</small><b id="r_m"></b></div><div><small>투자 회수</small><b id="r_pay"></b></div></div>
<p class="note">기타 비용(관리비·카드수수료·마케팅 등)은 월 550만 원으로 고정했어요.</p></div>
<script>
const $=id=>document.getElementById(id),f=n=>Math.round(n).toLocaleString('ko-KR');
function calc(){{const d=+$('day').value,c=+$('cogs').value,r=+$('rent').value,l=+$('labor').value,i=+$('inv').value;
$('o_day').textContent=f(d)+'만 원';$('o_cogs').textContent=c+'%';$('o_rent').textContent=f(r)+'만 원';$('o_labor').textContent=f(l)+'만 원';$('o_inv').textContent=(i/10000).toFixed(1)+'억 원';
const rev=d*30,op=Math.round(rev*(100-c)/100-r-l-550);$('r_rev').textContent=f(rev)+'만';$('r_op').textContent=f(op)+'만';$('r_op').className=op<0?'neg':'';
$('r_m').textContent=(op/rev*100).toFixed(1)+'%';$('r_pay').textContent=op<rev*0.01?'손익분기 이하':Math.ceil(i/op)+'개월';}}
document.querySelectorAll('.calc input').forEach(e=>e.addEventListener('input',calc));calc();
</script>'''

import json as _j
SC=_j.load(open(D/'data'/'scored.json',encoding='utf-8')); ST=_j.load(open(D/'data'/'stor.json',encoding='utf-8'))
def _row(r):
    c=ST.get(r['cd'],{}).get('STOR_CO',0); per=f"{r['sales']/3/c/1e4:,.0f}만" if c else '-'
    hl=' class="base"' if r['nm']=='봉은사역' else ''
    return f"<tr{hl}><td>{r['rank']}</td><td>{r['nm']}<br><small>{r['gu']} {r['dong']}</small></td><td>{r['score']}</td><td>{r['g_sales']*100:+.0f}%</td><td>{r['g_flp']*100:+.0f}%</td><td>{r['g_wrc']*100:+.0f}%</td><td>{int(c)}</td><td>{per}</td></tr>"
pick=SC[:12]
DATA='<h3 style="margin-top:20px">📊 362개 상권 성장 점수 순위 (상위 12)</h3><div class="tw"><table class="t"><thead><tr><th>순위</th><th>상권</th><th>점수</th><th>카페 매출</th><th>유동인구</th><th>직장인구</th><th>카페 수</th><th>카페당 월매출</th></tr></thead><tbody>'+''.join(_row(r) for r in pick)+'</tbody></table></div><p class="note">비교 기간: 2023년 2분기 → 2026년 2분기 · 업종: 커피-음료 · 3년 전 분기 카페 매출 3억 원 미만 상권 제외 · 점수 = 매출 성장 30% + 유동인구 성장 20% + 직장인구 성장 20% + 매출 규모 15% + 아침(06~11시) 매출 비중 15% (각 항목 백분위). 1위 성수 일대는 이미 뜬 상권이라 임대료 부담이 크고, 12위 신용산역은 카페가 103개로 포화 상태예요.</p>'
EXTRA = {1: DATA, 2: FLOOR, 3: menu_html, 4: PNL}
body = ''.join(f'<section>{sec(s)}{EXTRA.get(i, "")}{script(s)}</section>' for i, s in enumerate(S))

CSS = '''
:root{--bg:#f6f3ff;--ink:#1e1b2e;--card:#fff;--ac:#6d3fd6;--ac2:#e0d6ff;--mut:#6f6886;--line:#e3dbfb;--neg:#d6453f}
@media(prefers-color-scheme:dark){:root{--bg:#16131f;--ink:#efeaff;--card:#221d30;--ac:#a98bff;--ac2:#3a2f5c;--mut:#a59fbb;--line:#352e4a;--neg:#ff7a72}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:'Pretendard','Malgun Gothic',sans-serif;line-height:1.6}
main{max-width:1040px;margin:auto;padding:48px 16px}h1{font-size:clamp(28px,5vw,48px);margin:.2em 0}h1 b,h2 b{color:var(--ac)}
.k{color:var(--ac);font-weight:700;letter-spacing:3px;font-size:13px}video{width:100%;border-radius:18px;background:#000;margin:20px 0 8px}
section{margin-top:56px}h2{font-size:clamp(22px,3.5vw,32px);margin:.2em 0 .6em}h3{margin:0 0 10px}
.g{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px}.c,.mc,.calc,.fig{background:var(--card);border-radius:16px;padding:16px 18px}
.c b{color:var(--ac);font-size:14px}.c p{margin:.3em 0 0}details{margin-top:12px;color:var(--mut)}summary{cursor:pointer}
.fig{margin:16px 0 0}.fig svg{width:100%;height:auto}.fig text{fill:var(--ink);font-size:20px;font-weight:700;text-anchor:middle}.fig text.s{font-size:14px;font-weight:400;fill:var(--mut)}
.wall{fill:none;stroke:var(--ink);stroke-width:3}.z1,.z2,.z3,.z4,.z5,.z6{stroke:var(--ac);stroke-width:1.5}.z1{fill:var(--ac2)}.z2,.z5{fill:color-mix(in srgb,var(--ac2) 60%,transparent)}.z3,.z4,.z6{fill:color-mix(in srgb,var(--ac2) 30%,transparent)}
.door{stroke:var(--bg);stroke-width:8}figcaption{color:var(--mut);font-size:14px;margin-top:8px}
.menu{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:12px;margin-top:16px}.mc h3{color:var(--ac);font-size:16px}
.mi{display:flex;align-items:baseline;gap:6px;margin:6px 0}.mi i{flex:1;border-bottom:1px dotted var(--mut)}.mi b{font-variant-numeric:tabular-nums}
.note{color:var(--mut);font-size:13px}.t{width:100%;border-collapse:collapse;margin-top:16px;background:var(--card);border-radius:16px;overflow:hidden;font-variant-numeric:tabular-nums}
.t small{color:var(--mut)}.t th,.t td{padding:10px 12px;text-align:right;border-bottom:1px solid var(--line)}.t th:first-child,.t td:first-child{text-align:left}.t tr.base{background:var(--ac2);font-weight:700}
.bep{margin:12px 0;padding:12px 16px;border-left:4px solid var(--ac);background:var(--card);border-radius:8px}.bep strong{color:var(--ac)}
.calc label{display:grid;grid-template-columns:1fr auto;gap:2px 12px;margin:10px 0}.calc input{grid-column:1/-1;accent-color:var(--ac)}.calc output{font-weight:700}
.res{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:10px;margin-top:14px}.res div{background:var(--bg);border-radius:12px;padding:10px 12px}
.res small{display:block;color:var(--mut)}.res b{font-size:22px;font-variant-numeric:tabular-nums}.res b.neg{color:var(--neg)}
.tw{overflow-x:auto}footer{color:var(--mut);font-size:13px;margin-top:56px}'''

html = f'''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>성장 상권 출점 전략</title><style>{CSS}</style></head><body><main>
<div class="k">CASE BRIEF · 상권 분석 컨설팅</div><h1>3년 뒤 뜰 상권, <b>강남 봉은사역</b>에 출점합니다</h1>
<p>PE 보유 커피·베이커리 전문점의 신규 출점 전략: 입지 선정, 인테리어 컨셉, 메뉴 구성, 손익 시뮬레이션.</p>
<video src="pitch.mp4" controls preload="metadata"></video><div class="k">2분 발표 영상 · 내레이션 · 자막 포함</div>
{body}
<footer>데이터 출처: 서울 열린데이터광장 상권분석서비스(상권변화지표·직장인구·유동인구·추정매출). 상권 지표(2023·2026년 2분기)는 실제 데이터이며, 매장 매출·비용은 상권 평균을 바탕으로 가정한 시뮬레이션 값입니다. 추정매출은 카드 결제 등을 기반으로 한 추정치예요.</footer></main></body></html>'''
html = html.replace('<table class="t">', '<div class="tw"><table class="t">').replace('</table>', '</table></div>')
(D/'index.html').write_text(html, encoding='utf-8'); print('page ok')
