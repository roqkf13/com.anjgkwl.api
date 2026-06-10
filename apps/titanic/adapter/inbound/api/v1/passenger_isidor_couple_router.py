from fastapi import APIRouter, Depends

from titanic.adapter.inbound.api.schemas.passenger_isidor_couple_schema import IntroduceResponseSchema
from titanic.app.ports.input.passenger_isidor_couple_use_case import IntroduceIsidorUseCase
from titanic.dependencies.passenger_isidor_couple_provider import get_introduce_isidor_use_case

'''
이시도르 & 이다 스트라우스 부부 (Isidor & Ida Straus)
구명보트를 거부하고 마지막을 함께한 노부부.
'''
isidor_couple_router = APIRouter(prefix="/isidor", tags=["isidor"])


@isidor_couple_router.get("/myself", response_model=IntroduceResponseSchema)
async def introduce_myself(
    use_case: IntroduceIsidorUseCase = Depends(get_introduce_isidor_use_case),
):
    intro = await use_case.introduce(member_id=12, name="이시도르 & 이다 스트라우스 부부 (Isidor & Ida Straus)")
    return IntroduceResponseSchema(id=intro.id, name=intro.name)
