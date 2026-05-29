from __future__ import annotations

from abc import ABC, abstractmethod


class WalterRepository(ABC):
    @abstractmethod
    async def get_data(self) -> list[dict[str, str]]:
        ...

    @abstractmethod
    async def get_count(self) -> int:
        ...

    @abstractmethod
    async def get_count_survived(self) -> int:
        ...

    @abstractmethod
    async def get_count_dead(self) -> int:
        ...
