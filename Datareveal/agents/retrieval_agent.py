from __future__ import annotations

from typing import Any, Dict, List

from agents.embedding_agent import get_embeddings
from rag.vector_store import retrieve_top_k


def retrieve_context(*, dataset_id: str, query: str, k: int = 4) -> List[Dict[str, Any]]:
    embeddings = get_embeddings()
    return retrieve_top_k(dataset_id=dataset_id, query=query, embeddings=embeddings, k=k)

