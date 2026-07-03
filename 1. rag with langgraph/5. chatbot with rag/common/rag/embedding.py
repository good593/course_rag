from langchain_openai import OpenAIEmbeddings


def get_embedding_of_openai(model="text-embedding-3-small"):
  return OpenAIEmbeddings(model=model)



