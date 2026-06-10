from __future__ import annotations

from titanic.app.dtos.passenger_jack_trainer_dto import JackIntroduction
from titanic.app.ports.input.passenger_jack_trainer_use_case import IntroduceJackUseCase


class IntroduceJackInteractor(IntroduceJackUseCase):
    """자기소개 유스케이스 구현(영속성이 필요 없는 순수 로직)."""

    async def introduce(self, member_id: int, name: str) -> JackIntroduction:
        return JackIntroduction(
            id=member_id * 10000,
            name=f"{name}가 유스케이스에 다녀옴",
        )
