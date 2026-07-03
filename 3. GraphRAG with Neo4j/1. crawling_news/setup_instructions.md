# 네이버 뉴스 크롤링 설정 가이드

## 1. 필요한 패키지 설치

```bash
# Python 패키지 설치
pip install -r requirements.txt

# Playwright 브라우저 설치 (필수!)
playwright install chromium
```

## 2. 크롤링 실행

```bash
python crawl_news.py
```

## 3. 출력 결과

- 콘솔에 수집된 뉴스 제목과 링크가 출력됩니다
- `data/naver_news_YYYYMMDD_HHMMSS.csv` 형태로 CSV 파일이 생성됩니다
- `data/naver_news_YYYYMMDD_HHMMSS.json` 형태로 JSON 파일이 생성됩니다
- `data` 폴더가 자동으로 생성됩니다

## 4. 주요 기능

- **비동기 처리**: async/await를 사용하여 빠른 크롤링
- **헤드라인 뉴스**: 메인 헤드라인 기사 수집
- **리스트 뉴스**: 추가 뉴스 목록 수집
- **중복 제거**: 동일한 링크의 기사는 한 번만 저장
- **CSV 저장**: Excel에서 바로 열 수 있는 CSV 파일로 저장 (UTF-8 BOM)
- **JSON 저장**: 타임스탬프가 포함된 JSON 파일로 결과 저장
- **자동 폴더 생성**: data 폴더가 없으면 자동으로 생성

## 5. 코드 커스터마이징

### 브라우저 창 보기
```python
browser = await p.chromium.launch(headless=False)  # headless=True → False로 변경
```

### 다른 섹션 크롤링
```python
# 경제 뉴스 (섹션 101)
await page.goto('https://news.naver.com/section/101')

# 사회 뉴스 (섹션 102)
await page.goto('https://news.naver.com/section/102')

# IT/과학 뉴스 (섹션 105)
await page.goto('https://news.naver.com/section/105')
```

## 6. 문제 해결

### Playwright 브라우저가 설치되지 않은 경우
```bash
playwright install
```

### 권한 오류
```bash
# Windows에서 관리자 권한으로 실행
# 또는
pip install --user playwright
playwright install
```

## 7. 주의사항

- 웹 크롤링 시 해당 사이트의 robots.txt를 확인하세요
- 과도한 요청은 서버에 부담을 줄 수 있으므로 적절한 딜레이를 추가하세요
- 개인적인 용도로만 사용하고, 수집한 데이터의 저작권을 존중하세요

