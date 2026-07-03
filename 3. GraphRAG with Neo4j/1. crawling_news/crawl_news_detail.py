"""
네이버 뉴스 상세 정보 크롤링 스크립트
CSV 파일의 링크를 이용하여 뉴스의 상세 데이터를 수집합니다.
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
import random
import os
import re

def get_news_detail(url):
    """
    네이버 뉴스 상세 페이지에서 정보 추출
    
    Args:
        url (str): 뉴스 기사 URL
    
    Returns:
        dict: 뉴스 상세 정보 (제목, 내용, 기자명, 언론사, 발행일자)
    """
    try:
        # 헤더 설정 (크롤링 차단 방지)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        }
        
        # 페이지 요청
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # BeautifulSoup으로 파싱
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 뉴스 제목 추출
        title = ""
        title_tag = soup.select_one('#title_area h2, #title_area span, #articleTitle, .media_end_head_headline')
        if title_tag:
            title = title_tag.get_text(strip=True)
        
        # 뉴스 내용 추출
        content = ""
        # 여러 가능한 셀렉터 시도
        content_tag = soup.select_one('#dic_area, #articeBody, article#contents, #newsEndContents')
        if content_tag:
            # 스크립트 태그 제거
            for script in content_tag.find_all(['script', 'style']):
                script.decompose()
            content = content_tag.get_text(strip=True, separator=' ')
            # 불필요한 공백 제거
            content = re.sub(r'\s+', ' ', content).strip()
        
        # 기자명 추출
        reporter = ""
        # 여러 패턴 시도
        reporter_patterns = [
            soup.select_one('.media_end_head_journalist_name, .byline_s, em.media_end_head_journalist_name a'),
            soup.find('em', class_='media_end_head_journalist_name'),
            soup.find('span', class_='byline'),
        ]
        
        for pattern in reporter_patterns:
            if pattern:
                reporter = pattern.get_text(strip=True)
                break
        
        # 기자명이 없으면 본문에서 패턴 찾기 (예: "홍길동 기자", "홍길동기자")
        if not reporter and content:
            reporter_match = re.search(r'([가-힣]{2,4})\s*기자', content)
            if reporter_match:
                reporter = reporter_match.group(0)
        
        # 언론사 추출
        press = ""
        press_tag = soup.select_one('.media_end_head_top_logo img, .press_logo img, #pressLogo img')
        if press_tag and press_tag.get('alt'):
            press = press_tag['alt']
        
        # 언론사 정보가 없으면 다른 방법 시도
        if not press:
            press_tag = soup.select_one('.media_end_head_top_logo, .press_logo')
            if press_tag:
                press = press_tag.get_text(strip=True)
        
        # 발행일자 추출
        publish_date = ""
        date_tag = soup.select_one('.media_end_head_info_datestamp_time, .media_end_head_info_datestamp span, .t11')
        if date_tag:
            # data-date-time 속성 확인
            publish_date = date_tag.get('data-date-time', '')
            if not publish_date:
                publish_date = date_tag.get_text(strip=True)
        
        # 발행일자가 없으면 다른 방법 시도
        if not publish_date:
            date_pattern = soup.find('span', class_='media_end_head_info_datestamp_time')
            if date_pattern:
                publish_date = date_pattern.get('data-date-time', date_pattern.get_text(strip=True))
        
        return {
            'url': url,
            'title': title,
            'content': content[:500] if len(content) > 500 else content,  # 내용이 너무 길면 500자로 제한
            'reporter': reporter,
            'press': press,
            'publish_date': publish_date,
            'status': 'success'
        }
        
    except requests.exceptions.RequestException as e:
        print(f"요청 오류 발생: {url} - {str(e)}")
        return {
            'url': url,
            'title': '',
            'content': '',
            'reporter': '',
            'press': '',
            'publish_date': '',
            'status': f'error: {str(e)}'
        }
    except Exception as e:
        print(f"파싱 오류 발생: {url} - {str(e)}")
        return {
            'url': url,
            'title': '',
            'content': '',
            'reporter': '',
            'press': '',
            'publish_date': '',
            'status': f'error: {str(e)}'
        }

def crawl_news_details(input_csv_path, output_csv_path):
    """
    CSV 파일의 뉴스 링크를 읽어서 상세 정보를 크롤링
    
    Args:
        input_csv_path (str): 입력 CSV 파일 경로
        output_csv_path (str): 출력 CSV 파일 경로
    """
    # CSV 파일 읽기
    df = pd.read_csv(input_csv_path, encoding='utf-8-sig')
    print(f"총 {len(df)}개의 뉴스 기사를 크롤링합니다.")
    
    # 결과 저장 리스트
    results = []
    
    # 각 링크에 대해 크롤링 수행
    for idx, row in df.iterrows():
        print(f"\n진행중: {idx + 1}/{len(df)} - {row['제목'][:30]}...")
        
        url = row['링크']
        detail = get_news_detail(url)
        
        # 기존 정보와 상세 정보 결합
        result = {
            '번호': row['번호'],
            '원본_제목': row['제목'],
            '링크': url,
            '타입': row['타입'],
            '수집시간': row['수집시간'],
            '카테고리': row['카테고리'],
            '뉴스_제목': detail['title'],
            '뉴스_내용': detail['content'],
            '기자명': detail['reporter'],
            '언론사': detail['press'],
            '발행일자': detail['publish_date'],
            '크롤링_상태': detail['status']
        }
        results.append(result)
        
        # 서버 부하 방지를 위한 대기
        time.sleep(random.uniform(0.5, 1.5))
    
    # 결과를 DataFrame으로 변환
    result_df = pd.DataFrame(results)
    
    # CSV 파일로 저장
    result_df.to_csv(output_csv_path, index=False, encoding='utf-8-sig')
    print(f"\n크롤링 완료! 결과가 {output_csv_path}에 저장되었습니다.")
    print(f"성공: {len(result_df[result_df['크롤링_상태'] == 'success'])}개")
    print(f"실패: {len(result_df[result_df['크롤링_상태'] != 'success'])}개")
    
    return result_df

def main(folder='data'):
    """메인 함수"""
    # 입력/출력 파일 경로 설정
    timestamp = datetime.now().strftime('%Y%m%d')
    input_csv = os.path.join(folder, f'naver_news_{timestamp}.csv')
    
    # 출력 파일명 생성 (타임스탬프 포함)
    output_csv = f"data/naver_news_detail_{timestamp}.csv"
    
    # data 폴더가 없으면 생성
    os.makedirs("data", exist_ok=True)
    
    # 입력 파일 존재 확인
    if not os.path.exists(input_csv):
        print(f"오류: {input_csv} 파일을 찾을 수 없습니다.")
        return
    
    print("=" * 60)
    print("네이버 뉴스 상세 정보 크롤링 시작")
    print("=" * 60)
    
    # 크롤링 실행
    result_df = crawl_news_details(input_csv, output_csv)
    
    print("\n" + "=" * 60)
    print("크롤링 작업이 완료되었습니다!")
    print("=" * 60)
    
    # 결과 미리보기
    print("\n[결과 미리보기]")
    print(result_df[['번호', '뉴스_제목', '기자명', '언론사', '발행일자']].head(10))

if __name__ == "__main__":
    main()

