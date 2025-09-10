"""Primary orchestration logic for VEX agents.

The :class:`VexRouter` wires together the validator, memory manager and
personality core.  ``handle_message`` performs the following steps:

1. Validate the incoming user message.
2. Retrieve relevant memories.
3. Build a prompt and query the language model (local or remote).
4. Optionally stream the response back to the caller.
5. Persist the conversation to memory.
"""

from __future__ import annotations

from typing import AsyncGenerator, Optional

from .vex_memory_manager import VexMemoryManager
from .vex_personality_core import VexPersonalityCore
from .vex_validator import VexValidator


class VexRouter:
    """Coordinate the individual components that form an agent."""

    def __init__(
        self,
        *,
        personality_core: Optional[VexPersonalityCore] = None,
        validator: Optional[VexValidator] = None,
        memory_manager: Optional[VexMemoryManager] = None,
    ) -> None:
        self.personality_core = personality_core or VexPersonalityCore()
        self.validator = validator or VexValidator()
        self.memory_manager = memory_manager or VexMemoryManager()

    # ------------------------------------------------------------------
    # Model mode utilities
    # ------------------------------------------------------------------
    def set_remote(self, use_remote: bool) -> None:
        """Toggle between local and remote model usage."""
        self.personality_core.set_remote(use_remote)

    # ------------------------------------------------------------------
    # Routing logic
    # ------------------------------------------------------------------
    async def handle_message(
        self, message: str, *, stream: bool = False
    ) -> AsyncGenerator[str, None] | str:
        """Process ``message`` and return a response.

        Parameters
        ----------
        message:
            The user's input.
        stream:
            If ``True``, an asynchronous generator yielding chunks is
            returned.  Otherwise the full response string is produced.
        """

        if not await self.validator.validate(message):
            raise ValueError("Message failed validation")

        context = await self.memory_manager.search(message)
        prompt = self.personality_core.build_prompt(message, context)

        if stream:
            async def _generator() -> AsyncGenerator[str, None]:
                accumulated = ""
                async for chunk in self.personality_core.generate_response(prompt, stream=True):
                    accumulated += chunk
                    yield chunk
                await self.memory_manager.add_memory(message)
                await self.memory_manager.add_memory(accumulated)

            return _generator()

        response = await self.personality_core.generate_response(prompt, stream=False)
        if isinstance(response, str):
            await self.memory_manager.add_memory(message)
            await self.memory_manager.add_memory(response)
            return response
        return ""
