from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from titanic.adapter.inbound.api.schemas.passenger_rose_model_schema import RoseModelSchema
from titanic.app.dtos.passenger_rose_model_dto import RoseModelResponse


class SurvivalPredictionStrategy(ABC):
    """생존 예측 알고리즘 전략 인터페이스 (Strategy Pattern)."""

    @property
    @abstractmethod
    async def name(self) -> str:
        """알고리즘 식별자."""

    @abstractmethod
    async def fit(self, X: list[list[float]], y: list[int]) -> None:
        """훈련 데이터로 모델을 학습한다."""

    @abstractmethod
    async def predict(self, x: list[float]) -> dict[str, Any]:
        """단일 승객 특성 벡터로 생존 여부를 예측하고 결과를 반환한다."""


class RoseModelUseCase(ABC):

    @abstractmethod
    async def introduce_myself(self, schema: RoseModelSchema) -> RoseModelResponse:
        pass

    @abstractmethod
    async def analyze_rose_survival(self) -> list[dict[str, Any]]:
        pass

    @abstractmethod
    async def predict_survival(
        self,
        passenger_data: dict[str, Any],
        strategy: SurvivalPredictionStrategy,
    ) -> dict[str, Any]:
        pass
