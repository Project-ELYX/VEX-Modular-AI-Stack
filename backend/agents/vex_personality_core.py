"""Personality core responsible for prompt assembly and model calls.

The :class:`VexPersonalityCore` can operate in two modes:

``local``
    Utilises the ``llama.cpp`` bindings for on-device inference.  This
    requires the ``llama_cpp`` package and a path to a compiled model.
``remote``
    Sends the prompt to an HTTP endpoint (for example OpenRouter or
    OpenAI).  The exact API contract is intentionally tiny so that it can
    be adapted to many providers.

Both modes support optional streaming where tokens are yielded one by
one.  The public interface is purposely lightweight so that higher level
components such as the router can remain agnostic of the transport layer.
"""

from __future__ import annotations

import asyncio
from typing import AsyncGenerator, List, Optional

try:  # pragma: no cover - optional dependency
    from llama_cpp import Llama  # type: ignore
except Exception:  # pragma: no cover - not installed
    Llama = None  # type: ignore

import httpx


class VexPersonalityCore:
    """Assemble prompts and obtain completions from an LLM."""

    def __init__(
        self,
        *,
        system_prompt: str = "You are VEX, a helpful assistant.",
        local_model_path: Optional[str] = None,
        remote_url: Optional[str] = None,
        api_key: Optional[str] = None,
        use_remote: bool = False,
    ) -> None:
        self.system_prompt = system_prompt
        self.local_model_path = local_model_path
        self.remote_url = remote_url
        self.api_key = api_key
        self.use_remote = use_remote

        self._llama: Optional[Llama] = None
        if local_model_path and Llama is not None:
            # ``Llama`` is blocking; we keep a handle for ``asyncio.to_thread``
            self._llama = Llama(model_path=local_model_path)

    # ------------------------------------------------------------------
    # Prompt assembly helpers
    # ------------------------------------------------------------------
    def build_prompt(self, user_message: str, context: Optional[List[str]] = None) -> str:
        """Construct the textual prompt from user input and memory."""
        parts = [self.system_prompt]
        if context:
            parts.append("\n".join(context))
        parts.append(user_message)
        return "\n\n".join(parts)

    # ------------------------------------------------------------------
    # Model selection utilities
    # ------------------------------------------------------------------
    def set_remote(self, use_remote: bool) -> None:
        """Switch between local and remote model usage."""
        self.use_remote = use_remote

    # ------------------------------------------------------------------
    # Generation
    # ------------------------------------------------------------------
    async def generate_response(
        self, prompt: str, *, stream: bool = False
    ) -> AsyncGenerator[str, None] | str:
        """Return a completion for ``prompt``.

        When ``stream`` is ``True`` an asynchronous generator yielding
        tokens is returned, otherwise the complete string is produced.
        """

        if not self.use_remote and self._llama is not None:
            return await self._generate_local(prompt, stream=stream)
        return await self._generate_remote(prompt, stream=stream)

    async def _generate_local(
        self, prompt: str, *, stream: bool = False
    ) -> AsyncGenerator[str, None] | str:
        if self._llama is None:
            raise RuntimeError("Local model not available")

        def _call_llama() -> dict:
            return self._llama(prompt, stream=stream)  # type: ignore

        if not stream:
            result = await asyncio.to_thread(_call_llama)
            return result["choices"][0]["text"]

        async def _streamer() -> AsyncGenerator[str, None]:
            iterator = await asyncio.to_thread(_call_llama)
            text_key = "text"
            for chunk in iterator:
                yield chunk["choices"][0][text_key]

        return _streamer()

    async def _generate_remote(
        self, prompt: str, *, stream: bool = False
    ) -> AsyncGenerator[str, None] | str:
        if not self.remote_url:
            raise RuntimeError("No remote URL configured")

        headers = {"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}
        client = httpx.AsyncClient(headers=headers, timeout=60.0)

        if not stream:
            async with client:
                response = await client.post(self.remote_url, json={"prompt": prompt})
                response.raise_for_status()
                data = response.json()
                return data.get("text", "")

        async def _streamer() -> AsyncGenerator[str, None]:
            async with client.stream("POST", self.remote_url, json={"prompt": prompt}) as resp:
                async for chunk in resp.aiter_text():
                    yield chunk

        return _streamer()
