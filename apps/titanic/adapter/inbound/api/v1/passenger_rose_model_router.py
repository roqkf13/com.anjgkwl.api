from fastapi import APIRouter, Depends

from titanic.adapter.inbound.api.schemas.passenger_rose_model_schema import IntroduceResponseSchema
from titanic.app.ports.input.passenger_rose_model_use_case import IntroduceRoseUseCase
from titanic.dependencies.passenger_rose_model_provider import get_introduce_rose_use_case

'''
로즈 드윗 부카터 (Rose DeWitt Bukater)
상류층의 답답함에서 벗어나려는 의지, 영화의 핵심 매개체 '다이아몬드'의 주인공.
'''
rose_model_router = APIRouter(prefix="/rose", tags=["rose"])


@rose_model_router.get("/myself", response_model=IntroduceResponseSchema)
async def introduce_myself(
    use_case: IntroduceRoseUseCase = Depends(get_introduce_rose_use_case),
):
    intro = await use_case.introduce(member_id=14, name="로즈 드윗 부카터 (Rose DeWitt Bukater)")
    return IntroduceResponseSchema(id=intro.id, name=intro.name)
