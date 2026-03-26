from __future__ import annotations

from typing import Optional


SQL_KEYWORDS = [
    "count",
    "sum",
    "total",
    "average",
    "avg",
    "group by",
    "order by",
    "where",
    "join",
    "filter",
    "table",
    "column",
    "columns",
    "rows",
    "metric",
    "revenue",
    "amount",
]


def decide_mode(*, query: str, forced_mode: Optional[str] = None) -> str:
    if forced_mode in {"rag", "sql"}:
        return forced_mode

    q = (query or "").lower()

    if any(k in q for k in SQL_KEYWORDS):
        return "sql"

    # Heuristic: if the question includes explicit numbers, it's likely numeric/SQL.
    if any(ch.isdigit() for ch in q):
        return "sql"

    return "rag"

