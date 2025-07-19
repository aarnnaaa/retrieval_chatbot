from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core.settings import Settings
import os


Settings.llm = Ollama(model="tinyllama")
Settings.embed_model = OllamaEmbedding(model_name="tinyllama")  
docs_path2 = "/Users/aarnatejwani/Desktop/retrieval_chatbot/retrieval_docs2"
docs_path = "/Users/aarnatejwani/Desktop/retrieval_chatbot/initdb"
documents = SimpleDirectoryReader(docs_path).load_data()
docs = SimpleDirectoryReader(docs_path2).load_data()
all_docs = documents + docs
index = VectorStoreIndex.from_documents(docs)
index.storage_context.persist(persist_dir="./storage")
print("Index built and saved to ./storage")