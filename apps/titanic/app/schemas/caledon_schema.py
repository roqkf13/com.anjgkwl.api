from typing import Optional

from pydantic import BaseModel, Field


class TitanicPassengerSchema(BaseModel):
    """타이타닉 탑승자 1명 분석·검증용 스키마."""

    Survived: int = Field(..., description="생존 여부 (0 = 사망, 1 = 생존)")
    Pclass: int = Field(..., description="티켓 클래스 (1 = 1등석, 2 = 2등석, 3 = 3등석)")
    Sex: str = Field(..., description="성별")
    Age: Optional[float] = Field(default=None, description="나이")
    SibSp: int = Field(
        ..., description="함께 탑승한 자녀 / 배우자 의 수"
    )
    Parch: int = Field(
        ..., description="함께 탑승한 부모님 / 아이들 의 수"
    )
    Ticket: str = Field(..., description="티켓 번호")
    Fare: float = Field(..., description="탑승 요금")
    Cabin: Optional[str] = Field(default=None, description="수하물 번호")
    Boat: Optional[str] = Field(
        default=None, description="탈출한 보트가 있다면 boat 번호"
    )
    Embarked: Optional[str] = Field(
        default=None,
        description="선착장 (C = Cherbourg, Q = Queenstown, S = Southampton)",
    )
