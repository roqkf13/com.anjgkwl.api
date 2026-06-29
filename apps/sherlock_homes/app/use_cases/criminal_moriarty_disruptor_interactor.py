from __future__ import annotations

from tailor.apps.sherlock_homes.adapter.inbound.api.schemas.criminal_moriarty_disruptor_schema import MoriartyDisruptorSchema
from tailor.apps.sherlock_homes.app.dtos.criminal_moriarty_disruptor_dto import MoriartyDisruptorQuery, MoriartyDisruptorResponse
from tailor.apps.sherlock_homes.app.ports.input.criminal_moriarty_disruptor_use_case import MoriartyDisruptorUseCase
from tailor.apps.sherlock_homes.app.ports.output.criminal_moriarty_disruptor_repository import MoriartyDisruptorRepository


class MoriartyDisruptorInteractor(MoriartyDisruptorUseCase):

    def __init__(self, repository: MoriartyDisruptorRepository):
        self.repository = repository

    async def introduce_myself(self, schema: MoriartyDisruptorSchema) -> MoriartyDisruptorResponse:
        '''모리어티의 자기소개 인터렉트'''
        return await self.repository.introduce_myself(MoriartyDisruptorQuery(
            id=schema.id,
            name=schema.name
        ))
