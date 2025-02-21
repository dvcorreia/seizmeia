from __future__ import annotations

from typing import Protocol


class IHealther(Protocol):
    """Any object implementing this can be checked for healthcheck status"""

    async def ready(self) -> str | None:
        """
        Indicates if the healther fully started and is ready to start working.
        If not ready, it can return a string describing why it is not.
        """
        ...

    async def live(self) -> str | None:
        """
        Used to understand if the healther is no longer capable of doing work
        (i.g MQTT client disconnected from broker and can no longer listen
        for incoming messages).
        If not live, it can return a string describing why it is not.
        """
        ...


class IHealthchecker(Protocol):
    """
    Defines a healthcheck service interface.
    It provides a group of methods to inquire healthers about their status.
    Any service with this interface can be a healthcheck service.
    """

    healthers: dict[str, IHealther] = {}

    def add(self, name: str, healther: IHealther) -> None:
        """Registers a healther object in the healthcheck service."""
        if name in self.healthers.keys():
            raise Exception(f"checker with name {name} already exists")

        self.healthers[name] = healther

    async def ready(self) -> dict[str, str]:
        """
        The Kubernetes readiness probe waits until the healther is fully
        started before it allows the to send traffic to the service.
        """
        ...

    async def live(self) -> dict[str, str]:
        """
        The Kubernetes liveness probe detects that the service is no longer
        serving requests and restarts the offending pod.
        """
        ...
