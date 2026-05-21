import logging
from typing import Annotated, Any

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from titanic.app.deps import get_james_controller
from titanic.app.repositories.walter_repository import WalterRepository
from titanic.app.schemas.titanic_problem_schema import PROBLEM_SUMMARY
from titanic.app.services.jack_service import JackService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/titanic", tags=["titanic"])


class JamesController:
    def __init__(self, service: JackService, reader: WalterRepository) -> None:
        self.service = service
        self.reader = reader

    def get_titanic_data(self):
        return self.reader.get_data()

    def get_titanic_data_count(self) -> int:
        return self.reader.get_count()

    def get_titanic_data_count_survived(self) -> int:
        return self.reader.get_count_survived()

    def get_titanic_data_count_dead(self) -> int:
        return self.reader.get_count_dead()

    def has_decision_tree_model(self) -> bool:
        return self.service.has_decision_tree_model()

    def get_model_name_and_accuracy(self) -> dict[str, Any]:
        payload = self.service.get_model_name_and_accuracy()
        payload["problem_summary"] = PROBLEM_SUMMARY
        return payload


@router.get("/data")
def read_titanic_data(
    controller: Annotated[JamesController, Depends(get_james_controller)],
):
    df = controller.get_titanic_data()
    return df.to_dict(orient="records")


@router.get("/count")
def read_titanic_count(
    controller: Annotated[JamesController, Depends(get_james_controller)],
):
    return {"count": controller.get_titanic_data_count()}


@router.get("/count/survived")
def read_titanic_count_survived(
    controller: Annotated[JamesController, Depends(get_james_controller)],
):
    return {"count": controller.get_titanic_data_count_survived()}


@router.get("/count/dead")
def read_titanic_count_dead(
    controller: Annotated[JamesController, Depends(get_james_controller)],
):
    return {"count": controller.get_titanic_data_count_dead()}


@router.get("/tree")
def read_titanic_tree(
    controller: Annotated[JamesController, Depends(get_james_controller)],
):
    return {"tree": controller.has_decision_tree_model()}


@router.get("/model")
def read_titanic_model(
    controller: Annotated[JamesController, Depends(get_james_controller)],
):
    model_info = controller.get_model_name_and_accuracy()
    return JSONResponse(content=jsonable_encoder(model_info))
