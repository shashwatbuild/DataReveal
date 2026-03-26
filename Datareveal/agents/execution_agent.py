from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Tuple

from utils.settings import SQL_MAX_RESPONSE_CHARS, SQL_ROW_LIMIT


def get_sqlite_schema(db_path: str) -> Dict[str, Any]:
    conn = sqlite3.connect(db_path)
    try:
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
        tables = [r[0] for r in cur.fetchall()]

        schema: Dict[str, Any] = {}
        for t in tables:
            cur.execute(f"PRAGMA table_info({t})")
            cols = []
            for row in cur.fetchall():
                # (cid, name, type, notnull, dflt_value, pk)
                cols.append({"name": row[1], "type": row[2] or "unknown"})
            schema[t] = cols

        return schema
    finally:
        conn.close()


def execute_sqlite_select(db_path: str, sql: str, *, row_limit: int = SQL_ROW_LIMIT) -> Dict[str, Any]:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        cur = conn.cursor()
        cur.execute(sql)

        columns = [d[0] for d in (cur.description or [])]
        rows = cur.fetchmany(row_limit)
        preview = [dict(r) for r in rows]

        # Truncate overly large fields to keep responses reasonable.
        def _truncate_obj(obj: Any) -> Any:
            if isinstance(obj, str) and len(obj) > SQL_MAX_RESPONSE_CHARS:
                return obj[:SQL_MAX_RESPONSE_CHARS] + "...(truncated)"
            return obj

        preview = [{k: _truncate_obj(v) for k, v in row.items()} for row in preview]
        return {"columns": columns, "rows_preview": preview, "row_count_preview": len(preview)}
    finally:
        conn.close()

