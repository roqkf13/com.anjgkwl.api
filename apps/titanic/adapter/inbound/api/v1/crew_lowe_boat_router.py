from fastapi import APIRouter, Depends

from titanic.adapter.inbound.api.schemas.crew_lowe_boat_schema import IntroduceResponseSchema
from titanic.app.ports.input.crew_lowe_boat_use_case import IntroduceLoweUseCase
from titanic.dependencies.crew_lowe_boat_provider import get_introduce_lowe_use_case

'''
해롤드 로우 (Harold Lowe)
구명보트 14호를 이끌고 유일하게 생존자를 구하러 되돌아온 5등 항해사.
'''
lowe_boat_router = APIRouter(prefix="/lowe", tags=["lowe"])


@lowe_boat_router.get("/myself", response_model=IntroduceResponseSchema)
async def introduce_myself(
    use_case: IntroduceLoweUseCase = Depends(get_introduce_lowe_use_case),
):
    intro = await use_case.introduce(member_id=5, name="해롤드 로우 (Harold Lowe)")
    return IntroduceResponseSchema(id=intro.id, name=intro.name)
