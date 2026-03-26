from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agents.execution_agent import execute_sqlite_select, get_sqlite_schema
from agents.retrieval_agent import retrieve_context
from agents.response_agent import generate_answer_rag, generate_answer_sql
from agents.router_agent import decide_mode
from agents.sql_agent import generate_sql
from agents.upload_agent import ingest_upload, save_upload_to_disk
from utils.settings import SQL_ROW_LIMIT, SQLITE_DIR, VECTOR_DIR
from utils.sql_validation import validate_and_sanitize_sql


app = FastAPI(title="Enterprise RAG + SQL Chatbot (MVP)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AskRequest(BaseModel):
    query: str
    dataset_id: str
    mode: Optional[str] = None  # "auto" | "sql" | "rag" (server treats None as auto)
    top_k: Optional[int] = 4


def _sqlite_db_path(dataset_id: str) -> Path:
    return SQLITE_DIR / f"{dataset_id}.db"


def _vector_dir_path(dataset_id: str) -> Path:
    return VECTOR_DIR / str(dataset_id)


def _has_rag_index(dataset_id: str) -> bool:
    # FAISS saves several files. We just check the directory exists and has at least one file.
    vdir = _vector_dir_path(dataset_id)
    return vdir.exists() and any(vdir.iterdir())


def _has_sqlite_db(dataset_id: str) -> bool:
    return _sqlite_db_path(dataset_id).exists()


@app.get("/health")
def health() -> Dict[str, Any]:
    return {
        "status": "ok",
        "sql_row_limit": SQL_ROW_LIMIT,
        "message": "Service is running. Upload data then ask questions.",
    }


@app.post("/upload")
async def upload(file: UploadFile = File(...)) -> Dict[str, Any]:
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Empty upload.")

    out_path, dataset_id = save_upload_to_disk(
        upload_bytes=content,
        original_filename=file.filename or file.client.filename or "upload",
    )

    try:
        ingestion = ingest_upload(file_path=out_path, original_filename=file.filename, dataset_id=dataset_id)
        return ingestion
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ingestion failed: {e}")


@app.post("/ask")
def ask(req: AskRequest) -> Dict[str, Any]:
    if req.mode == "auto":
        forced_mode = None
    else:
        forced_mode = req.mode

    mode = decide_mode(query=req.query, forced_mode=forced_mode)

    sqlite_ok = _has_sqlite_db(req.dataset_id)
    rag_ok = _has_rag_index(req.dataset_id)

    if mode == "sql" and not sqlite_ok:
        if rag_ok:
            mode = "rag"
        else:
            raise HTTPException(status_code=400, detail="Dataset has no SQL index (SQLite DB missing).")
    if mode == "rag" and not rag_ok:
        if sqlite_ok:
            mode = "sql"
        else:
            raise HTTPException(status_code=400, detail="Dataset has no RAG index (FAISS store missing).")

    if mode == "sql":
        db_path = str(_sqlite_db_path(req.dataset_id))
        try:
            schema = get_sqlite_schema(db_path=db_path)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Failed to read SQLite schema: {e}")

        try:
            sql_raw = generate_sql(query=req.query, schema=schema)
        except Exception as e:
            raise HTTPException(status_code=503, detail=f"SQL generation failed (Ollama unavailable?): {e}")

        validation = validate_and_sanitize_sql(sql_raw, row_limit=SQL_ROW_LIMIT)
        if not validation.ok:
            raise HTTPException(status_code=400, detail=f"SQL safety validation failed: {validation.reason}")

        try:
            exec_result = execute_sqlite_select(db_path=db_path, sql=validation.sql, row_limit=SQL_ROW_LIMIT)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"SQL execution failed: {e}")

        try:
            answer = generate_answer_sql(query=req.query, sql=validation.sql, execution_result=exec_result)
        except Exception as e:
            raise HTTPException(status_code=503, detail=f"Answer generation failed (Ollama unavailable?): {e}")

        return {
            "mode_used": "sql",
            "answer": answer,
            "sql": validation.sql,
            "result_preview": exec_result,
        }

    # mode == "rag"
    k = max(1, min(10, int(req.top_k or 4)))
    try:
        retrieved_chunks = retrieve_context(dataset_id=req.dataset_id, query=req.query, k=k)
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"RAG retrieval failed (Ollama unavailable?): {e}")

    try:
        answer = generate_answer_rag(query=req.query, retrieved_chunks=retrieved_chunks)
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"RAG answer generation failed (Ollama unavailable?): {e}")

    return {
        "mode_used": "rag",
        "answer": answer,
        "retrieved_context": retrieved_chunks,
    }


@app.get("/ask")
def ask_get(query: str, dataset_id: str, mode: Optional[str] = None, top_k: Optional[int] = 4) -> Dict[str, Any]:
    return ask(AskRequest(query=query, dataset_id=dataset_id, mode=mode, top_k=top_k))

