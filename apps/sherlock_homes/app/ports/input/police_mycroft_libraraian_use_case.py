from __future__ import annotations

from abc import ABC, abstractmethod

from tailor.apps.sherlock_homes.adapter.inbound.api.schemas.police_mycroft_libraraian_schema import MycroftLibraraianSchema
from tailor.apps.sherlock_homes.app.dtos.police_mycroft_libraraian_dto import MycroftLibraraianResponse


class MycroftLibraraianUseCase(ABC):

    @abstractmethod
    async def introduce_myself(self, schema: MycroftLibraraianSchema) -> MycroftLibraraianResponse:
        '''마이크로프트 홈즈의 자기소개 메소드'''
        pass
