# Qdrant Docker Compose 사용 가이드

## 목차
1. [시작하기](#시작하기)
2. [서비스 관리](#서비스-관리)
3. [연결 정보](#연결-정보)
4. [데이터 백업](#데이터-백업)
5. [문제 해결](#문제-해결)

## 시작하기

### 1. Qdrant 시작

```bash
# Qdrant 컨테이너 시작 (백그라운드 실행)
docker-compose up -d

# 로그 확인
docker-compose logs -f qdrant
```

### 2. 서비스 상태 확인

```bash
# 컨테이너 상태 확인
docker-compose ps

# 헬스체크 확인
curl http://localhost:6333/healthz
```

### 3. Web UI 접속

브라우저에서 다음 주소로 접속:
- **Dashboard**: http://localhost:6333/dashboard

## 서비스 관리

### Qdrant 중지

```bash
# 컨테이너 중지 (데이터 유지)
docker-compose stop

# 컨테이너 중지 및 제거 (데이터는 볼륨에 유지)
docker-compose down
```

### Qdrant 재시작

```bash
# 서비스 재시작
docker-compose restart
```

### 완전 삭제 (데이터 포함)

```bash
# 컨테이너, 네트워크, 볼륨 모두 삭제
docker-compose down -v

# 로컬 스토리지 폴더 삭제
rm -rf qdrant_storage qdrant_snapshots
```

## 🔌 연결 정보

### Python에서 연결

```python
from qdrant_client import QdrantClient

# 방법 1: 로컬 Docker 연결
client = QdrantClient(host="localhost", port=6333)

# 방법 2: URL 형식
client = QdrantClient(url="http://localhost:6333")

# API 키 설정한 경우
# client = QdrantClient(
#     url="http://localhost:6333",
#     api_key="your-secret-api-key"
# )
```

### LangChain에서 연결

```python
from langchain_qdrant import QdrantVectorStore
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings()

vectorstore = QdrantVectorStore.from_documents(
    documents=docs,
    embedding=embeddings,
    url="http://localhost:6333",
    collection_name="my_collection",
)
```

## 데이터 백업

### 스냅샷 생성

```bash
# API를 통한 스냅샷 생성
curl -X POST "http://localhost:6333/collections/{collection_name}/snapshots"

# 생성된 스냅샷 확인
curl "http://localhost:6333/collections/{collection_name}/snapshots"
```

### 백업 파일 위치

- 벡터 데이터: `./qdrant_storage/`
- 스냅샷: `./qdrant_snapshots/`

이 폴더들을 정기적으로 백업하세요!

## 보안 설정 (옵션)

### API 키 설정

`docker-compose.yml` 파일에서 다음 환경 변수의 주석을 해제하고 수정:

```yaml
environment:
  # 전체 권한 API 키
  - QDRANT__SERVICE__API_KEY=your-secret-api-key
  
  # 읽기 전용 API 키
  - QDRANT__SERVICE__READ_ONLY_API_KEY=your-read-only-key
```

그 후 재시작:

```bash
docker-compose down
docker-compose up -d
```

## 문제 해결

### 포트 충돌

포트가 이미 사용 중인 경우 `docker-compose.yml`에서 포트 번호 변경:

```yaml
ports:
  - "6333:6333"  # 왼쪽 숫자를 다른 포트로 변경 (예: 7333:6333)
  - "6334:6334"
```

### 로그 확인

```bash
# 실시간 로그 보기
docker-compose logs -f qdrant

# 최근 100줄 보기
docker-compose logs --tail=100 qdrant
```

### 컨테이너가 시작되지 않는 경우

```bash
# 이미지 재다운로드
docker-compose pull

# 캐시 없이 재빌드
docker-compose up -d --force-recreate
```

### 디스크 공간 확인

```bash
# 볼륨 크기 확인
du -sh qdrant_storage
du -sh qdrant_snapshots
```

## 성능 모니터링

### 메모리 및 CPU 사용량 확인

```bash
# 실시간 리소스 사용량 확인
docker stats qdrant
```

### 컬렉션 정보 확인

```bash
# 모든 컬렉션 목록
curl http://localhost:6333/collections

# 특정 컬렉션 정보
curl http://localhost:6333/collections/{collection_name}
```

## 추가 리소스

- [Qdrant 공식 문서](https://qdrant.tech/documentation/)
- [Qdrant API 레퍼런스](https://qdrant.github.io/qdrant/redoc/index.html)
- [LangChain Qdrant 통합](https://python.langchain.com/docs/integrations/vectorstores/qdrant)

## 팁

1. **프로덕션 환경**: API 키를 반드시 설정하세요
2. **백업**: 정기적으로 스냅샷을 생성하고 외부에 저장하세요
3. **모니터링**: 메모리 사용량을 주기적으로 확인하세요
4. **리소스**: 데이터가 많아지면 메모리 제한을 늘리세요

