from langchain_community.tools import TavilySearchResults


def get_web_search():
    # 최대 검색 결과를 3으로 설정
    return TavilySearchResults(
        max_results=5,
        include_answer=True,
        include_raw_content=True,
        include_domains=["github.io", "wikidocs.net"]
    )


