
from langgraph.graph import END, StateGraph, START

from common.langgraph.states import State
from common.langgraph.nodes import retrieve_of_reg, generate_of_reg, evaluate_of_reg, web_search

# 답변 생성 여부 결정
def decide_to_generate(state:State):
    print("==== [ASSESS GRADED DOCUMENTS] ====")
    state["question"]
    filtered_documents = state["documents"]

    if not filtered_documents:
        return "web_search"
    else:
        # 관련 문서가 있는 경우 답변 생성
        print("==== [DECISION: GENERATE] ====")
        return "generate"


def get_graph():
    workflow = StateGraph(State)

    workflow.add_node("retrieve", retrieve_of_reg)
    workflow.add_node("evaluate", evaluate_of_reg)
    workflow.add_node("generate", generate_of_reg)
    workflow.add_node("web_search", web_search)

    # 엣지 정의
    workflow.add_edge(START, "retrieve")
    workflow.add_edge("retrieve", "evaluate")
    workflow.add_edge("web_search", END)
    workflow.add_edge("generate", END)

    # 문서 평가 노드에서 조건부 엣지 추가
    workflow.add_conditional_edges(
        "evaluate",
        decide_to_generate,
        {
            "web_search": "web_search",
            "generate": "generate",
        },
    )

    return workflow.compile()



