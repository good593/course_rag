from langchain_community.document_loaders import PyMuPDFLoader

def get_docs_from_loader(pdf_path= 'common/rag/data/SPRI_AI_Brief_2023년12월호_F.pdf'):
  loader = PyMuPDFLoader(pdf_path)
  return loader.load()






