from __future__ import annotations

import asyncio

from seizmeia.healthcheck.protocol import IHealthchecker


class AsyncHealthcheck(IHealthchecker):
    """
    Implements an asyncio healtcheck service.
    Requesting healthcheck status should be as slow as the slowest
    healthcheck provider.
    """

    async def ready(self) -> dict[str, str]:
        not_ready: dict[str, str] = {}

        status = await asyncio.gather(
            *[h.ready() for _, h in self.healthers.items()]
        )

        for name, msg in zip(self.healthers.keys(), status, strict=True):
            if msg:
                not_ready[name] = msg

        return not_ready

    async def live(self) -> dict[str, str]:
        not_live: dict[str, str] = {}

        status = await asyncio.gather(
            *[h.live() for _, h in self.healthers.items()]
        )

        for name, msg in zip(self.healthers.keys(), status, strict=True):
            if msg:
                not_live[name] = msg

        return not_live
