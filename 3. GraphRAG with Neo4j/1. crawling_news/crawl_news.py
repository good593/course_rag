import asyncio
from playwright.async_api import async_playwright
import csv
import os
from datetime import datetime


async def crawl_naver_news(lst_categorys):  #category_nm:str, category_id:int):
    """네이버 뉴스 섹션에서 뉴스 제목과 링크를 크롤링합니다."""

    print("뉴스 데이터 수집 중...")
    # 뉴스 기사 목록 수집
    news_items = []

    for category in lst_categorys:
        category_id = category['category_id']
        category_nm = category['category_nm']
        
        # 강의용임으로 카테고리별 5개의 뉴스 기사만 수집 
        cnt = 0

        async with async_playwright() as p:
            # 브라우저 실행 (headless=False로 설정하면 브라우저 창이 보입니다)
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            print("네이버 뉴스 페이지 로딩 중...")
            await page.goto(f'https://news.naver.com/section/{str(category_id)}')
            
            # 페이지 로딩 대기
            await page.wait_for_load_state('networkidle')
            
            # 헤드라인 뉴스 수집
            headline_articles = await page.query_selector_all('div.sa_text')
            
            for article in headline_articles:
                try:
                    # 제목 링크 찾기
                    title_element = await article.query_selector('a.sa_text_title')
                    
                    if title_element:
                        title = await title_element.inner_text()
                        link = await title_element.get_attribute('href')
                        
                        # 상대 URL을 절대 URL로 변환
                        if link and not link.startswith('http'):
                            link = f'https://news.naver.com{link}'
                        
                        news_items.append({
                            'category':category_nm,
                            'title': title.strip(),
                            'link': link,
                            'type': 'headline'
                        })
                        
                        cnt += 1  # 카운트 증가
                        if cnt >= 5:
                            break 
                except Exception as e:
                    print(f"헤드라인 수집 중 오류: {e}")
                    continue
            
            # 추가 뉴스 기사 수집 (리스트 형태) - 아직 5개 미만인 경우만
            if cnt < 5:
                list_articles = await page.query_selector_all('div.sa_item')
                
                for article in list_articles:
                    try:
                        # 제목 링크 찾기
                        title_element = await article.query_selector('a.sa_text_strong')
                        
                        if title_element:
                            title = await title_element.inner_text()
                            link = await title_element.get_attribute('href')
                            
                            # 상대 URL을 절대 URL로 변환
                            if link and not link.startswith('http'):
                                link = f'https://news.naver.com{link}'
                            
                            # 중복 체크
                            if not any(item['link'] == link for item in news_items):
                                news_items.append({
                                    'category':category_nm,
                                    'title': title.strip(),
                                    'link': link,
                                    'type': 'list'
                                })
                                
                                cnt += 1  # 카운트 증가
                                if cnt >= 5:
                                    break
                    except Exception as e:
                        print(f"리스트 뉴스 수집 중 오류: {e}")
                        continue
            
            print(f"'{category_nm}' 카테고리에서 {cnt}개의 뉴스를 수집했습니다.")
            await browser.close()
        
    return news_items


def save_to_csv(news_data, folder='data'):
    """수집한 뉴스 데이터를 CSV 파일로 저장합니다."""
    # data 폴더가 없으면 생성
    if not os.path.exists(folder):
        os.makedirs(folder)
        print(f"'{folder}' 폴더를 생성했습니다.")
    
    # 타임스탬프로 파일명 생성
    timestamp = datetime.now().strftime('%Y%m%d')
    csv_filename = os.path.join(folder, f'naver_news_{timestamp}.csv')
    
    # CSV 파일로 저장
    with open(csv_filename, 'w', encoding='utf-8-sig', newline='') as f:
        if news_data:
            # CSV 헤더 작성
            fieldnames = ['번호', '카테고리', '제목', '링크', '타입', '수집시간']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            # 데이터 작성
            for idx, news in enumerate(news_data, 1):
                writer.writerow({
                    '번호': idx,
                    '카테고리': news['category'],
                    '제목': news['title'],
                    '링크': news['link'],
                    '타입': news['type'],
                    '수집시간': timestamp
                })
    
    return csv_filename


async def main():
    """메인 실행 함수"""
    print("=" * 80)
    print("네이버 뉴스 크롤링 시작")
    print("=" * 80)
    
    # 뉴스 크롤링 실행
    lst_categorys = [
        {
            "category_nm":"경제", 
            "category_id":101
        },
        {
            "category_nm":"생활/문화", 
            "category_id":103
        },
        {
            "category_nm":"IT/과학", 
            "category_id":105
        },
        {
            "category_nm":"세계", 
            "category_id":104
        }
    ]
    news_data = await crawl_naver_news(lst_categorys)
    
    print(f"\n총 {len(news_data)}개의 뉴스 기사를 수집했습니다.\n")
    
    # 결과 출력
    print("=" * 80)
    print("수집된 뉴스 목록:")
    print("=" * 80)
    
    for idx, news in enumerate(news_data, 1):
        print(f"\n[{idx}] {news['title']}")
        print(f"    링크: {news['link']}")
        print(f"    타입: {news['type']}")
    
    # CSV 파일로 저장
    csv_filename = save_to_csv(news_data)
    
    
    print("\n" + "=" * 80)
    print("파일 저장 완료!")
    print("=" * 80)
    print(f"CSV 파일: {csv_filename}")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())

