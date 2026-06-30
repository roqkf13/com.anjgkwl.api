from __future__ import annotations

from sherlock_homes.adapter.inbound.api.schemas.telegram_schema import TelegramSchema
from sherlock_homes.app.dtos.telegram_dto import TelegramQuery, TelegramResponse
from sherlock_homes.app.ports.input.telegram_use_case import TelegramUseCase
from sherlock_homes.app.ports.output.telegram_repository import TelegramRepository


class TelegramInteractor(TelegramUseCase):

    def __init__(self, repository: TelegramRepository):
        self.repository = repository

    async def introduce_myself(self, schema: TelegramSchema) -> TelegramResponse:
        return await self.repository.introduce_myself(TelegramQuery(
            id=schema.id,
            name=schema.name,
        ))
