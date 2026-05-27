from fastapi import APIRouter, status

from titanic.adapter.inbound.deps import TitanicCommandDep
from titanic.adapter.inbound.mappers.titanic_passenger_mapper import (
    entity_to_response,
    request_to_entity,
)
from titanic.adapter.inbound.schemas.titanic_request import (
    TitanicPassengerBulkRequest,
    TitanicPassengerRequest,
)
from titanic.adapter.inbound.schemas.titanic_response import (
    TitanicBulkCommandResponse,
    TitanicPassengerResponse,
)

router = APIRouter(prefix="/api/v1/titanic", tags=["titanic-command"])


@router.post(
    "/passengers",
    response_model=TitanicPassengerResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_passenger(
    body: TitanicPassengerRequest,
    command: TitanicCommandDep,
) -> TitanicPassengerResponse:
    saved = command.register_passenger(request_to_entity(body))
    return entity_to_response(saved)


@router.post(
    "/passengers/bulk",
    response_model=TitanicBulkCommandResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_passengers_bulk(
    body: TitanicPassengerBulkRequest,
    command: TitanicCommandDep,
) -> TitanicBulkCommandResponse:
    entities = [request_to_entity(item) for item in body.passengers]
    count = command.register_passengers(entities)
    return TitanicBulkCommandResponse(
        message="passengers registered",
        count=count,
    )
