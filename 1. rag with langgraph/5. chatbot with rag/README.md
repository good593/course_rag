# RAG 기반 챗봇 (LangGraph)

이 프로젝트는 LangGraph를 사용하여 RAG(Retrieval-Augmented Generation) 기반 챗봇을 구현한 것입니다. 사용자의 질문에 대해 관련 문서를 검색하고, 필요시 웹 검색을 통해 답변을 생성합니다.

## 🚀 주요 기능

- **RAG 시스템**: 벡터 데이터베이스를 활용한 문서 검색
- **웹 검색**: 관련 문서가 없을 때 웹 검색을 통한 답변 생성
- **Streamlit UI**: 사용자 친화적인 웹 인터페이스
- **다중 LLM 지원**: OpenAI, Groq 등 다양한 LLM 제공자 지원
- **LangGraph 워크플로우**: 구조화된 대화 처리 파이프라인

## 📁 프로젝트 구조

```
chatbot with rag/
├── chatbot.py              # Streamlit 메인 애플리케이션
├── studio.py               # LangGraph 실행 파일
├── langgraph.json          # LangGraph 설정 파일
├── pyproject.toml          # 프로젝트 설정
├── requirements.txt        # 의존성 목록
├── common/
│   ├── langgraph/          # LangGraph 관련 모듈
│   │   ├── graph.py        # 워크플로우 그래프 정의
│   │   ├── model.py        # LLM 모델 설정
│   │   ├── nodes.py        # 워크플로우 노드들
│   │   ├── prompt.py       # 프롬프트 템플릿
│   │   ├── states.py       # 상태 관리
│   │   └── tools.py        # 도구들
│   ├── llm/                # LLM 제공자 모듈
│   │   ├── call_provider.py
│   │   ├── groq.py
│   │   ├── openai.py
│   │   ├── provider.py
│   │   └── rag.py
│   ├── rag/                # RAG 시스템
│   │   ├── data/           # 문서 데이터
│   │   │   ├── SPRI_AI_Brief_2023년12월호_F.pdf
│   │   │   └── nlp-keywords.txt
│   │   ├── embedding.py    # 임베딩 처리
│   │   ├── loader.py       # 문서 로더
│   │   └── retriever.py    # 검색기
│   └── screen/             # UI 관련 모듈
│       ├── constant.py
│       ├── display.py
│       ├── history.py
│       ├── input.py
│       └── utils.py
```

## 🛠️ 설치 및 실행

### 1. 의존성 설치

```bash
uv venv .venv
source .venv/bin/activate  # Linux/Mac
# 또는
.venv\Scripts\activate     # Windows

uv pip install -r requirements.txt
```

### 2. 환경 변수 설정

`.env.example`을 참고해서 `.env` 파일을 생성하고 필요한 API 키를 설정하세요:

```env
# To separate your traces from other application
LANGSMITH_API_KEY=""
LANGSMITH_PROJECT=""

# Add API keys for connecting to LLM providers, data sources, and other integrations here
OPENAI_API_KEY=""
GROQ_API_KEY=""
TAVILY_API_KEY=""
```

### 3. 애플리케이션 실행

#### 예제 시나리오 
- RAG 테스트
```test
삼성전자가 개발한 생성AI 에 대해 설명하세요.
```
- TAVILY 테스트 
```test
LangChain에 대해서 설명하세요.
```

#### Streamlit 챗봇 실행
```bash
streamlit run chatbot.py
```

#### LangGraph Studio 실행
```bash
uv pip install -e .

langgraph dev --allow-blocking
```

## 🔧 워크플로우

이 챗봇은 다음과 같은 워크플로우로 동작합니다:

1. **Retrieve**: 사용자 질문에 관련된 문서를 벡터 데이터베이스에서 검색
2. **Evaluate**: 검색된 문서의 관련성을 평가
3. **Generate**: 관련 문서가 있으면 이를 기반으로 답변 생성
4. **Web Search**: 관련 문서가 없으면 웹 검색을 통해 답변 생성

## 📚 데이터

프로젝트에는 다음 문서들이 포함되어 있습니다:
- `SPRI_AI_Brief_2023년12월호_F.pdf`: AI 관련 브리프 문서

## 🎯 사용법

1. Streamlit 애플리케이션을 실행합니다
2. 채팅 인터페이스에서 질문을 입력합니다
3. 시스템이 관련 문서를 검색하고 답변을 생성합니다
4. 필요시 웹 검색을 통해 추가 정보를 제공합니다

## 🔌 지원하는 LLM 제공자

- OpenAI (GPT 모델)
- Groq (고속 추론)

