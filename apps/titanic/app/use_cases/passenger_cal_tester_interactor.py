from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from titanic.app.dtos.passenger_cal_tester_dto import CalIntroduction
from titanic.app.ports.input.passenger_cal_tester_use_case import IntroduceCalUseCase


class IntroduceCalInteractor(IntroduceCalUseCase):
    """자기소개 유스케이스 구현(영속성이 필요 없는 순수 로직)."""

    async def introduce(self, member_id: int, name: str) -> CalIntroduction:
        return CalIntroduction(
            id=member_id * 10000,
            name=f"{name}가 유스케이스에 다녀옴",
        )


class CaledonValidation(BaseModel):
    Pclass: int = Field(..., ge=1, le=3, description="티켓 클래스 (1 = 1등석, 2 = 2등석, 3 = 3등석)")
    Sex: Literal["male", "female"] = Field(..., description="성별 (male 또는 female)")
    Age: float = Field(..., ge=0.0, description="나이")
    SibSp: int = Field(..., ge=0, description="함께 탑승한 형제자매 / 배우자의 수")
    Parch: int = Field(..., ge=0, description="함께 탑승한 부모님 / 아이들의 수")
    Fare: float = Field(..., ge=0.0, description="탑승 요금")

    class Config:
        json_schema_extra = {
            "example": {
                "Pclass": 3,
                "Sex": "male",
                "Age": 22.0,
                "SibSp": 1,
                "Parch": 0,
                "Fare": 7.25
            }
        }
