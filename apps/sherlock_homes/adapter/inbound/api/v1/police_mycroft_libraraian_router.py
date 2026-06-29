from fastapi import APIRouter, Depends

from tailor.apps.sherlock_homes.adapter.inbound.api.schemas.police_mycroft_libraraian_schema import MycroftLibraraianSchema
from tailor.apps.sherlock_homes.app.dtos.police_mycroft_libraraian_dto import MycroftLibraraianResponse
from tailor.apps.sherlock_homes.app.ports.input.police_mycroft_libraraian_use_case import MycroftLibraraianUseCase
from tailor.apps.sherlock_homes.dependencies.police_mycroft_libraraian_provider import get_mycroft_libraraian_use_case

'''
마이크로프트 홈즈 (Mycroft)
역할 (keyword): libraraian (지식/정보 창고)
영국 정부의 핵심 관료이자 최고 국가 정보망을 통제하는 인물.
정부 기관 레벨의 거대 글로벌 컨텍스트 및 마스터 지식 베이스를 관리합니다.
'''

mycroft_libraraian_router = APIRouter(prefix="/mycroft", tags=["mycroft"])


@mycroft_libraraian_router.get("/myself")
async def introduce_myself(
    mycroft: MycroftLibraraianUseCase = Depends(get_mycroft_libraraian_use_case)
) -> MycroftLibraraianResponse:
    return await mycroft.introduce_myself(
        MycroftLibraraianSchema(
            id=3,
            name="마이크로프트 홈즈 (Mycroft)"
        )
    )
