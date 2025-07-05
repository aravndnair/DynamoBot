import os
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, StorageContext, load_index_from_storage
from llama_index.core.settings import Settings
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.langchain import LangChainLLM
from langchain_openai import ChatOpenAI

# Configure embeddings and LLM
Settings.embed_model = OpenAIEmbedding()
Settings.llm = LangChainLLM(llm=ChatOpenAI(temperature=0.1, model="gpt-3.5-turbo"))

def build_index(file_path, index_dir):
    documents = SimpleDirectoryReader(input_files=[file_path]).load_data()
    index = VectorStoreIndex.from_documents(documents)
    index.storage_context.persist(index_dir)

def query_index(question, index_dir):
    storage_context = StorageContext.from_defaults(persist_dir=index_dir)
    index = load_index_from_storage(storage_context)
    query_engine = index.as_query_engine()
    response = query_engine.query(question)
    return str(response)
