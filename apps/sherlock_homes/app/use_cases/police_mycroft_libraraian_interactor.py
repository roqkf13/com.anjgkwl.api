from __future__ import annotations

from tailor.apps.sherlock_homes.adapter.inbound.api.schemas.police_mycroft_libraraian_schema import MycroftLibraraianSchema
from tailor.apps.sherlock_homes.app.dtos.police_mycroft_libraraian_dto import MycroftLibraraianQuery, MycroftLibraraianResponse
from tailor.apps.sherlock_homes.app.ports.input.police_mycroft_libraraian_use_case import MycroftLibraraianUseCase
from tailor.apps.sherlock_homes.app.ports.output.police_mycroft_libraraian_repository import MycroftLibraraianRepository


class MycroftLibraraianInteractor(MycroftLibraraianUseCase):

    def __init__(self, repository: MycroftLibraraianRepository):
        self.repository = repository

    async def introduce_myself(self, schema: MycroftLibraraianSchema) -> MycroftLibraraianResponse:
        '''마이크로프트 홈즈의 자기소개 인터렉트'''
        return await self.repository.introduce_myself(MycroftLibraraianQuery(
            id=schema.id,
            name=schema.name
        ))
