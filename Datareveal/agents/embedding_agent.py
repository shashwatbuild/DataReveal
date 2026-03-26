from __future__ import annotations

from langchain_ollama import OllamaEmbeddings

from utils.settings import OLLAMA_BASE_URL, OLLAMA_EMBED_MODEL


def get_embeddings():
    # LangChain wrapper around Ollama embeddings.
    return OllamaEmbeddings(
        model=OLLAMA_EMBED_MODEL,
        base_url=OLLAMA_BASE_URL,
    )

