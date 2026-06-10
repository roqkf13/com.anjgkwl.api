from fastapi import APIRouter, Depends

from titanic.adapter.inbound.api.schemas.passenger_jack_trainer_schema import IntroduceResponseSchema
from titanic.app.ports.input.passenger_jack_trainer_use_case import IntroduceJackUseCase
from titanic.dependencies.passenger_jack_trainer_provider import get_introduce_jack_use_case

'''
잭 도슨 (Jack Dawson)
자유로운 영혼, 예술가. 생존 예측 모델의 핵심 인터페이스 담당.
'''
jack_train_router = APIRouter(prefix="/jack", tags=["jack"])


@jack_train_router.get("/myself", response_model=IntroduceResponseSchema)
async def introduce_myself(
    use_case: IntroduceJackUseCase = Depends(get_introduce_jack_use_case),
):
    intro = await use_case.introduce(member_id=13, name="잭 도슨 (Jack Dawson)")
    return IntroduceResponseSchema(id=intro.id, name=intro.name)
