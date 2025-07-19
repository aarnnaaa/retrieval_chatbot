import sqlite3
import time
import re
from llama_index.core import load_index_from_storage, StorageContext
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core.settings import Settings
 Settings.llm = Ollama(model="tinyllama", request_timeout=120.0)
Settings.embed_model = OllamaEmbedding(model="tinyllama")

storage_context = StorageContext.from_defaults(persist_dir='/Users/aarnatejwani/Desktop/retrieval_chatbot/index_store')

index = load_index_from_storage(storage_context)
query_engine = index.as_query_engine()

conn = sqlite3.connect('initdb/courier.db')
cursor = conn.cursor()

#functions
def track_parcel(parcel_id, user_id):
 cursor.execute(SELECT status FROM parcels WHERE parcel_id=? AND user_id=?", (parcel_id, user_id))
 result = cursor.fetchone()
 if result:
  return result
 return f"no parcel found with ID {parcel_id} for user {user_id}"
def cancel_parcel(parcel_id,user_id):
   cursor.execute("SELECT status FROM parcels WHERE parcel_id=? AND user_id=?", (parcel_id, user_id))
    result = cursor.fetchone()
    if not result:
        return f"parcel {parcel_id} not found or not associated with user {user_id}."
    if result[0].lower() == "delivered":
        return "parcel already delivered and cannot be canceled."
    cursor.execute("UPDATE parcels SET status='Cancelled' WHERE parcel_id=? AND user_id=?", (parcel_id, user_id))
    conn.commit()
    return f"parcel {parcel_id} has been cancelled."

def interpret_command(text):
 
