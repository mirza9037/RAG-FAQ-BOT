import os

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma

from chroma_store import COLLECTION_NAME, get_client, reset_db

DOCS_DIR = "docs"


def load_documents():
    docs = []
    for filename in os.listdir(DOCS_DIR):
        path = os.path.join(DOCS_DIR, filename)
        if filename.endswith(".txt"):
            docs.extend(TextLoader(path, encoding="utf-8").load())
        elif filename.endswith(".pdf"):
            docs.extend(PyPDFLoader(path).load())
    return docs


def ingest():
    print("Loading documents...")
    docs = load_documents()
    if not docs:
        print("No documents found in /docs. Add .txt or .pdf files and retry.")
        return

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=60)
    chunks = splitter.split_documents(docs)
    print(f"{len(chunks)} chunks created.")

    print("Loading embedding model (downloads once ~80MB)...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    print("Writing to ChromaDB...")
    reset_db()
    Chroma.from_documents(
        chunks,
        embeddings,
        client=get_client(),
        collection_name=COLLECTION_NAME,
    )
    print(f"Done. {len(chunks)} chunks stored in '{COLLECTION_NAME}'.")


if __name__ == "__main__":
    ingest()
