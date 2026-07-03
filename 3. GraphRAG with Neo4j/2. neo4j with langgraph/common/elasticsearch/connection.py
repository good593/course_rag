from elasticsearch import Elasticsearch
import warnings

# SSL 경고 무시 (개발 환경용)
warnings.filterwarnings('ignore')

def create_client(hosts:list=["http://localhost:9200"], id:str="elastic", pw:str="changeme123!"):
    """개발 환경에서 손쉽게 재사용할 수 있는 Elasticsearch 클라이언트 생성기"""
    es_client = Elasticsearch(
        hosts=hosts,                # 리스트 형태로, scheme 포함
        basic_auth=(id, pw),        # 인증 정보 (보안 활성화 시 필수)
        verify_certs=False,         # SSL 인증서 검증 여부 (개발 환경에서는 False, 운영 환경에서는 True 권장)
        ssl_show_warn=False,        # SSL 비검증 시 발생하는 경고 메시지 숨김
        request_timeout=30,         # 요청 타임아웃(초). 기본값보다 넉넉하게 설정 가능
        max_retries=3,              # 요청 실패 시 재시도 횟수
        retry_on_timeout=True,      # 타임아웃 발생 시 재시도 활성화
        # 호환성 헤더 비활성화 (개발 환경용)
        headers={"accept": "application/json", "content-type": "application/json"}
    )
    
    # 연결 확인
    if es_client.ping():
        print("Elasticsearch 연결 성공!")
        print()
        
        # 클러스터 정보
        info = es_client.info()
        print(f"버전: {info['version']['number']}")
        print(f"클러스터 이름: {info['cluster_name']}")
        print(f"노드 이름: {info['name']}")
        return es_client
    else:
        # ping 자체가 실패하면 세부 예외를 상위 호출부에서 확인하도록 알림만 출력
        print("Elasticsearch 연결 실패 (ping 실패)")


if __name__ == "__main__":
    create_client()