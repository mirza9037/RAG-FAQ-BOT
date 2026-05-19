import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.prompts import PromptTemplate

from chroma_store import open_vectorstore
from memory_store import get_memory

load_dotenv()

CONDENSE_PROMPT = PromptTemplate.from_template(
    """Given the chat history and a follow-up question, rewrite the follow-up as a standalone question.

Chat history:
{chat_history}

Follow-up: {question}
Standalone question:"""
)

ANSWER_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template="""You are a helpful customer support assistant for a Pakistani business.
Answer using ONLY the context below. Be brief and friendly.
If the answer isn't in the context, say you don't have that information and suggest contacting the business directly.

Context:
{context}

Question: {question}
Answer:"""
)

# Shared resources — loaded once at startup
_embeddings = None
_retriever  = None
_llm        = None

def _init():
    global _embeddings, _retriever, _llm
    if _llm is not None:
        return
    _embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    try:
        db = open_vectorstore(_embeddings)
    except Exception:
        # Stale or incompatible chroma_db folder — rebuild once
        from chroma_store import reset_db
        from ingest import ingest

        reset_db()
        ingest()
        db = open_vectorstore(_embeddings)
    _retriever = db.as_retriever(search_kwargs={"k": 3})
    _llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.2,
        api_key=os.getenv("GROQ_API_KEY"),
    )


def warm_up():
    """Load models and vector store once at startup."""
    _init()

def ask(user_id: str, question: str) -> str:
    """Ask a question with per-user memory."""
    _init()
    memory = get_memory(user_id)

    chain = ConversationalRetrievalChain.from_llm(
        llm=_llm,
        retriever=_retriever,
        memory=memory,
        condense_question_prompt=CONDENSE_PROMPT,
        combine_docs_chain_kwargs={"prompt": ANSWER_PROMPT},
        return_source_documents=False,
        verbose=False
    )

    result = chain.invoke({"question": question})
    return result["answer"]
