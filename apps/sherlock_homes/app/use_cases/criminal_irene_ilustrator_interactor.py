from __future__ import annotations

from tailor.apps.sherlock_homes.adapter.inbound.api.schemas.criminal_irene_ilustrator_schema import IreneIlustratorSchema
from tailor.apps.sherlock_homes.app.dtos.criminal_irene_ilustrator_dto import IreneIlustratorQuery, IreneIlustratorResponse
from tailor.apps.sherlock_homes.app.ports.input.criminal_irene_ilustrator_use_case import IreneIlustratorUseCase
from tailor.apps.sherlock_homes.app.ports.output.criminal_irene_ilustrator_repository import IreneIlustratorRepository


class IreneIlustratorInteractor(IreneIlustratorUseCase):

    def __init__(self, repository: IreneIlustratorRepository):
        self.repository = repository

    async def introduce_myself(self, schema: IreneIlustratorSchema) -> IreneIlustratorResponse:
        '''아이린 애들러의 자기소개 인터렉트'''
        return await self.repository.introduce_myself(IreneIlustratorQuery(
            id=schema.id,
            name=schema.name
        ))
