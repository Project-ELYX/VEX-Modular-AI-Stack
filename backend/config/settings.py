from pathlib import Path
from typing import Literal

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent

# Potential locations of the ``.env`` file. Search the project root first
# and fall back to the backend directory for backwards compatibility.
ENV_FILES = [BASE_DIR.parent / ".env", BASE_DIR / ".env"]

class Settings(BaseSettings):
    """Application settings.

    Loads variables from ``.env`` and provides default paths and flags.
    """

    model_config = SettingsConfigDict(
        env_file=ENV_FILES,
        env_file_encoding="utf-8",
    )

    # Paths
    base_path: Path = BASE_DIR
    models_path: Path = BASE_DIR.parent / 'models'
    local_model_path: Path | None = None

    # API keys
    openai_api_key: str | None = None
    openrouter_api_key: str | None = None
    anthropic_api_key: str | None = None

    # Model settings
    embedding_model: str | None = 'text-embedding-3-large'
    vector_backend: Literal["chroma", "qdrant"] = "chroma"

    @field_validator("vector_backend", mode="before")
    @classmethod
    def _normalize_vector_backend(cls, v: str | None) -> str:
        if v is None:
            return "chroma"
        v = v.lower()
        if v not in {"chroma", "qdrant"}:
            raise ValueError("VECTOR_BACKEND must be 'chroma' or 'qdrant'")
        return v

    # Feature flags
    use_gpu: bool = False


settings = Settings()

