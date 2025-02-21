from __future__ import annotations

from datetime import timedelta

import pytest

from seizmeia.healthcheck.asynchronous import AsyncHealthcheck
from tests.health import AsyncHealtherMock


@pytest.mark.asyncio
async def test_concurrent_health_check():
    """
    Testing ready and live, they should not take more than the time of the most
    expensive computation on multithreading systems.
    Time constrains are not tested due to weak reproducibility of results.
    """

    checker1 = AsyncHealtherMock(
        sleep_time=timedelta(seconds=0.01),
        live_status="not alive",
        ready_status="not ready. waiting for something",
    )

    checker2 = AsyncHealtherMock(
        sleep_time=timedelta(seconds=0.01), live_status=None, ready_status=None
    )

    checker3 = AsyncHealtherMock(
        sleep_time=timedelta(seconds=0.02), live_status=None, ready_status=None
    )

    healthcheck = AsyncHealthcheck()
    healthcheck.add("checker1", checker1)
    healthcheck.add("checker2", checker2)
    healthcheck.add("checker3", checker3)

    r = await healthcheck.ready()

    assert len(r.keys()) == 1
    assert r.get("checker1", None) == checker1.ready_status

    r = await healthcheck.live()

    assert len(r.keys()) == 1
    assert r.get("checker1", None) == checker1.live_status

    # changing live status of checker2. should be seen in the live result
    checker2.live_status = "went unhealthy. ups!"

    r = await healthcheck.live()
    assert len(r.keys()) == 2
    assert r.get("checker1", None) == checker1.live_status
    assert r.get("checker2", None) == checker2.live_status
