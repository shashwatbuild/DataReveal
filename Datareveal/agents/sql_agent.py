from __future__ import annotations

from typing import Dict, Any

from langchain_ollama import ChatOllama

from utils.settings import OLLAMA_BASE_URL, OLLAMA_CHAT_MODEL, SQL_ROW_LIMIT


def _schema_to_text(schema: Dict[str, Any]) -> str:
    lines = []
    for table, cols in (schema or {}).items():
        col_lines = ", ".join([f"{c['name']} ({c['type']})" for c in cols])
        lines.append(f"- {table}: {col_lines}")
    return "\n".join(lines) if lines else "(no tables found)"


def generate_sql(*, query: str, schema: Dict[str, Any], llm_temperature: float = 0.0) -> str:
    chat = ChatOllama(
        model=OLLAMA_CHAT_MODEL,
        base_url=OLLAMA_BASE_URL,
        temperature=llm_temperature,
    )

    schema_text = _schema_to_text(schema)

    prompt = f"""
You are an expert SQLite SQL generator.
Generate a single read-only SQL query to answer the user's question.

Rules:
- Only output a single SELECT query (you may use WITH, but no other statement types).
- Do not include semicolons.
- Do not use forbidden keywords: INSERT, UPDATE, DELETE, DROP, ALTER, TRUNCATE, CREATE, ATTACH, DETACH, PRAGMA.
- Always include LIMIT {SQL_ROW_LIMIT} (if not already present).
- Use table/column names exactly as provided in the schema.

Schema:
{schema_text}

User question:
{query}

Return ONLY the SQL query.
""".strip()

    resp = chat.invoke(prompt)
    return (resp.content or "").strip()

