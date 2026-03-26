from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

from langchain_ollama import ChatOllama

from utils.settings import OLLAMA_BASE_URL, OLLAMA_CHAT_MODEL


def _get_chat_llm(*, temperature: float = 0.1) -> ChatOllama:
    return ChatOllama(model=OLLAMA_CHAT_MODEL, base_url=OLLAMA_BASE_URL, temperature=temperature)


def generate_answer_rag(*, query: str, retrieved_chunks: List[Dict[str, Any]]) -> str:
    llm = _get_chat_llm(temperature=0.0)

    context_lines = []
    for c in retrieved_chunks:
        chunk_id = c.get("metadata", {}).get("chunk_id", "unknown")
        content = (c.get("content") or "").strip()
        context_lines.append(f"[chunk-{chunk_id}] {content}")

    context_text = "\n\n".join(context_lines) if context_lines else "(no retrieved context)"

    prompt = f"""
You are a data-aware assistant. Answer the user question using ONLY the provided context.
If the context is insufficient, ask a clarifying question.

Context:
{context_text}

User question:
{query}

Answer:
""".strip()

    resp = llm.invoke(prompt)
    return (resp.content or "").strip()


def generate_answer_sql(*, query: str, sql: str, execution_result: Dict[str, Any]) -> str:
    llm = _get_chat_llm(temperature=0.0)

    payload = {
        "sql": sql,
        "row_count_preview": execution_result.get("row_count_preview"),
        "columns": execution_result.get("columns"),
        "rows_preview": execution_result.get("rows_preview"),
    }

    prompt = f"""
You are a helpful analytics assistant.
Explain the answer to the user based on the SQL execution result.

User question:
{query}

SQL:
{sql}

Execution result (JSON):
{json.dumps(payload, ensure_ascii=False)}

Rules:
- Do not claim additional facts beyond the result.
- If rows_preview is empty, say no matching records were found.
- Keep the response concise and human-readable.

Answer:
""".strip()

    resp = llm.invoke(prompt)
    return (resp.content or "").strip()

