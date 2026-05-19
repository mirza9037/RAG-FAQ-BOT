# Business FAQ Chatbot (RAG)

A public-facing **Streamlit** chatbot that answers customer questions using your own documents (RAG).

**Stack:** LangChain · ChromaDB · Groq (LLaMA 3.1) · HuggingFace embeddings · Streamlit

---

## How it works

```
User question (browser)
        │
        ▼
   Streamlit app (app.py)
        │
        ├── ChromaDB     ← vector search on docs/
        ├── Groq LLM     ← grounded answer
        └── Memory       ← last 6 turns per session
```

---

## Run locally

### 1. Clone and install

```bash
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate   # Mac/Linux
pip install -r requirements.txt
```

### 2. Add your Groq API key

```bash
copy .env.example .env
```

Edit `.env` and set `GROQ_API_KEY`. Get a free key at [console.groq.com](https://console.groq.com).

### 3. Add business documents

Put `.txt` or `.pdf` files in `docs/` (see `docs/sample_faq.txt` for an example).

### 4. Build the knowledge base (first time)

```bash
python ingest.py
```

### 5. Start the app

```bash
streamlit run app.py
```

Open **http://localhost:8501**

---

## Deploy for everyone (Streamlit Community Cloud) — recommended

Free hosting with a public URL like `https://your-app.streamlit.app`.

### Step 1 — Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit: Streamlit RAG chatbot"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

> **Important:** Never commit `.env`. Your API key goes only in Streamlit Cloud secrets.

### Step 2 — Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
2. Click **New app** → select your repository.
3. Set **Main file path** to `app.py`.
4. Open **Advanced settings → Secrets** and paste:

```toml
GROQ_API_KEY = "gsk_your_actual_key_here"
```

5. Click **Deploy**. First boot may take a few minutes (downloads embedding model + builds ChromaDB from `docs/`).

**Python version:** This repo includes `.python-version` set to **3.12**. If deploy fails with `cffi` / `zstandard` / `ffi.h` errors, open your app on Streamlit Cloud → **Settings** → set **Python version** to **3.12** (not 3.14), then **Reboot app**.

### Step 3 — Share the link

Copy the app URL from the dashboard and share it — anyone can chat without installing anything.

---

## Updating documents

1. Edit or add files in `docs/`
2. Locally: run `python ingest.py` again
3. On Streamlit Cloud: delete the app cache or redeploy; the app auto-runs ingest if `chroma_db/` is missing

---

## Project structure

```
├── app.py              ← Streamlit UI (entry point for deploy)
├── ingest.py           ← docs/ → chroma_db/
├── rag_chain.py        ← RAG + Groq
├── memory_store.py     ← conversation memory
├── docs/               ← your knowledge base
├── chroma_db/          ← vector store (optional in git)
├── requirements.txt
├── .env.example
└── .streamlit/
    ├── config.toml
    └── secrets.toml.example
```

---

## Environment variables

| Variable       | Required | Description        |
|----------------|----------|--------------------|
| `GROQ_API_KEY` | Yes      | Groq API key       |

---

## Troubleshooting

**"Missing GROQ_API_KEY" on Streamlit Cloud**  
Add the key under App → Settings → Secrets (see format above).

**Slow first load on cloud**  
The app downloads the embedding model (~80MB) and may run ingest once. Later loads are faster.

**ChromaDB error**  
Run `python ingest.py` locally, or let the app build the DB on first run (spinner shown).

**Deploy fails with `cffi`, `zstandard`, or `ffi.h`**  
Streamlit defaulted to Python 3.14. Use Python **3.12** (`.python-version` in this repo, or set it in Cloud app Settings → Reboot).
