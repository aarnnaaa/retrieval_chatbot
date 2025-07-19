import time
from llama_index.core.storage import StorageContext
from llama_index.core import load_index_from_storage
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core.settings import Settings

llm = Ollama(model="tinyllama", request_timeout=360.0, context_window=2048)
Settings.llm = llm
Settings.embed_model = OllamaEmbedding(model_name="tinyllama")

storage_context = StorageContext.from_defaults(persist_dir="storage")
index = load_index_from_storage(storage_context)
query_engine = index.as_query_engine(similarity_top_k=10)
def detect_intent_with_llamaindex(user_query: str) -> str:
    intent_prompt = f"""
You are an intent classifier for a courier assistant.

Classify the user's message into one of the following intents:
- shipping_info
- delivery_updates
- fax_queries
- services_info
- general_inquiry

Message: "{user_query}"

Only return one of the intent names above. Do not explain.
Intent:
"""

    response = query_engine.query(intent_prompt)
    return str(response).strip().lower()

while True:
    user_query = input("\nyou: ")
    if user_query.strip().lower() == "exit":
        print("bye")
        break
    intent = detect_intent_with_llamaindex(user_query)
    print(f"[intent recognized: {intent}]")

    modified_query = f"user question about {intent}: {user_query}"

    print("\ncourier bot: ", end="")
    response = query_engine.query(modified_query)
    for word in str(response).split():
        print(word, end=' ', flush=True)
    print()
