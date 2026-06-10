from fastapi import APIRouter, Depends

from titanic.adapter.inbound.api.schemas.crew_andrews_architect_schema import IntroduceResponseSchema
from titanic.app.ports.input.crew_andrews_architect_use_case import IntroduceAndrewsUseCase
from titanic.dependencies.crew_andrews_architect_provider import get_introduce_andrews_use_case

'''
토마스 앤드류스 (Thomas Andrews)
타이타닉을 설계한 수석 디자이너. 시스템 구조/메타데이터 담당.
'''
andrews_architect_router = APIRouter(prefix="/andrews", tags=["andrews"])


@andrews_architect_router.get("/myself", response_model=IntroduceResponseSchema)
async def introduce_myself(
    use_case: IntroduceAndrewsUseCase = Depends(get_introduce_andrews_use_case),
):
    intro = await use_case.introduce(member_id=2, name="토마스 앤드류스 (Thomas Andrews)")
    return IntroduceResponseSchema(id=intro.id, name=intro.name)
