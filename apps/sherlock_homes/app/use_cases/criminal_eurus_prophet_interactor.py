from __future__ import annotations

from tailor.apps.sherlock_homes.adapter.inbound.api.schemas.criminal_eurus_prophet_schema import EurusProphetSchema
from tailor.apps.sherlock_homes.app.dtos.criminal_eurus_prophet_dto import EurusProphetQuery, EurusProphetResponse
from tailor.apps.sherlock_homes.app.ports.input.criminal_eurus_prophet_use_case import EurusProphetUseCase
from tailor.apps.sherlock_homes.app.ports.output.criminal_eurus_prophet_repository import EurusProphetRepository


class EurusProphetInteractor(EurusProphetUseCase):

    def __init__(self, repository: EurusProphetRepository):
        self.repository = repository

    async def introduce_myself(self, schema: EurusProphetSchema) -> EurusProphetResponse:
        '''유라루스 홈즈의 자기소개 인터렉트'''
        return await self.repository.introduce_myself(EurusProphetQuery(
            id=schema.id,
            name=schema.name
        ))
