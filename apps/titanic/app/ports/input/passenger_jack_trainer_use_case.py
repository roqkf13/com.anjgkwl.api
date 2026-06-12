from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from titanic.adapter.inbound.api.schemas.passenger_jack_trainer_schema import JackTrainerSchema
from titanic.app.dtos.passenger_jack_trainer_dto import JackTrainerResponse


class JackTrainerUseCase(ABC):

    @abstractmethod
    async def introduce_myself(self, schema: JackTrainerSchema) -> JackTrainerResponse:
        pass

    @abstractmethod
    async def get_model_info(self) -> dict[str, Any]:
        pass

    @abstractmethod
    async def analyze_jack_dawson(self) -> dict[str, Any]:
        pass

    @abstractmethod
    async def predict_survival(self, passenger_data: dict[str, Any]) -> dict[str, Any]:
        pass
