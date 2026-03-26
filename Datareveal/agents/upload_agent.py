from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional, Tuple
from uuid import uuid4

import pandas as pd
from sqlalchemy import create_engine

from agents.chunk_agent import chunk_text
from agents.embedding_agent import get_embeddings
from agents.preprocess_agent import extract_text_from_pdf, load_text_file, load_tabular_file, preprocess_tabular_df
from rag.vector_store import build_faiss_store
from utils.settings import SQLITE_DIR, UPLOAD_DIR, VECTOR_DIR


def _ensure_safe_name(filename: str) -> str:
    # Minimal secure filename: remove path separators and keep safe chars.
    name = (filename or "upload").strip().replace("/", "_").replace("\\", "_")
    name = "".join(c for c in name if c.isalnum() or c in {".", "-", "_"}).strip()
    return name or "upload"


def _sqlite_db_path(dataset_id: str) -> Path:
    return SQLITE_DIR / f"{dataset_id}.db"


def _table_name(dataset_id: str) -> str:
    # Stable, sqlite-safe table identifier.
    return f"t_{dataset_id.replace('-', '')[:12]}"


def ingest_upload(*, file_path: str, original_filename: str, dataset_id: Optional[str] = None) -> Dict[str, Any]:
    dataset_id = dataset_id or str(uuid4())
    path = Path(file_path)
    ext = path.suffix.lower()

    if ext in {".csv", ".xlsx", ".xls"}:
        df = load_tabular_file(str(path))
        df = preprocess_tabular_df(df)
        db_path = _sqlite_db_path(dataset_id)
        db_path.parent.mkdir(parents=True, exist_ok=True)

        engine = create_engine(f"sqlite:///{db_path}")
        table = _table_name(dataset_id)
        df.to_sql(table, engine, if_exists="replace", index=False)

        return {
            "dataset_id": dataset_id,
            "mode_ingested": "sql",
            "sqlite_db_path": str(db_path),
            "table_name": table,
            "rows": int(len(df)),
            "columns": list(df.columns),
        }

    if ext in {".txt", ".md", ".pdf"}:
        if ext == ".pdf":
            full_text = extract_text_from_pdf(str(path))
        else:
            full_text = load_text_file(str(path))

        full_text = full_text.strip()
        if not full_text:
            raise ValueError("No text extracted from uploaded document.")

        chunks = chunk_text(full_text)
        embeddings = get_embeddings()

        texts = chunks
        metadatas = [{"chunk_id": i} for i in range(len(texts))]
        build_faiss_store(dataset_id=dataset_id, texts=texts, metadatas=metadatas, embeddings=embeddings)

        return {
            "dataset_id": dataset_id,
            "mode_ingested": "rag",
            "vector_store_dir": str((VECTOR_DIR / dataset_id).resolve()),
            "chunks_indexed": int(len(texts)),
        }

    raise ValueError(f"Unsupported file type: {ext}")


def save_upload_to_disk(*, upload_bytes: bytes, original_filename: str, dataset_id: Optional[str] = None) -> Tuple[str, str]:
    dataset_id = dataset_id or str(uuid4())
    safe_name = _ensure_safe_name(original_filename)
    out_path = UPLOAD_DIR / f"{dataset_id}__{safe_name}"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(upload_bytes)
    return str(out_path), dataset_id

