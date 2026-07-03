import streamlit as st 

def print_message(role, message):
  with st.chat_message(role):
    if not isinstance(message, str):
      message_placeholder = st.empty() # 깡통 프린트될 메세지 변수 선언
      messages = "" # 리턴할 전체 메세지 
      for msg in message: # message(제너레이터) for문을 이용해서 msg 받을 수 있음 
        messages += msg # 기존 전체 메세지에 새로운 msg 추가!!!
        message_placeholder.markdown(messages) # 화면에 표시하는 함수
    else:
      st.markdown(message)
      messages = message

  return messages

def print_history_message():
  # 이전 대화 내역을 화면에 표시
  for message in st.session_state.messages:
    print_message(message["role"], message["content"])


