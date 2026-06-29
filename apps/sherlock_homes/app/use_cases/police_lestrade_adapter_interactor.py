from __future__ import annotations

from tailor.apps.sherlock_homes.adapter.inbound.api.schemas.police_lestrade_adapter_schema import LestradeAdapterSchema
from tailor.apps.sherlock_homes.app.dtos.police_lestrade_adapter_dto import LestradeAdapterQuery, LestradeAdapterResponse
from tailor.apps.sherlock_homes.app.ports.input.police_lestrade_adapter_use_case import LestradeAdapterUseCase
from tailor.apps.sherlock_homes.app.ports.output.police_lestrade_adapter_repository import LestradeAdapterRepository


class LestradeAdapterInteractor(LestradeAdapterUseCase):

    def __init__(self, repository: LestradeAdapterRepository):
        self.repository = repository

    async def introduce_myself(self, schema: LestradeAdapterSchema) -> LestradeAdapterResponse:
        '''레스트레이드 경감의 자기소개 인터렉트'''
        return await self.repository.introduce_myself(LestradeAdapterQuery(
            id=schema.id,
            name=schema.name
        ))
