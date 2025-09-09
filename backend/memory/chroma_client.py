"""Asynchronous vector store client supporting ChromaDB and Qdrant."""

from __future__ import annotations

import asyncio
from functools import partial
from typing import Any, Dict, List, Optional, Sequence, Tuple


class VectorStoreClient:
    """Simple abstraction over ChromaDB and Qdrant vector stores.

    Parameters
    ----------
    config:
        Configuration dictionary. Must contain the key ``backend`` with value
        either ``"chroma"`` or ``"qdrant"``. Backend specific settings are
        also read from this dictionary.
    """

    def __init__(self, config: Dict[str, Any]):
        self.backend = config.get("backend", "chroma").lower()
        if self.backend == "chroma":
            self._client = self._init_chroma(config)
        elif self.backend == "qdrant":
            self._client = self._init_qdrant(config)
        else:  # pragma: no cover - defensive
            raise ValueError(f"Unsupported backend: {self.backend}")

    # ------------------------------------------------------------------
    # backend initialisation helpers
    def _init_chroma(self, config: Dict[str, Any]):
        try:
            import chromadb
            from chromadb.config import Settings
        except Exception as exc:  # pragma: no cover - optional dependency
            raise ImportError("chromadb is required for Chroma backend") from exc

        persist_dir = config.get("persist_directory")
        settings = Settings(chroma_db_impl="duckdb+parquet", persist_directory=persist_dir)
        return chromadb.Client(settings)

    def _init_qdrant(self, config: Dict[str, Any]):
        try:
            from qdrant_client import QdrantClient
        except Exception as exc:  # pragma: no cover - optional dependency
            raise ImportError("qdrant-client is required for Qdrant backend") from exc

        url = config.get("url", "http://localhost:6333")
        api_key = config.get("api_key")
        return QdrantClient(url=url, api_key=api_key)

    # ------------------------------------------------------------------
    async def add_vectors(
        self,
        collection: str,
        ids: Sequence[str],
        vectors: Sequence[Sequence[float]],
        metadatas: Optional[Sequence[Dict[str, Any]]] = None,
    ) -> None:
        """Add embeddings to the vector store."""

        if self.backend == "chroma":
            await self._add_chroma(collection, ids, vectors, metadatas)
        else:
            await self._add_qdrant(collection, ids, vectors, metadatas)

    async def _add_chroma(
        self,
        collection: str,
        ids: Sequence[str],
        vectors: Sequence[Sequence[float]],
        metadatas: Optional[Sequence[Dict[str, Any]]],
    ) -> None:
        loop = asyncio.get_running_loop()
        coll = await loop.run_in_executor(
            None, self._client.get_or_create_collection, collection
        )
        add = partial(
            coll.add,
            ids=list(ids),
            embeddings=[list(v) for v in vectors],
            metadatas=list(metadatas) if metadatas is not None else None,
        )
        await loop.run_in_executor(None, add)

    async def _add_qdrant(
        self,
        collection: str,
        ids: Sequence[str],
        vectors: Sequence[Sequence[float]],
        metadatas: Optional[Sequence[Dict[str, Any]]],
    ) -> None:
        try:
            from qdrant_client.http.models import PointStruct
        except Exception as exc:  # pragma: no cover - optional dependency
            raise ImportError("qdrant-client is required for Qdrant backend") from exc

        points = [
            PointStruct(id=id_, vector=list(vec), payload=meta or {})
            for id_, vec, meta in zip(ids, vectors, metadatas or [{}] * len(ids))
        ]
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, self._client.upsert, collection, points)

    # ------------------------------------------------------------------
    async def query(
        self, collection: str, vector: Sequence[float], *, n_results: int = 3
    ) -> List[Tuple[str, float, Dict[str, Any]]]:
        """Query the vector store and return list of (id, score, metadata)."""

        if self.backend == "chroma":
            return await self._query_chroma(collection, vector, n_results)
        else:
            return await self._query_qdrant(collection, vector, n_results)

    async def _query_chroma(
        self, collection: str, vector: Sequence[float], n_results: int
    ) -> List[Tuple[str, float, Dict[str, Any]]]:
        loop = asyncio.get_running_loop()
        coll = await loop.run_in_executor(
            None, self._client.get_or_create_collection, collection
        )
        query = partial(
            coll.query,
            query_embeddings=[list(vector)],
            n_results=n_results,
        )
        res = await loop.run_in_executor(None, query)
        ids = res.get("ids", [[]])[0]
        distances = res.get("distances", [[]])[0]
        metas = res.get("metadatas", [[]])[0]
        return [(id_, dist, meta) for id_, dist, meta in zip(ids, distances, metas)]

    async def _query_qdrant(
        self, collection: str, vector: Sequence[float], n_results: int
    ) -> List[Tuple[str, float, Dict[str, Any]]]:
        loop = asyncio.get_running_loop()
        res = await loop.run_in_executor(
            None,
            self._client.search,
            collection,
            list(vector),
            n_results,
            True,
        )
        return [
            (str(p.id), float(p.score), dict(p.payload or {}))
            for p in res
        ]

    # ------------------------------------------------------------------
    @classmethod
    def from_config(cls, config: Dict[str, Any]) -> "VectorStoreClient":
        return cls(config)
