"""ChromaDB helpers — use PersistentClient so local and Streamlit Cloud behave the same."""

import os
import shutil

import chromadb
from langchain_chroma import Chroma

DB_DIR = "chroma_db"
COLLECTION_NAME = "langchain"


def get_client() -> chromadb.PersistentClient:
    os.makedirs(DB_DIR, exist_ok=True)
    return chromadb.PersistentClient(path=DB_DIR)


def is_db_ready() -> bool:
    if not os.path.isdir(DB_DIR):
        return False
    try:
        client = get_client()
        return client.get_collection(COLLECTION_NAME).count() > 0
    except Exception:
        return False


def reset_db() -> None:
    if os.path.exists(DB_DIR):
        shutil.rmtree(DB_DIR)
    os.makedirs(DB_DIR, exist_ok=True)


def open_vectorstore(embeddings) -> Chroma:
    return Chroma(
        client=get_client(),
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
    )
