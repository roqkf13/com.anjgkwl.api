from fastapi import APIRouter, Depends

from titanic.adapter.inbound.api.schemas.passenger_cal_tester_schema import IntroduceResponseSchema
from titanic.app.ports.input.passenger_cal_tester_use_case import IntroduceCalUseCase
from titanic.dependencies.passenger_cal_tester_provider import get_introduce_cal_use_case

'''
칼 캘던 하클리 (Caledon Hockley)
오만한 자산가 빌런. 승객 입력값 유효성 검사를 담당.
'''
cal_test_router = APIRouter(prefix="/cal", tags=["cal"])


@cal_test_router.get("/myself", response_model=IntroduceResponseSchema)
async def introduce_myself(
    use_case: IntroduceCalUseCase = Depends(get_introduce_cal_use_case),
):
    intro = await use_case.introduce(member_id=2, name="칼 캘던 하클리 (Caledon Hockley)")
    return IntroduceResponseSchema(id=intro.id, name=intro.name)
