import enum

from langchain_groq import ChatGroq

from .provider import Provider

class GROQ_LLMs(enum.Enum):
  llama3 = (enum.auto(), "llama-3.3-70b-versatile") 
  qwen = (enum.auto(), "qwen-qwq-32b")

class Provider_GROQ(Provider):
  def __init__(self, choiced_llm) -> None:
    self.model = ChatGroq(
        model=GROQ_LLMs[choiced_llm].value[1]
    )


