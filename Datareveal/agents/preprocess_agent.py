from __future__ import annotations

import re
from pathlib import Path
from typing import List, Optional

import pandas as pd
from pypdf import PdfReader


def normalize_column_name(name: str) -> str:
    """
    Convert column names to safe SQLite identifiers:
    - lowercase
    - only letters/numbers/underscore
    - prefix if starts with digit
    """
    base = (name or "").strip().lower()
    base = re.sub(r"[^a-z0-9_]+", "_", base)
    base = re.sub(r"_+", "_", base).strip("_")
    if not base:
        base = "col"
    if re.match(r"^\d", base):
        base = f"col_{base}"
    return base


def make_unique(columns: List[str]) -> List[str]:
    seen = {}
    out = []
    for c in columns:
        if c not in seen:
            seen[c] = 0
            out.append(c)
            continue
        seen[c] += 1
        out.append(f"{c}_{seen[c]}")
    return out


def preprocess_tabular_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = make_unique([normalize_column_name(c) for c in df.columns])
    return df


def load_tabular_file(file_path: str) -> pd.DataFrame:
    path = Path(file_path)
    suffix = path.suffix.lower()
    if suffix in {".csv"}:
        return pd.read_csv(path)
    if suffix in {".xlsx", ".xls"}:
        # MVP: use first sheet.
        return pd.read_excel(path, sheet_name=0)
    raise ValueError(f"Unsupported tabular file type: {suffix}")


def extract_text_from_pdf(file_path: str) -> str:
    reader = PdfReader(file_path)
    chunks: List[str] = []
    for page in reader.pages:
        page_text = page.extract_text() or ""
        if page_text.strip():
            chunks.append(page_text)
    return "\n\n".join(chunks).strip()


def load_text_file(file_path: str) -> str:
    return Path(file_path).read_text(encoding="utf-8", errors="ignore")

