from __future__ import annotations

from abc import ABC, abstractmethod

from titanic.app.dtos.passenger_jack_trainer_dto import JackIntroduction


class IntroduceJackUseCase(ABC):
    """잭 도슨 (Jack Dawson) 자기소개 유스케이스."""

    @abstractmethod
    async def introduce(self, member_id: int, name: str) -> JackIntroduction:
        ...
