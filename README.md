# Instinct 사용량 대시보드

하루 동안의 Instinct 사용량을 **일일 예산 대비 %** 로 기록해 보여주는 정적 대시보드입니다.
절대 단위는 표시하지 않습니다.

- 대시보드: https://sigco3111.github.io/instinct-usage-dashboard/
- 현재 상태: **샘플** (2026-10-16 하루치 기록만 포함)

## 구조

```
data/usage.json            ← 모든 기록이 들어있는 데이터 파일 (유일한 입력)
src/index.template.html    ← 대시보드 템플릿 (차트: Chart.js)
scripts/build.py           ← data + template -> dist/index.html (완전 정적)
scripts/append_day.py      ← 하루치 기록을 data에 추가/교체
.github/workflows/dashboard.yml  ← push 시 자동 빌드 → GitHub Pages 배포
```

## 하루 기록을 추가하는 방법

**방법 1 — GitHub 웹에서 바로 편집**
`data/usage.json`의 `days` 배열에 새 날짜를 추가하고 커밋하면
Actions가 페이지를 다시 빌드합니다.

**방법 2 — 스크립트 사용**

```bash
# day.json 예시: {"date":"2026-10-17","total_percent":7.2,
#                 "agents":[{"name":"...","percent":1.2}]}
python3 scripts/append_day.py day.json
git add data/usage.json && git commit -m "기록: 2026-10-17" && git push
```

같은 날짜는 중복 없이 교체됩니다. 이 방법으로 첫 실제 기록이 들어가면
상태가 자동으로 `live` (샘플 딱지 해제)가 됩니다.

## 매일 자동 집계 ("시작해" 확인 후)

1. `.github/workflows/dashboard.yml`의 `schedule` 주석 해제 — 매일 09:00 KST에 리빌드.
2. 데이터 소스 연결 — 워크플로의 "Append daily record" 단계에서
   `scripts/append_day.py`를 호출해 그날 사용량을 data에 추가
   (또는 Instinct이 매일 data/usage.json을 직접 갱신 커밋).
3. 이후에는 별도 작업 없이 대시보드가 매일 갱신됩니다.
