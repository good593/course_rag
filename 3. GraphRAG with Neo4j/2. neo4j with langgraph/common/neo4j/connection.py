from neo4j import GraphDatabase
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings

from .query_templates import CypherQueryTemplates

class Singleton(type):
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        # 동일한 인스턴스를 재사용하여 연결 수를 최소화
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Neo4jConnection(metaclass=Singleton):
    """Neo4j 데이터베이스 연결 및 작업을 위한 클래스"""
    
    def __init__(self, uri, user, password, embedding_model="qwen3-embedding:0.6b"):
        # 드라이버와 임베딩 모델은 비용이 크므로 생성 시점에 초기화
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.embedding_model = OllamaEmbeddings(model=embedding_model)
        print("Neo4j 연결 성공!")

    
    def close(self):
        if self.driver is not None:
            # 세션 풀 리소스를 명시적으로 해제
            self.driver.close()
            print("Neo4j 연결 종료")
    
    def execute_query(self, query:str, parameters:dict=None) -> list:
        # session.run을 래핑하여 간단한 리스트 형태로 결과 반환
        with self.driver.session() as session:
            result = session.run(query, parameters)
            return [record for record in result]
           

    def execute_query_templates(self, template:str, parameters:dict=None) -> list:
        if template not in CypherQueryTemplates.__members__:
            raise Exception("[Neo4jConnection] 올바른 template이 아닙니다.")

        # Enum 기반 템플릿을 통해 최종 Cypher 쿼리 생성
        cypher_query = CypherQueryTemplates[template].build(**parameters)
        results = self.execute_query(cypher_query)

        documents = []
        for result in results:
            # 결과 레코드를 LangChain Document와 score 페어로 변환
            doc = Document(
                page_content=f"[뉴스 제목] {result['title']}\n[뉴스 내용]\n{result['content']}",
                metadata={
                    "publisher_name":result['publisher_name'],
                    "reporter_name":result['reporter_name'],
                    "publish_date":result['publish_date'],
                    "source":result['news_link'],
                }
            )
            documents.append((doc, result['score']))

        return documents

