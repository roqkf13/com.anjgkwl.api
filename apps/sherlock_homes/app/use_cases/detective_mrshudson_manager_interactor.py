from __future__ import annotations

from tailor.apps.sherlock_homes.adapter.inbound.api.schemas.detective_mrshudson_manager_schema import MrshudsonManagerSchema
from tailor.apps.sherlock_homes.app.dtos.detective_mrshudson_manager_dto import MrshudsonManagerQuery, MrshudsonManagerResponse
from tailor.apps.sherlock_homes.app.ports.input.detective_mrshudson_manager_use_case import MrshudsonManagerUseCase
from tailor.apps.sherlock_homes.app.ports.output.detective_mrshudson_manager_repository import MrshudsonManagerRepository


class MrshudsonManagerInteractor(MrshudsonManagerUseCase):

    def __init__(self, repository: MrshudsonManagerRepository):
        self.repository = repository

    async def introduce_myself(self, schema: MrshudsonManagerSchema) -> MrshudsonManagerResponse:
        '''허드슨 부인의 자기소개 인터렉트'''
        return await self.repository.introduce_myself(MrshudsonManagerQuery(
            id=schema.id,
            name=schema.name
        ))
