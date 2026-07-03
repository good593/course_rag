import streamlit as st 

from common.screen.history import add_history
from common.screen.display import print_message
from common.screen.input import get_prompt
from common.screen.constant import ROLE_TYPE
from common.screen.utils import init_page, init_display

def app():
  st.title("Chatbot")

  # 화면 초기화  
  provider = init_display()
  # 사용자 입력
  prompt = get_prompt()

  if prompt is not None:
    # 사용자 메시지를 세션 상태에 추가
    add_history(ROLE_TYPE.user, prompt)
    # 사용자 메시지 표시
    print_message(ROLE_TYPE.user.name, prompt)
    
    # AI 응답 요청
    generator = provider()
    # AI 응답 표시
    assistant_message = print_message(
      ROLE_TYPE.assistant.name
      , generator)
    
    add_history(ROLE_TYPE.assistant, assistant_message)

if __name__=="__main__":
  init_page()
  app() 
