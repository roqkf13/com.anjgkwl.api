from __future__ import annotations

from titanic.app.dtos.crew_hartley_violin_dto import HartleyIntroduction
from titanic.app.ports.input.crew_hartley_violin_use_case import IntroduceHartleyUseCase


class IntroduceHartleyInteractor(IntroduceHartleyUseCase):
    """자기소개 유스케이스 구현(영속성이 필요 없는 순수 로직)."""

    async def introduce(self, member_id: int, name: str) -> HartleyIntroduction:
        return HartleyIntroduction(
            id=member_id * 10000,
            name=f"{name}가 유스케이스에 다녀옴",
        )
