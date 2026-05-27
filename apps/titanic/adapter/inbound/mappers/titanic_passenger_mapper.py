from titanic.adapter.inbound.schemas.titanic_request import TitanicPassengerRequest
from titanic.adapter.inbound.schemas.titanic_response import TitanicPassengerResponse
from titanic.domain.entities.titanic import TitanicPassenger


def request_to_entity(request: TitanicPassengerRequest) -> TitanicPassenger:
    return TitanicPassenger(
        passenger_id=request.PassengerId,
        survived=request.Survived,
        pclass=request.Pclass,
        name=request.Name,
        gender=request.gender,
        age=request.Age,
        sib_sp=request.SibSp,
        parch=request.Parch,
        ticket=request.Ticket,
        fare=request.Fare,
        cabin=request.Cabin,
        embarked=request.Embarked,
    )


def entity_to_response(entity: TitanicPassenger) -> TitanicPassengerResponse:
    return TitanicPassengerResponse(
        PassengerId=entity.passenger_id,
        Survived=entity.survived,
        Pclass=entity.pclass,
        Name=entity.name,
        gender=entity.gender,
        Age=entity.age,
        SibSp=entity.sib_sp,
        Parch=entity.parch,
        Ticket=entity.ticket,
        Fare=entity.fare,
        Cabin=entity.cabin,
        Embarked=entity.embarked,
    )
