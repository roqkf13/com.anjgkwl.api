import logging
from typing import Any

from titanic.adapter.inbound.api.schemas.passenger_jack_trainer_schema import JackTrainerSchema
from titanic.app.dtos.passenger_jack_trainer_dto import JackTrainerQuery, JackTrainerResponse
from titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainerUseCase
from titanic.app.ports.output.passenger_jack_trainer_repository import JackTrainerRepository

logger = logging.getLogger(__name__)


class JackTrainerInteractor(JackTrainerUseCase):

    def __init__(self, repository: JackTrainerRepository):
        self.repository = repository

    async def introduce_myself(self, schema: JackTrainerSchema) -> JackTrainerResponse:
        return await self.repository.introduce_myself(JackTrainerQuery(
            id=schema.id,
            name=schema.name
        ))

    async def get_model_info(self) -> dict[str, Any]:
        raise NotImplementedError

    async def analyze_jack_dawson(self) -> dict[str, Any]:
        raise NotImplementedError

    async def predict_survival(self, passenger_data: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError
