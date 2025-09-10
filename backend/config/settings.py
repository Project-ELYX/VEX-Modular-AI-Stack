from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    """Application settings.

    Loads variables from ``.env`` and provides default paths and flags.
    """

    model_config = SettingsConfigDict(
        env_file=[BASE_DIR.parent / '.env', BASE_DIR / '.env'],
        env_file_encoding='utf-8',
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
    vector_backend: str | None = 'faiss'

    # Feature flags
    use_gpu: bool = False


settings = Settings()

