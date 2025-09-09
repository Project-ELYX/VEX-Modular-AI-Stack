"""Memory management utilities for VEX agents.

The real project is expected to integrate a proper vector database for
Retrieval Augmented Generation (RAG).  For demonstration purposes this
module stores memories in a simple list and performs extremely naive
substring matching.
"""

from __future__ import annotations

from typing import List


class VexMemoryManager:
    """Persist and retrieve conversational memories."""

    def __init__(self) -> None:
        self._store: List[str] = []

    def add_memory(self, content: str) -> None:
        """Persist a piece of ``content`` for later retrieval."""
        self._store.append(content)

    def search(self, query: str, top_k: int = 5) -> List[str]:
        """Return up to ``top_k`` memories roughly matching ``query``.

        The current implementation performs a very small amount of
        filtering by returning memories that contain the query string.
        """

        results = [m for m in self._store if query.lower() in m.lower()]
        return results[:top_k]
