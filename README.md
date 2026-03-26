# DataReveal

Where your data reveals its story.

DataReveal is a local-first RAG + SQL chatbot with:
- FastAPI backend for uploads and question answering
- Streamlit frontend for the chat experience
- Ollama for local LLM and embedding inference
- SQLite for tabular datasets and FAISS for document retrieval

## Prerequisites

- Python 3.10+ recommended
- Ollama running locally
- Required Ollama models:
  - `OLLAMA_CHAT_MODEL` (default `llama3`)
  - `OLLAMA_EMBED_MODEL` (default `nomic-embed-text`)

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run backend

```bash
uvicorn backend.api:app --reload --host 0.0.0.0 --port 8000
```

## Run frontend

```bash
streamlit run frontend/streamlit_app.py --server.port 8501
```

## Environment variables

- `OLLAMA_BASE_URL` default: `http://localhost:11434`
- `OLLAMA_CHAT_MODEL` default: `llama3`
- `OLLAMA_EMBED_MODEL` default: `nomic-embed-text`
- `SQL_ROW_LIMIT` default: `50`

## Notes

- SQL execution is SELECT-only with safety validation and enforced LIMIT.
- RAG answers are grounded in retrieved FAISS chunks.
