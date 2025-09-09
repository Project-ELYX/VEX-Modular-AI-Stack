import asyncio
from typing import List, Dict, Optional

try:
    from sentence_transformers import SentenceTransformer
except ImportError:  # pragma: no cover - optional dependency
    SentenceTransformer = None  # type: ignore


_MODEL_MAP = {
    "MiniLM": "all-MiniLM-L6-v2",
    "BGE": "bge-small-en",
}


class Embedder:
    """Wrapper around :mod:`sentence_transformers` models.

    Parameters
    ----------
    model_key:
        Key identifying which embedding model to load. Supported keys are
        ``"MiniLM"`` and ``"BGE"`` but any valid SentenceTransformer model
        name may be provided.
    device:
        Optional device identifier passed to SentenceTransformer.
    """

    def __init__(self, model_key: str = "MiniLM", *, device: Optional[str] = None):
        if SentenceTransformer is None:  # pragma: no cover - dependency not installed
            raise ImportError(
                "sentence-transformers package is required for Embedder"
            )

        model_name = _MODEL_MAP.get(model_key, model_key)
        self._model = SentenceTransformer(model_name, device=device)

    async def embed(self, text: str) -> List[float]:
        """Asynchronously embed ``text`` returning a list of floats."""

        loop = asyncio.get_running_loop()
        vector = await loop.run_in_executor(None, self._model.encode, text)
        return vector.tolist() if hasattr(vector, "tolist") else list(vector)

    @classmethod
    def from_config(cls, config: Dict[str, str]) -> "Embedder":
        """Create an :class:`Embedder` from a configuration mapping."""

        model_key = config.get("model", "MiniLM")
        device = config.get("device")
        return cls(model_key=model_key, device=device)
