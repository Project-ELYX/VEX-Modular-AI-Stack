from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    """Application settings.

    Loads variables from ``.env`` and provides default paths and flags.
    """

    model_config = SettingsConfigDict(env_file=BASE_DIR / '.env', env_file_encoding='utf-8')

    # Paths
    base_path: Path = BASE_DIR
    models_path: Path = BASE_DIR.parent / 'models'

    # API keys
    openai_api_key: str | None = None

    # Feature flags
    use_gpu: bool = False


settings = Settings()

