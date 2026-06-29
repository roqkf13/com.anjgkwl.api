from __future__ import annotations

from abc import ABC, abstractmethod

from tailor.apps.sherlock_homes.adapter.inbound.api.schemas.detective_mary_operator_schema import MaryOperatorSchema
from tailor.apps.sherlock_homes.app.dtos.detective_mary_operator_dto import MaryOperatorResponse


class MaryOperatorUseCase(ABC):

    @abstractmethod
    async def introduce_myself(self, schema: MaryOperatorSchema) -> MaryOperatorResponse:
        '''메리 왓슨의 자기소개 메소드'''
        pass
