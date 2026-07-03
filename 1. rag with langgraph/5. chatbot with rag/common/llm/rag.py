import enum

from common.langgraph.graph import get_graph

from .provider import Provider_RAG

class RAG_LLMs(enum.Enum):
  삼성AI_RAG = (enum.auto(), "llama-3.3-70b-versatile")

class Provider_RAG(Provider_RAG):
  def __init__(self, choiced_llm) -> None:
    # LangGraph 모델 사용
    self.model = get_graph()

