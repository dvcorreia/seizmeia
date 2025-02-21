from __future__ import annotations

import asyncio
from datetime import timedelta


class AsyncHealtherMock:
    def __init__(
        self,
        sleep_time: timedelta,
        live_status: str | None,
        ready_status: str | None,
    ) -> None:
        self.sleep_time = sleep_time
        self.live_status = live_status
        self.ready_status = ready_status

    async def live(self) -> str | None:
        await asyncio.sleep(self.sleep_time.total_seconds())
        return self.live_status

    async def ready(self) -> str | None:
        await asyncio.sleep(self.sleep_time.total_seconds())
        return self.ready_status
