#!/usr/bin/env python3

from llama_index.core import Settings
from llama_index.core.llms import ChatMessage
from llama_index.core.memory import VectorMemory
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from qdrant_client import QdrantClient
from qdrant_client import models
from llama_index.vector_stores.qdrant import QdrantVectorStore
import pandas as pd
from tqdm import tqdm
import re

CHAT_DB_PORT = 7000
MOCK_CHAT_HISTORY_PATH = "mock_chat_history.csv"
COLLECTION_NAME = "llamaindex_chat_store"

Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")
df = pd.read_csv(MOCK_CHAT_HISTORY_PATH)
chat_db_client = QdrantClient(host="localhost", port=CHAT_DB_PORT)
chat_db_vector_store = QdrantVectorStore(client=chat_db_client, collection_name=COLLECTION_NAME)
vector_memory = VectorMemory.from_defaults(vector_store=chat_db_vector_store)
#for i in tqdm(range(0, len(df)), desc="Creating mock chat history from csv"):
for i in tqdm(range(0, 100), desc="Creating mock chat history from csv"):
    row = df.iloc[i]
    msg = ChatMessage(role="user", content=row["question"]) 
    vector_memory.put(msg)
    unparsed_answer = row["answers"] #csv answer col contains the actual answer and other info that needs to be removed
    parsed_answer = re.search(r"(?<=\[).+?(?=\])", unparsed_answer).group(0) 
    msg = ChatMessage(role="assistant", content=parsed_answer) 
    vector_memory.put(msg)