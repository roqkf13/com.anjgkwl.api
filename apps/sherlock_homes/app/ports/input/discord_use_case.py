from __future__ import annotations

from abc import ABC, abstractmethod

from sherlock_homes.adapter.inbound.api.schemas.discord_schema import DiscordSchema
from sherlock_homes.app.dtos.discord_dto import DiscordResponse


class DiscordUseCase(ABC):

    @abstractmethod
    async def introduce_myself(self, schema: DiscordSchema) -> DiscordResponse:
        pass
