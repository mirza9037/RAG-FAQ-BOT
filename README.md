# RAG FAQ Bot

A public-facing **Streamlit** chatbot that answers customer questions from your own documents using **RAG** (Retrieval-Augmented Generation).

**Live demo:** [rag-faq-bot.streamlit.app](https://rag-faq-bot.streamlit.app)  
**Repository:** [github.com/mirza9037/RAG-FAQ-BOT](https://github.com/mirza9037/RAG-FAQ-BOT)

**Stack:** LangChain · ChromaDB · Groq (LLaMA 3.1) · HuggingFace embeddings · Streamlit

---

## Features

- Chat UI powered by Streamlit
- Answers grounded in your `docs/` (`.txt` and `.pdf`)
- Per-session conversation memory (last 6 turns)
- Free deploy on Streamlit Community Cloud
- Auto-builds vector DB on first run (no `chroma_db` in Git)

---

## How it works

```
User question (browser)
        │
        ▼
   app.py (Streamlit)
        │
        ├── chroma_store.py  → ChromaDB (PersistentClient)
        ├── rag_chain.py     → retrieve + Groq LLM
        └── memory_store.py  → chat history
```

---

## Run locally

### 1. Clone and install

```bash
git clone https://github.com/mirza9037/RAG-FAQ-BOT.git
cd RAG-FAQ-BOT
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Mac/Linux
pip install -r requirements.txt
```

### 2. Add your Groq API key

```bash
copy .env.example .env   # Windows
# cp .env.example .env   # Mac/Linux
```

Edit `.env` and set `GROQ_API_KEY`. Get a free key at [console.groq.com](https://console.groq.com).

### 3. Add business documents

Put `.txt` or `.pdf` files in `docs/` (see `docs/sample_faq.txt` for an example).

### 4. Build the knowledge base (optional — app can do this on first run)

```bash
python ingest.py
```

### 5. Start the app

```bash
streamlit run app.py
```

Open **http://localhost:8501**

---

## Deploy on Streamlit Cloud

1. Fork or use this repo: `mirza9037/RAG-FAQ-BOT`
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**
3. **Main file:** `app.py` · **Branch:** `main`
4. **Python version:** **3.12** (required — see `.python-version`)
5. **Secrets** (Settings → Secrets):

```toml
GROQ_API_KEY = "gsk_your_actual_key_here"
```

6. **Deploy** — first boot may take several minutes (embeddings + ingest)

After deploy, confirm the UI shows **Build 1.2.0** under the title.

---

## Project structure

```
RAG-FAQ-BOT/
├── app.py                    ← Streamlit UI (deploy entry point)
├── chroma_store.py           ← ChromaDB PersistentClient helpers
├── ingest.py                 ← docs/ → chroma_db/
├── rag_chain.py              ← RAG + Groq
├── memory_store.py           ← conversation memory
├── docs/
│   └── sample_faq.txt        ← example business FAQ
├── requirements.txt
├── .python-version           ← 3.12 for Streamlit Cloud
├── .env.example
└── .streamlit/
    ├── config.toml
    └── secrets.toml.example
```

`chroma_db/` is created at runtime and is **not** committed (see `.gitignore`).

---

## Updating documents

1. Edit or add files in `docs/`
2. **Locally:** run `python ingest.py`
3. **Streamlit Cloud:** reboot the app (or clear cache); ingest runs automatically if the DB is empty

---

## Environment variables

| Variable       | Required | Description   |
|----------------|----------|---------------|
| `GROQ_API_KEY` | Yes      | Groq API key  |

Never commit `.env` or real API keys to GitHub.

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Missing `GROQ_API_KEY` | Add secret in Streamlit Cloud Settings |
| `cffi` / `zstandard` / `ffi.h` on deploy | Set Python **3.12**, not 3.14 → Reboot app |
| Chroma `ValueError` / tenant error | Reboot app (uses `PersistentClient`; DB rebuilds on cloud) |
| Old code still running on Cloud | Manage app → **Reboot**; check for **Build 1.2.0** in UI |
| Slow first load | Normal — downloads embedding model (~80MB) + ingests docs |

---

## License

MIT — use freely for learning and demos.
