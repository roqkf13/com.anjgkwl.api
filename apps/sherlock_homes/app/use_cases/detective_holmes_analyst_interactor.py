from __future__ import annotations

from tailor.apps.sherlock_homes.adapter.inbound.api.schemas.detective_holmes_analyst_schema import HolmesAnalystSchema
from tailor.apps.sherlock_homes.app.dtos.detective_holmes_analyst_dto import HolmesAnalystQuery, HolmesAnalystResponse
from tailor.apps.sherlock_homes.app.ports.input.detective_holmes_analyst_use_case import HolmesAnalystUseCase
from tailor.apps.sherlock_homes.app.ports.output.detective_holmes_analyst_repository import HolmesAnalystRepository


class HolmesAnalystInteractor(HolmesAnalystUseCase):

    def __init__(self, repository: HolmesAnalystRepository):
        self.repository = repository

    async def introduce_myself(self, schema: HolmesAnalystSchema) -> HolmesAnalystResponse:
        '''셜록 홈즈의 자기소개 인터렉트'''
        return await self.repository.introduce_myself(HolmesAnalystQuery(
            id=schema.id,
            name=schema.name
        ))
