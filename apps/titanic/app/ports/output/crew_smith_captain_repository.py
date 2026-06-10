from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class SmithCaptainRepository(ABC):
    """전체 승객 생존/사망 통계 조회 포트."""

    @abstractmethod
    async def get_stats(self) -> dict[str, Any]:
        ...
