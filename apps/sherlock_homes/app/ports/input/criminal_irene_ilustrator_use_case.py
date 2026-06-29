from __future__ import annotations

from abc import ABC, abstractmethod

from tailor.apps.sherlock_homes.adapter.inbound.api.schemas.criminal_irene_ilustrator_schema import IreneIlustratorSchema
from tailor.apps.sherlock_homes.app.dtos.criminal_irene_ilustrator_dto import IreneIlustratorResponse


class IreneIlustratorUseCase(ABC):

    @abstractmethod
    async def introduce_myself(self, schema: IreneIlustratorSchema) -> IreneIlustratorResponse:
        '''아이린 애들러의 자기소개 메소드'''
        pass
