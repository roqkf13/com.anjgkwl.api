from fastapi import APIRouter, Depends

from titanic.adapter.inbound.api.schemas.crew_smith_captain_schema import IntroduceResponseSchema
from titanic.app.ports.input.crew_smith_captain_use_case import IntroduceSmithUseCase
from titanic.dependencies.crew_smith_captain_provider import get_introduce_smith_use_case

'''
스미스 선장 (Captain Edward John Smith)
타이타닉의 총책임자. 전체 승객 현황(생존/사망 통계)을 관장하는 마스터 역할.
'''
smith_captain_router = APIRouter(prefix="/smith", tags=["smith"])


@smith_captain_router.post("/chat", response_model=IntroduceResponseSchema)
async def chat(
    use_case: IntroduceSmithUseCase = Depends(get_introduce_smith_use_case),
):
    return None
