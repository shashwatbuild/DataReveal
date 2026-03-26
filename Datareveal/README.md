# DataReveal

Where your data reveals its story.

DataReveal is a local-first RAG + SQL chatbot with:
- FastAPI backend for uploads and question answering
- Streamlit frontend for the chat experience
- Ollama for local LLM and embedding inference
- SQLite for tabular datasets and FAISS for document retrieval

<img width="1465" height="815" alt="Screenshot 2026-03-26 at 3 06 44 PM" src="https://github.com/user-attachments/assets/f5293923-4fbe-40b7-bf8a-6b723d50eca2" />
<img width="1470" height="836" alt="Screenshot 2026-03-26 at 3 07 10 PM" src="https://github.com/user-attachments/assets/221c5d71-5509-438e-b349-0a1dd9f44b42" />
<img width="1467" height="806" alt="Screenshot 2026-03-26 at 3 09 25 PM" src="https://github.com/user-attachments/assets/78c12009-4ed6-47d5-8387-01bfa1eb4668" />
<img width="1464" height="829" alt="Screenshot 2026-03-26 at 3 11 13 PM" src="https://github.com/user-attachments/assets/1407c84e-f589-44a3-9b6b-b69e738561d7" />

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
