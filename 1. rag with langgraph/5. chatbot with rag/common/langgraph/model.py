from pydantic import BaseModel, Field

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

from .prompt import get_prompt_of_evaluation, get_prompt_of_generation, get_prompt_of_web_search
from .tools import get_web_search

def get_model(name="gpt-4o-mini"):
  return ChatOpenAI(model=name, temperature=0)


class Answer_of_evaluation(BaseModel):
  """A binary score to determine the relevance of the retrieved documents."""

  # 문서가 질문에 관련이 있는지 여부를 'yes' 또는 'no'로 나타내는 필드
  binary_score: str = Field(
      description="Documents are relevant to the question, 'yes' or 'no'"
  )

def get_model_of_evaluation():
  llm = get_model().with_structured_output(Answer_of_evaluation)

  return get_prompt_of_evaluation() | llm


def get_model_of_generation():
  return get_prompt_of_generation() | get_model() | StrOutputParser()


def get_model_of_web_search():
  llm = get_model("gpt-4o")
  return get_prompt_of_web_search() | llm.bind_tools([get_web_search()]) | StrOutputParser()
  

