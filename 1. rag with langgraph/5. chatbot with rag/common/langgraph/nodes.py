
from langgraph.prebuilt import create_react_agent

from common.langgraph.states import State
from common.langgraph.model import get_model_of_generation, get_model_of_evaluation, get_model_of_web_search
from common.rag.retriever import VectorDB

# 문서 검색
def retrieve_of_reg(state:State):
    print("==== [RETRIEVE] ====")
    question = state["question"]

    # 검색 수행
    documents = VectorDB().get_retriever().invoke(question)
    return {"documents": documents}

# 답변 생성
def generate_of_reg(state:State):
    print("==== [GENERATE] ====")
    question = state["question"]
    documents = state["documents"]

    # RAG 생성
    generation = get_model_of_generation().invoke({"context": documents, "question": question})
    print(f"generation: {generation}")
    return {"generation": generation}


# 검색된 문서의 관련성 평가
def evaluate_of_reg(state:State):
    print("==== [GRADE DOCUMENTS] ====")
    question = state["question"]
    documents = state["documents"]

    # 각 문서 점수 평가
    filtered_docs = []
    for d in documents:
        score = get_model_of_evaluation().invoke(
            {"question": question, "document": d.page_content}
        )
        grade = score.binary_score
        if grade == "yes":
            print("==== GRADE: DOCUMENT RELEVANT ====")
            filtered_docs.append(d)
        else:
            print("==== GRADE: DOCUMENT NOT RELEVANT ====")
            continue
    return {"documents": filtered_docs}


def web_search(state:State):
    question = state["question"]

    generation = get_model_of_web_search().invoke(
            {"question": question}
        )
    
    print(f"generation: {generation}")
    return {"generation": generation}

