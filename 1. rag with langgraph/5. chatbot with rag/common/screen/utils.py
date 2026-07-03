import streamlit as st

from dotenv import load_dotenv 

from common.screen.history import init_history
from common.screen.display import print_history_message
from common.screen.input import choice_provider, choice_llms

from common.llm.call_provider import get_provider


def init_page(is_clear:bool=False):
  # .env 파일에 선언한 변수를 환경변수에 등록하는 함수
  load_dotenv() 
  # history 초기화 
  init_history(is_clear)  



def init_display():
  # 이력 데이터를 프린트
  print_history_message()

  if st.sidebar.button("챗봇 메세지 클린징", icon="😃"):
    init_history(is_clear=True)
    st.cache_resource.clear()
    st.rerun()

  # provider 리스트 
  choiced_provider = choice_provider()
  # 선택한 provider가 제공하는 모델 리스트
  choiced_llm = choice_llms(choiced_provider)

  return get_provider(choiced_provider, choiced_llm)
