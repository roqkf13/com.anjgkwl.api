from pydantic import BaseModel, ConfigDict, Field


class TitanicPassengerRequest(BaseModel):
    """타이타닉 승객 CSV 컬럼 구조 (Sex → gender, 모든 필드 str)."""

    model_config = ConfigDict(populate_by_name=True, str_strip_whitespace=True)

    PassengerId: str
    Survived: str
    Pclass: str
    Name: str
    gender: str = Field(..., description="CSV Sex 컬럼에 대응")
    Age: str
    SibSp: str
    Parch: str
    Ticket: str
    Fare: str
    Cabin: str
    Embarked: str


class TitanicPassengerBulkRequest(BaseModel):
    passengers: list[TitanicPassengerRequest]
