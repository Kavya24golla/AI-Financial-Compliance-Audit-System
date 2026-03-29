from __future__ import annotations

from tools.vector_store import SimpleVectorStore


class RAGAgent:
    def __init__(self, index_path: str = "memory/vector_index.json"):
        self.store = SimpleVectorStore(index_path=index_path)

    def retrieve(self, query: str, top_k: int = 5):
        return self.store.search(query, top_k=top_k)