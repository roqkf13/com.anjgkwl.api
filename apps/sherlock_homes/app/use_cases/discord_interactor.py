from __future__ import annotations

from sherlock_homes.adapter.inbound.api.schemas.discord_schema import DiscordSchema
from sherlock_homes.app.dtos.discord_dto import DiscordQuery, DiscordResponse
from sherlock_homes.app.ports.input.discord_use_case import DiscordUseCase
from sherlock_homes.app.ports.output.discord_repository import DiscordRepository


class DiscordInteractor(DiscordUseCase):

    def __init__(self, repository: DiscordRepository):
        self.repository = repository

    async def introduce_myself(self, schema: DiscordSchema) -> DiscordResponse:
        return await self.repository.introduce_myself(DiscordQuery(
            id=schema.id,
            name=schema.name,
        ))
