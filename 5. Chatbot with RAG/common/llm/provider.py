import time
import streamlit as st

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import HumanMessage

from common.screen.constant import ROLE_TYPE, HISTORY_INFO

class Provider:

  def __call__(self):
    
    prompts = [] 
    for msg in st.session_state.messages[:-1]:
      prompts.append(tuple(msg.values()))
      
    prompts += [(ROLE_TYPE.user.name, "{user_input}")] # 사용자의 메세지 입력 프론프트
    chat_prompt = ChatPromptTemplate.from_messages(prompts)

    # 체인 생성
    chain = chat_prompt | self.model | StrOutputParser()

    # 모델 답변 
    for token in chain.stream({"user_input": st.session_state.messages[-1][HISTORY_INFO.content.name]}):
      yield token
      time.sleep(0.05) 

class Provider_RAG:

  def __call__(self):
    config = RunnableConfig(recursion_limit=10)

    # 모델 답변 
    answer = self.model.invoke({"question": st.session_state.messages[-1][HISTORY_INFO.content.name]},
                                    config=config)
    for token in answer['generation']:
      yield token
      time.sleep(0.05) 
