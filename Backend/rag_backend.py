import os
from dotenv import load_dotenv
load_dotenv()

from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    ServiceContext,
    StorageContext,
    load_index_from_storage,
)
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
INDEX_DIR = "index"

def build_index(input_file: str = "data", output_dir: str = INDEX_DIR):
    try:
        documents = SimpleDirectoryReader(input_files=[input_file]).load_data()

        embed_model = OpenAIEmbedding(model="text-embedding-3-small", api_key=OPENAI_API_KEY)
        llm = OpenAI(model="gpt-3.5-turbo", api_key=OPENAI_API_KEY)
        service_context = ServiceContext.from_defaults(embed_model=embed_model, llm=llm)

        index = VectorStoreIndex.from_documents(documents, service_context=service_context)
        index.storage_context.persist(persist_dir=output_dir)
    except Exception as e:
        print(f"Error in build_index: {e}")
        import traceback
        traceback.print_exc()
        raise

def load_index(persist_dir: str = INDEX_DIR):
    try:
        embed_model = OpenAIEmbedding(model="text-embedding-3-small", api_key=OPENAI_API_KEY)
        llm = OpenAI(model="gpt-3.5-turbo", api_key=OPENAI_API_KEY)
        service_context = ServiceContext.from_defaults(embed_model=embed_model, llm=llm)

        storage_context = StorageContext.from_defaults(persist_dir=persist_dir)
        return load_index_from_storage(storage_context, service_context=service_context)
    except Exception as e:
        print(f"Error in load_index: {e}")
        import traceback
        traceback.print_exc()
        raise
