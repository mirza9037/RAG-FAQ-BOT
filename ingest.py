import os
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_chroma import Chroma

DOCS_DIR = "docs"
DB_DIR   = "chroma_db"

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
    Chroma.from_documents(chunks, embeddings, persist_directory=DB_DIR)
    print(f"Done. {len(chunks)} chunks stored in '{DB_DIR}/'.")

if __name__ == "__main__":
    ingest()
