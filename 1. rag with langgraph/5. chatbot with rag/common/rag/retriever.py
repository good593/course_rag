from langchain_community.vectorstores import FAISS

from .embedding import get_embedding_of_openai
from .loader import get_docs_from_loader

class Singleton(type):
	_instances = {}

	def __call__(cls, *args, **kwargs):
		if cls not in cls._instances:
			cls._instances[cls] = super(Singleton, cls)\
				.__call__(*args, **kwargs)
		return cls._instances[cls]

class VectorDB(metaclass=Singleton):
    
    def __init__(self):
        self.retriever = self.__create_vectordb()

    def __create_vectordb(self):
        db = FAISS.from_documents(
        documents=get_docs_from_loader(), embedding=get_embedding_of_openai())
        return db.as_retriever()

    def get_retriever(self):
        return self.retriever

