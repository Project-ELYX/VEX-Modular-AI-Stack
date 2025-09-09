"""Asynchronous content validation for VEX agents.

This module provides a very small stub used to demonstrate how
content moderation might be performed in a real system.  The
``validate`` coroutine simply returns ``True`` after yielding control
back to the event loop, making it easy to later plug in API calls or
other heavy checks without changing the router's behaviour.
"""

from __future__ import annotations

import asyncio


class VexValidator:
    """Validate user input before it reaches the LLM.

    The real implementation might call an external moderation service.
    For now the validator always returns ``True``.
    """

    async def validate(self, text: str) -> bool:
        """Asynchronously validate ``text``.

        Parameters
        ----------
        text:
            The user supplied content to validate.

        Returns
        -------
        bool
            ``True`` if the text passes validation.
        """

        # ``sleep(0)`` yields control so the function remains truly async
        # and can later be extended without changing its public contract.
        await asyncio.sleep(0)
        return True
