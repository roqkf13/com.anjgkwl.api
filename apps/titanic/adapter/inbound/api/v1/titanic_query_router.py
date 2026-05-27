from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from titanic.adapter.inbound.deps import TitanicQueryDep

router = APIRouter(prefix="/titanic", tags=["titanic-query"])


@router.get("/data")
def read_titanic_data(query: TitanicQueryDep):
    df = query.get_titanic_data()
    return df.to_dict(orient="records")


@router.get("/count")
def read_titanic_count(query: TitanicQueryDep):
    return {"count": query.get_titanic_data_count()}


@router.get("/count/survived")
def read_titanic_count_survived(query: TitanicQueryDep):
    return {"count": query.get_titanic_data_count_survived()}


@router.get("/count/dead")
def read_titanic_count_dead(query: TitanicQueryDep):
    return {"count": query.get_titanic_data_count_dead()}


@router.get("/tree")
def read_titanic_tree(query: TitanicQueryDep):
    return {"tree": query.has_decision_tree_model()}


@router.get("/model")
def read_titanic_model(query: TitanicQueryDep):
    model_info = query.get_model_name_and_accuracy()
    return JSONResponse(content=jsonable_encoder(model_info))
