from llama_index.core.storage import StorageContext
from llama_index.core import load_index_from_storage
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core.settings import Settings
import time


llm = Ollama(
    model="tinyllama",
    request_timeout=360.0,
    context_window=2048
)
Settings.llm = llm
Settings.embed_model = OllamaEmbedding(model_name="tinyllama")

storage_context = StorageContext.from_defaults(persist_dir="storage")  # Correct path
index = load_index_from_storage(storage_context)
query_engine = index.as_query_engine(similarity_top_k=10)

def detect_intent_with_llamaindex(user_query: str) -> str:
    intent_prompt = f"""
    You are an intent classifier for a documentation support assistant.

    Given the user message below, classify it into one of the following intents:
    - refund
    - cancel subscription
    - damaged item
    - return_item
    - general inquiry

    User message: "{user_query}"

    Just output one of the above intent labels.
    Intent:
    """
    response = query_engine.query(intent_prompt)
    return str(response).strip().lower()
print("Welcome to DocBot! Type 'exit' to quit.\n")

while True:
    user_query = input("\nAsk your question: ")
    if user_query.strip().lower() == "exit":
        print("Goodbye!")
        break

    intent = detect_intent_with_llamaindex(user_query)
    print(f"[Intent recognized: {intent}]")

    # Modify query based on intent
    if intent == "cancel subscription":
        modified_query = f"User wants to cancel subscription. {user_query}"
    elif intent == "refund":
        modified_query = f"User is asking about refund. {user_query}"
    elif intent == "return_item":
        modified_query = f"User wants to return an item. {user_query}"
    elif intent == "damaged item":
        modified_query = f"User received a damaged item. {user_query}"
    else:
        modified_query = user_query

    print("\nAnswer:")
    response = query_engine.query(modified_query)

    for word in str(response).split():
        print(word, end=' ', flush=True)
        time.sleep(0.05)

    # print("\n\n sources: ")
    # print("\n\nSources used:")
    # for i, source_node in enumerate(response.source_nodes):
    #     metadata = source_node.metadata
    #     source_info = metadata.get("source", "unknown")
    #     print(f"[{i+1}] Source: {source_info}")
    #     print(source_node.text[:200] + "...\n")
