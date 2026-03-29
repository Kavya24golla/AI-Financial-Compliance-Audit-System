from __future__ import annotations

from typing import List


def chunk_text(text: str, chunk_size: int = 900, overlap: int = 120) -> List[str]:
    """
    Simple word-based chunking.
    Good enough for policy docs, filing summaries, and past-case text.
    """
    words = text.split()
    if not words:
        return []

    chunks = []
    step = max(1, chunk_size - overlap)

    for start in range(0, len(words), step):
        chunk = words[start:start + chunk_size]
        if chunk:
            chunks.append(" ".join(chunk))

    return chunks