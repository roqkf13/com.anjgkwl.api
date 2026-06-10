from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class RoseModelRepository(ABC):
    """ML 학습용 전체 승객 데이터 조회 포트."""

    @abstractmethod
    async def get_all_records(self) -> list[dict[str, Any]]:
        ...
