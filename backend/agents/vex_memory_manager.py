"""Memory management utilities for VEX agents.

The real project is expected to integrate a proper vector database for
Retrieval Augmented Generation (RAG).  For demonstration purposes this
module stores memories in a simple list and performs extremely naive
substring matching.
"""

from __future__ import annotations

from typing import List, Optional
from uuid import uuid4

from ..memory import Embedder, VectorStoreClient


class VexMemoryManager:
    """Persist and retrieve conversational memories.

    Parameters
    ----------
    embedder:
        Optional embedding backend used to create vector representations
        of memories.
    vector_store:
        Optional vector store client used for semantic search.  When not
        provided the manager falls back to a simple in-memory list and
        naive substring matching.
    """

    def __init__(
        self,
        *,
        embedder: Optional[Embedder] = None,
        vector_store: Optional[VectorStoreClient] = None,
    ) -> None:
        self._store: List[str] = []
        self._embedder = embedder
        self._vector_store = vector_store
        self._collection = "memories"

    async def add_memory(self, content: str) -> None:
        """Persist a piece of ``content`` for later retrieval."""

        self._store.append(content)

        if self._embedder and self._vector_store:
            try:
                vector = await self._embedder.embed(content)
                await self._vector_store.add_vectors(
                    self._collection,
                    ids=[str(uuid4())],
                    vectors=[vector],
                    metadatas=[{"text": content}],
                )
            except Exception:
                # Optional dependency may not be available or storage may fail.
                pass

    async def search(self, query: str, top_k: int = 5) -> List[str]:
        """Return up to ``top_k`` memories roughly matching ``query``.

        If an embedding model and vector store are configured, semantic
        search is performed.  Otherwise a naive substring match against
        the in-memory list is used.
        """

        if self._embedder and self._vector_store:
            try:
                vector = await self._embedder.embed(query)
                results = await self._vector_store.query(
                    self._collection, vector, n_results=top_k
                )
                return [meta.get("text", "") for _, _, meta in results]
            except Exception:
                # Fall back to simple substring search on failure.
                pass

        results = [m for m in self._store if query.lower() in m.lower()]
        return results[:top_k]
