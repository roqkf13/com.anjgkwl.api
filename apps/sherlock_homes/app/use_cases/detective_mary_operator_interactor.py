from __future__ import annotations

from tailor.apps.sherlock_homes.adapter.inbound.api.schemas.detective_mary_operator_schema import MaryOperatorSchema
from tailor.apps.sherlock_homes.app.dtos.detective_mary_operator_dto import MaryOperatorQuery, MaryOperatorResponse
from tailor.apps.sherlock_homes.app.ports.input.detective_mary_operator_use_case import MaryOperatorUseCase
from tailor.apps.sherlock_homes.app.ports.output.detective_mary_operator_repository import MaryOperatorRepository


class MaryOperatorInteractor(MaryOperatorUseCase):

    def __init__(self, repository: MaryOperatorRepository):
        self.repository = repository

    async def introduce_myself(self, schema: MaryOperatorSchema) -> MaryOperatorResponse:
        '''메리 왓슨의 자기소개 인터렉트'''
        return await self.repository.introduce_myself(MaryOperatorQuery(
            id=schema.id,
            name=schema.name
        ))
