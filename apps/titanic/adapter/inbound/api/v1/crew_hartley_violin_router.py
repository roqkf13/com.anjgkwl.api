from fastapi import APIRouter, Depends

from titanic.adapter.inbound.api.schemas.crew_hartley_violin_schema import IntroduceResponseSchema
from titanic.app.ports.input.crew_hartley_violin_use_case import IntroduceHartleyUseCase
from titanic.dependencies.crew_hartley_violin_provider import get_introduce_hartley_use_case

'''
왈리스 하틀리 (Wallace Hartley)
침몰 속에서도 끝까지 연주한 악단장. 배경 작업/알림 라우터 역할.
'''
hartley_violin_router = APIRouter(prefix="/hartley", tags=["hartley"])


@hartley_violin_router.get("/myself", response_model=IntroduceResponseSchema)
async def introduce_myself(
    use_case: IntroduceHartleyUseCase = Depends(get_introduce_hartley_use_case),
):
    intro = await use_case.introduce(member_id=3, name="왈리스 하틀리 (Wallace Hartley)")
    return IntroduceResponseSchema(id=intro.id, name=intro.name)
