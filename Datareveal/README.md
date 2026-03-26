# DataReveal

Where your data reveals its story.

DataReveal is a local-first RAG + SQL chatbot with:
- FastAPI backend for uploads and question answering
- Streamlit frontend for the chat experience
- Ollama for local LLM and embedding inference
- SQLite for tabular datasets and FAISS for document retrieval

  <img width="1465" height="815" alt="Screenshot 2026-03-26 at 3 06 44 PM" src="https://github.com/user-attachments/a<img width="1470" height="836" alt="Screenshot 2026-03-26 at 3 07 10 PM" src="https://github.com/user-attachments/assets/a81c7ab4-dd70-4516-b5a0-fd2fb020bdef" />
ssets/af614794-06b9-4778-aab3-293e8ed76768" />
<img width="1467" height="806" alt="Screenshot 2026-03-26 at 3 09 25 PM" src="https://github.com/user-attachments/assets/5da3f54c-bab5-4dc2-a161-5c4f8157ff38" />
<img width="1464" height="829" alt="Screenshot 2026-03-26 at 3 11 13 PM" src="https://github.com/user-attachments/assets/f6006b14-a78a-4461-a0a7-5835dc2eac6b" />



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
