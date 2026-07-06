---
style: |
  img {
    display: block;
    float: none;
    margin-left: auto;
    margin-right: auto;
  }
marp: true
paginate: true
---
# RAG 서비스 평가

이 폴더는 RAGAS를 이용해 RAG 서비스 평가 데이터셋을 만들고, RAG 답변을 생성한 뒤, 생성 품질과 검색 품질을 평가하는 강의자료입니다.

---
## 학습 흐름

1. `1. RAGAs 이용해서 평가 데이터셋 생성.ipynb`
   - PDF 문서를 로드하고 RAGAS 테스트셋을 생성합니다.
   - 결과를 `data/evaluation_questions_for_ragas.csv`에 저장합니다.

2. `2. RAG 답변 데이터셋 생성.ipynb`
   - PDF를 Chroma 벡터 DB에 저장합니다.
   - `data/evaluation_questions_for_ragas.csv`의 질문을 RAG 체인에 넣어 답변과 검색 문맥을 생성합니다.
   - RAGAS 0.3.9 평가 입력 컬럼명에 맞춰 `data/evaluation_answers_from_rag.csv`를 저장합니다.

3. `3. RAGAs를 이용해서 RAG 평가.ipynb`
   - `data/evaluation_answers_from_rag.csv`를 로드합니다.
   - `answer_relevancy`, `faithfulness`, `context_recall`, `context_precision`을 계산합니다.
   - 평가 점수를 하나의 표로 합치고, 낮은 점수 샘플을 확인해 검색 문제와 생성 문제를 구분합니다.
   - 결과를 `data/evaluation_scores_from_ragas.csv`로 저장합니다.

## 실행 준비

Python 버전은 `.python-version`과 `pyproject.toml`에 맞춰 3.12를 사용합니다.

```powershell
uv sync
```

`.env.example`을 참고해 `.env` 파일에 OpenAI API 키를 입력합니다.

```text
OPENAI_API_KEY="sk-..."
```

2번 노트북은 로컬 Ollama 모델을 사용합니다. Ollama가 설치되어 있어야 하며, 아래 모델을 미리 내려받습니다.

```powershell
ollama pull gemma3:4b
```

1번과 3번 노트북은 OpenAI API를 사용하므로 실행 시간과 API 비용이 발생할 수 있습니다. 강의 중에는 기본 데이터셋 10건으로 먼저 흐름을 확인한 뒤, 시간이 남으면 `testset_size`를 늘려 평가 표본을 확장합니다.

## RAGAS 0.3.9 평가 컬럼

이 자료에서는 RAGAS 0.3.9 기준 컬럼명을 사용합니다.

| 컬럼명 | 의미 |
| --- | --- |
| `user_input` | 평가 질문 |
| `response` | RAG 체인이 생성한 답변 |
| `retrieved_contexts` | RAG 체인이 검색한 문맥 리스트 |
| `reference` | 기준 정답 |
| `reference_contexts` | 기준 정답을 만들 때 사용된 참조 문맥 |

예전 예제에서 자주 보이는 `question`, `answer`, `contexts`, `ground_truth` 컬럼명은 RAGAS 0.3.9에서 평가 입력으로 자동 인식되지 않을 수 있으므로 사용하지 않습니다.

## 평가 결과 해석

평가 점수는 단일 평균만 보고 끝내지 않습니다. 낮은 점수 샘플을 직접 열어 보고, 어떤 단계가 병목인지 분리해서 판단합니다.

| 관찰되는 패턴 | 의심할 문제 | 먼저 확인할 것 |
| --- | --- | --- |
| `context_recall`이 낮음 | 정답 근거가 검색 결과에 충분히 들어오지 않음 | chunk 크기, overlap, retriever `k`, embedding 모델 |
| `context_precision`이 낮음 | 관련 없는 문맥이 상위에 많이 섞임 | retriever `k`, MMR, metadata 필터, 문서 분할 방식 |
| `faithfulness`가 낮음 | 답변이 검색 문맥 밖의 내용을 말함 | 프롬프트의 근거 사용 지시, LLM temperature, 답변 길이 |
| `answer_relevancy`가 낮음 | 질문에 직접 답하지 않거나 불필요한 내용이 많음 | 프롬프트, 출력 형식, 질문 전처리 |

강의에서는 `data/evaluation_answers_from_rag.csv` 안의 실패 사례를 함께 봅니다. 예를 들어 FTC 질문은 참조 문맥에 정답이 있지만 RAG 답변이 정보 부족처럼 시작하므로, 점수와 사람이 보는 오류 유형이 어떻게 연결되는지 설명하기 좋습니다.

## 확장 실습 아이디어

- `testset_size`를 10에서 30 이상으로 늘려 점수 분포를 비교합니다.
- `SingleHopSpecificQuerySynthesizer` 외에 multi-hop, 조건형, 도메인 외 질문을 추가해 더 까다로운 평가셋을 만듭니다.
- `retriever = vectorstore.as_retriever(search_kwargs={"k": 2})`, `k=4`, `k=8`처럼 검색 개수를 바꿔 `context_recall`과 `context_precision`의 trade-off를 확인합니다.
- `chunk_size`와 `chunk_overlap`을 바꿔 같은 질문셋에서 평가 점수가 어떻게 달라지는지 비교합니다.
- 전처리 전후의 문맥을 비교해 특수문자 제거가 평가에 주는 영향을 확인합니다.
