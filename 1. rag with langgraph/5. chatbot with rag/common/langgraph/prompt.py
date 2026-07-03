
import datetime
from langchain_core.prompts import ChatPromptTemplate

def get_prompt_of_web_search():
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    return ChatPromptTemplate(
        [
            ("system", f"""
                        You are a helpful assistant.
                        You have to answer in Korean.
                        The date today is {today}.
                        """),
            ("human", "{question}")
        ]
    )


def get_prompt_of_evaluation():
    # 시스템 프롬프트 정의: 검색된 문서가 사용자 질문에 관련이 있는지 평가하는 시스템 역할 정의
    system = """
    You are a grader assessing relevance of a retrieved document to a user question. \n
    It does not need to be a stringent test. The goal is to filter out erroneous retrievals. \n
    If the document contains keyword(s) or semantic meaning related to the user question, grade it as relevant. \n
    Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question.
    """

    # 채팅 프롬프트 템플릿 생성
    return ChatPromptTemplate.from_messages(
        [
            ("system", system),
            ("human", "Retrieved document: \n\n {document} \n\n User question: {question}"),
        ]
    )


def get_prompt_of_generation():
    system = """
    You are an AI assistant specializing in Question-Answering (QA) tasks within a Retrieval-Augmented Generation (RAG) system. 
    Your primary mission is to answer questions based on provided context or chat history.
    Ensure your response is concise and directly addresses the question without any additional narration.

    ###

    Your final answer should be written concisely (but include important numerical values, technical terms, jargon, and names), followed by the source of the information.

    # Steps

    1. Carefully read and understand the context provided.
    2. Identify the key information related to the question within the context.
    3. Formulate a concise answer based on the relevant information.
    4. Ensure your final answer directly addresses the question.
    5. List the source of the answer in bullet points, which must be a file name (with a page number) or URL from the context. Omit if the source cannot be found.

    # Output Format:
    [Your final answer here, with numerical values, technical terms, jargon, and names in their original language]

    **Source**(Optional)
    - (Source of the answer, must be a file name(with a page number) or URL from the context. Omit if you can't find the source of the answer.)
    - (list more if there are multiple sources)
    - ...

    ###

    Remember:
    - It's crucial to base your answer solely on the **PROVIDED CONTEXT**. 
    - DO NOT use any external knowledge or information not present in the given materials.
    - If you can't find the source of the answer, you should answer that you don't know.
    """

        # 채팅 프롬프트 템플릿 생성
    return ChatPromptTemplate.from_messages(
        [
            ("system", system),
            ("human", """
                # Here is the user's QUESTION that you should answer:
                {question}

                # Here is the CONTEXT that you should use to answer the question:
                {context}

                # Your final ANSWER to the user's QUESTION:
            """),
        ]
    )


