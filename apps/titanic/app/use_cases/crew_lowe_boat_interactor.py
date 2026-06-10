from __future__ import annotations

from titanic.app.dtos.crew_lowe_boat_dto import LoweIntroduction
from titanic.app.ports.input.crew_lowe_boat_use_case import IntroduceLoweUseCase


class IntroduceLoweInteractor(IntroduceLoweUseCase):
    """자기소개 유스케이스 구현(영속성이 필요 없는 순수 로직)."""

    async def introduce(self, member_id: int, name: str) -> LoweIntroduction:
        return LoweIntroduction(
            id=member_id * 10000,
            name=f"{name}가 유스케이스에 다녀옴",
        )
