import os

# Avoid langsmith/zstandard build issues on cloud; not needed for this demo
os.environ.setdefault("LANGCHAIN_TRACING_V2", "false")

import streamlit as st
from dotenv import load_dotenv

from chroma_store import is_db_ready
from ingest import ingest
from memory_store import clear_memory
from rag_chain import ask, warm_up

load_dotenv()

APP_VERSION = "1.2.0"  # bump when deploying — visible in UI to confirm latest code

# Streamlit Community Cloud stores secrets in the dashboard (not .env)
if "GROQ_API_KEY" in st.secrets:
    os.environ["GROQ_API_KEY"] = st.secrets["GROQ_API_KEY"]

st.set_page_config(
    page_title="Business FAQ Chatbot",
    page_icon="💬",
    layout="centered",
)


@st.cache_resource(show_spinner="Loading knowledge base and models (first time may take a few minutes)...")
def bootstrap():
    if not is_db_ready():
        ingest()
    warm_up()
    return APP_VERSION


st.title("💬 Business FAQ Chatbot")
st.caption("RAG-powered assistant — answers from your business documents")

if not os.getenv("GROQ_API_KEY"):
    st.error(
        "Missing `GROQ_API_KEY`. Add it to `.env` locally, or in "
        "**Streamlit Cloud → Settings → Secrets** when deployed."
    )
    st.stop()

build = bootstrap()
st.caption(f"Build **{build}** — if you still see errors, use *Manage app → Reboot* on Streamlit Cloud")

TEST_USER = "demo_user"

if st.button("🔄 Clear conversation"):
    clear_memory(TEST_USER)
    st.session_state.messages = []

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! How can I help you today?"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

query = st.chat_input("Ask about store hours, delivery, returns...")
if query:
    st.session_state.messages.append({"role": "user", "content": query})
    st.chat_message("user").write(query)

    with st.spinner("Thinking..."):
        response = ask(user_id=TEST_USER, question=query)

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)
