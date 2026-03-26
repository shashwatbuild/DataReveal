from __future__ import annotations

import os
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]  # rag-enterprise/
DATA_DIR = PROJECT_ROOT / "data"
UPLOAD_DIR = DATA_DIR / "uploads"
SQLITE_DIR = DATA_DIR / "sqlite"
VECTOR_DIR = DATA_DIR / "vector"


OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_CHAT_MODEL = os.getenv("OLLAMA_CHAT_MODEL", "llama3")
OLLAMA_EMBED_MODEL = os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text")

# Hard caps for MVP safety/performance.
SQL_ROW_LIMIT = int(os.getenv("SQL_ROW_LIMIT", "50"))
SQL_MAX_RESPONSE_CHARS = int(os.getenv("SQL_MAX_RESPONSE_CHARS", "12000"))
SQL_MAX_SQL_CHARS = int(os.getenv("SQL_MAX_SQL_CHARS", "5000"))

# Ensure directories exist at import time (safe; only creates inside workspace).
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
SQLITE_DIR.mkdir(parents=True, exist_ok=True)
VECTOR_DIR.mkdir(parents=True, exist_ok=True)

