from fastapi import APIRouter, Depends

from titanic.adapter.inbound.api.schemas.crew_walter_roaster_schema import IntroduceResponseSchema
from titanic.app.ports.input.crew_walter_roaster_use_case import IntroduceWalterUseCase
from titanic.dependencies.crew_walter_roaster_provider import get_introduce_walter_use_case

'''
Walter Nichols
타이타닉의 일등 항해사, 승객 명단(Passenger List) 관리 담당.
'''
walter_roaster_router = APIRouter(prefix="/walter", tags=["walter"])


@walter_roaster_router.get("/myself", response_model=IntroduceResponseSchema)
async def introduce_myself(
    use_case: IntroduceWalterUseCase = Depends(get_introduce_walter_use_case),
):
    intro = await use_case.introduce(member_id=2, name="Walter Nichols")
    return IntroduceResponseSchema(id=intro.id, name=intro.name)
