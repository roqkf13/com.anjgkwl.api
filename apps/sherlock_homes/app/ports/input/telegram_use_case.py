from __future__ import annotations

from abc import ABC, abstractmethod

from sherlock_homes.adapter.inbound.api.schemas.telegram_schema import TelegramSchema
from sherlock_homes.app.dtos.telegram_dto import TelegramResponse


class TelegramUseCase(ABC):

    @abstractmethod
    async def introduce_myself(self, schema: TelegramSchema) -> TelegramResponse:
        pass
