from __future__ import annotations

import re
from dataclasses import dataclass

FORBIDDEN_KEYWORDS = {
    "INSERT",
    "UPDATE",
    "DELETE",
    "DROP",
    "ALTER",
    "TRUNCATE",
    "CREATE",
    "ATTACH",
    "DETACH",
    "PRAGMA",
    "VACUUM",
    "REINDEX",
}


SQL_FENCE_RE = re.compile(r"```(?:sql)?\s*(.*?)\s*```", re.IGNORECASE | re.DOTALL)


def extract_sql(text: str) -> str:
    """
    Best-effort extraction of raw SQL from LLM output.
    Handles fenced code and plain-text answers that include extra prose.
    """
    cleaned = (text or "").strip()
    if not cleaned:
        return cleaned

    match = SQL_FENCE_RE.search(cleaned)
    if match:
        cleaned = match.group(1).strip()
    else:
        sql_start = re.search(r"\b(SELECT|WITH)\b", cleaned, re.IGNORECASE)
        if sql_start:
            cleaned = cleaned[sql_start.start() :]

    # Collapse formatting noise from multiline model output.
    cleaned = re.sub(r"\s+", " ", cleaned).strip()

    # Accept a single trailing semicolon, which is common in LLM SQL output.
    cleaned = re.sub(r";\s*$", "", cleaned).strip()
    return cleaned


@dataclass(frozen=True)
class ValidationResult:
    ok: bool
    reason: str
    sql: str


def _has_semicolon(sql: str) -> bool:
    return ";" in sql


def _normalize_for_checking(sql: str) -> str:
    # Collapse whitespace so keyword scanning is more robust.
    return re.sub(r"\s+", " ", sql).strip().upper()


def validate_and_sanitize_sql(sql_text: str, *, row_limit: int) -> ValidationResult:
    sql = extract_sql(sql_text)
    if not sql:
        return ValidationResult(ok=False, reason="Empty SQL generated", sql="")

    if len(sql) > 5000:
        return ValidationResult(ok=False, reason="SQL too long", sql=sql)

    if _has_semicolon(sql):
        return ValidationResult(ok=False, reason="Only a single SELECT statement is allowed", sql=sql)

    normalized = _normalize_for_checking(sql)

    if not (normalized.startswith("SELECT") or normalized.startswith("WITH")):
        return ValidationResult(ok=False, reason="Only SELECT/CTE (WITH) queries are allowed", sql=sql)

    for kw in FORBIDDEN_KEYWORDS:
        if re.search(rf"\b{kw}\b", normalized):
            return ValidationResult(ok=False, reason=f"Forbidden keyword detected: {kw}", sql=sql)

    # Enforce row limiting to prevent large responses.
    if not re.search(r"\bLIMIT\s+\d+\b", normalized):
        sql = sql.rstrip() + f" LIMIT {row_limit}"

    return ValidationResult(ok=True, reason="OK", sql=sql)
