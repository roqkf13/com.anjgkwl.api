from fastapi import APIRouter, Depends

from titanic.adapter.inbound.api.schemas.passenger_ruth_validation_schema import IntroduceResponseSchema
from titanic.app.ports.input.passenger_ruth_validation_use_case import IntroduceRuthUseCase
from titanic.dependencies.passenger_ruth_validation_provider import get_introduce_ruth_use_case

'''
루스 드윗 부카터 (Ruth DeWitt Bukater)
딸 로즈에게 상류층의 체면을 강요하던 통제욕의 상징. 1등석 승객 조회 담당.
'''
ruth_validation_router = APIRouter(prefix="/ruth", tags=["ruth"])


@ruth_validation_router.get("/myself", response_model=IntroduceResponseSchema)
async def introduce_myself(
    use_case: IntroduceRuthUseCase = Depends(get_introduce_ruth_use_case),
):
    intro = await use_case.introduce(member_id=14, name="루스 드윗 부카터 (Ruth DeWitt Bukater)")
    return IntroduceResponseSchema(id=intro.id, name=intro.name)
