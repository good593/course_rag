import enum

from langchain_openai import OpenAI

from .provider import Provider

class OpenAI_LLMs(enum.Enum):
  gpt_4o_mini = (enum.auto(), "gpt-4o-mini") 
  gpt_4o = (enum.auto(), "gpt-4o") 

class Provider_OpenAI(Provider):
  def __init__(self, choiced_llm) -> None:
    self.model = OpenAI(
        model=OpenAI_LLMs[choiced_llm].value[1]
    )


