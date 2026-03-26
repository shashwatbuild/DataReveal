from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from langchain_community.vectorstores import FAISS  # type: ignore

from utils.settings import VECTOR_DIR


def dataset_vector_dir(dataset_id: str) -> Path:
    return VECTOR_DIR / str(dataset_id)


def build_faiss_store(*, dataset_id: str, texts: List[str], metadatas: List[Dict[str, Any]], embeddings: Any) -> None:
    """
    Persist a per-dataset FAISS index on disk.
    """
    store = FAISS.from_texts(texts=texts, embedding=embeddings, metadatas=metadatas)
    persist_path = dataset_vector_dir(dataset_id)
    persist_path.mkdir(parents=True, exist_ok=True)
    store.save_local(str(persist_path))


def load_faiss_store(*, dataset_id: str, embeddings: Any) -> FAISS:
    persist_path = dataset_vector_dir(dataset_id)
    try:
        return FAISS.load_local(str(persist_path), embeddings, allow_dangerous_deserialization=True)
    except TypeError:
        # Older/newer LangChain versions may not expose this flag.
        return FAISS.load_local(str(persist_path), embeddings)


def retrieve_top_k(*, dataset_id: str, query: str, embeddings: Any, k: int) -> List[Dict[str, Any]]:
    store = load_faiss_store(dataset_id=dataset_id, embeddings=embeddings)
    docs = store.similarity_search(query, k=k)
    return [
        {
            "content": d.page_content,
            "metadata": d.metadata or {},
        }
        for d in docs
    ]

