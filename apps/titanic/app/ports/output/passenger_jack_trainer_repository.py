from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class JackTrainerRepository(ABC):
    """생존 예측 모델 학습용 피처 데이터 조회 포트."""

    @abstractmethod
    async def get_training_data(self) -> list[dict[str, Any]]:
        ...
