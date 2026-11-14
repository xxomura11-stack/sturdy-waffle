# 성장 상권 출점 전략: 커피·베이커리 전문점

PE가 보유한 커피·베이커리 전문점의 신규 출점 전략 제안입니다. 결론은 **강남구 삼성1동 봉은사역 상권**입니다.

- `index.html`: 제안서 페이지 (2분 발표 영상, 입지 선정, 인테리어, 메뉴, 손익 시뮬레이션, 계산기 포함)
- `pitch.mp4`: 2분 발표 영상 (내레이션·자막)
- `fetch.py` / `analyze.py`: 서울 열린데이터광장 상권분석서비스 수집·분석 (2023년 2분기 → 2026년 2분기, 362개 상권)
- `gen_page.py` / `build.py` / `slides.json`: 페이지·영상 생성

다시 실행하려면 `.env`에 `SEOUL_API_KEY=인증키`를 넣고 `python fetch.py` → `python analyze.py` → `python gen_page.py` → `python build.py` 순서로 실행하세요.
