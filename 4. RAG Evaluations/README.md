# RAG 서비스 평가

이 폴더는 RAGAS를 이용해 RAG 서비스 평가 데이터셋을 만들고, RAG 답변을 생성한 뒤, 생성 품질과 검색 품질을 평가하는 강의자료입니다.

## 학습 흐름

1. `1. RAGAs 이용해서 평가 데이터셋 생성.ipynb`
   - PDF 문서를 로드하고 RAGAS 테스트셋을 생성합니다.
   - 결과를 `data/evaluation_ragas.csv`에 저장합니다.

2. `2. RAG 답변 데이터셋 생성.ipynb`
   - PDF를 Chroma 벡터 DB에 저장합니다.
   - `data/evaluation_ragas.csv`의 질문을 RAG 체인에 넣어 답변과 검색 문맥을 생성합니다.
   - RAGAS 0.3.9 평가 입력 컬럼명에 맞춰 `data/evaluation_ragas_with_answer.csv`를 저장합니다.

3. `3. RAGAs를 이용해서 RAG 평가.ipynb`
   - `data/evaluation_ragas_with_answer.csv`를 로드합니다.
   - `answer_relevancy`, `faithfulness`, `context_recall`, `context_precision`을 계산합니다.

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
