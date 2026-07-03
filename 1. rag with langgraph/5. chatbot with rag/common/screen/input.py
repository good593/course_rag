import streamlit as st

from common.llm.call_provider import PROVIDER_TYPE


def choice_provider():
  choiced_provider = st.sidebar.selectbox(
    label="LLM 제공자를 선택해주세요.",
    options=list(PROVIDER_TYPE.__members__)
  )

  return choiced_provider

def choice_llms(choiced_provider:str):
  choiced_llm = st.sidebar.selectbox(
    label="모델을 선택해주세요.",
    options=list(PROVIDER_TYPE[choiced_provider].value[2].__members__)
  )

  return choiced_llm

def get_prompt():
  return st.chat_input("무엇이든지 물어봐주세요.")
