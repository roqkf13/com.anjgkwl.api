from pydantic import BaseModel, ConfigDict, Field


class TitanicPassengerResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    PassengerId: str
    Survived: str
    Pclass: str
    Name: str
    gender: str
    Age: str
    SibSp: str
    Parch: str
    Ticket: str
    Fare: str
    Cabin: str
    Embarked: str


class TitanicCommandMessageResponse(BaseModel):
    message: str
    passenger_id: str


class TitanicBulkCommandResponse(BaseModel):
    message: str
    count: int
