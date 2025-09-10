from __future__ import annotations

import os
from typing import Optional

from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel

router = APIRouter()

# In-memory configuration storage
_config: dict[str, Optional[str]] = {
    "openrouter_api_key": os.getenv("OPENROUTER_API_KEY"),
    "anthropic_api_key": os.getenv("ANTHROPIC_API_KEY"),
    "mode": "local",
}

def _verify_token(x_token: str = Header(...)) -> None:
    """Very small token based auth guard."""
    expected = os.getenv("CONFIG_TOKEN", "secret-token")
    if x_token != expected:
        raise HTTPException(status_code=401, detail="Invalid token")


class ConfigRequest(BaseModel):
    openrouter_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    mode: str


@router.post("", dependencies=[Depends(_verify_token)])
async def set_config(cfg: ConfigRequest) -> dict[str, Optional[str]]:
    """Update configuration for API keys and model mode."""
    _config["openrouter_api_key"] = cfg.openrouter_api_key
    _config["anthropic_api_key"] = cfg.anthropic_api_key
    _config["mode"] = cfg.mode
    return _config


@router.get("", dependencies=[Depends(_verify_token)])
async def get_config() -> dict[str, Optional[str]]:
    """Return the current configuration."""
    return _config


def get_runtime_config() -> dict[str, Optional[str]]:
    """Helper for other modules to access runtime config."""
    return _config
