from __future__ import annotations

import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Tuple


class SimpleVectorStore:
    def __init__(self, index_path: str = "memory/vector_index.json"):
        self.index_path = Path(index_path)
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.index_path.exists():
            self.index_path.write_text("[]", encoding="utf-8")

    def _tokenize(self, text: str) -> List[str]:
        return re.findall(r"[a-zA-Z0-9]+", text.lower())

    def _vectorize(self, text: str) -> Counter:
        return Counter(self._tokenize(text))

    def _cosine(self, a: Counter, b: Counter) -> float:
        if not a or not b:
            return 0.0

        dot = sum(a[t] * b.get(t, 0) for t in a)
        norm_a = math.sqrt(sum(v * v for v in a.values()))
        norm_b = math.sqrt(sum(v * v for v in b.values()))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot / (norm_a * norm_b)

    def add_documents(self, docs: List[Dict]):
        """
        docs = [
            {
              "id": "...",
              "text": "...",
              "source": "...",
              "metadata": {...}
            }
        ]
        """
        records = []
        for doc in docs:
            vec = self._vectorize(doc["text"])
            records.append({
                **doc,
                "vector": dict(vec)
            })

        self.index_path.write_text(json.dumps(records, indent=2), encoding="utf-8")

    def load(self) -> List[Dict]:
        return json.loads(self.index_path.read_text(encoding="utf-8"))

    def search(self, query: str, top_k: int = 5) -> List[Dict]:
        query_vec = self._vectorize(query)
        docs = self.load()

        scored = []
        for doc in docs:
            doc_vec = Counter(doc.get("vector", {}))
            score = self._cosine(query_vec, doc_vec)
            scored.append((score, doc))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [
            {
                "score": round(score, 4),
                "id": doc["id"],
                "source": doc.get("source", ""),
                "text": doc.get("text", ""),
                "metadata": doc.get("metadata", {})
            }
            for score, doc in scored[:top_k]
        ]