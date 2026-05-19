import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from core.config import get_settings
from matrix.app.chat_router import router as chat_router
from secom.app.controllers.user_controller import router as secom_signup_router
from secom.app.database_init import init_secom_tables
from core.database import configure_engine, dispose_engine
from core.deps import (
    AsyncSessionDep,
    DatabaseHealthAdapterDep,
    DoroDirectorDep,
    JamesControllerDep,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:     %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    configure_engine(settings.database_url)
    await init_secom_tables()
    try:
        yield
    finally:
        await dispose_engine()


app = FastAPI(title="titanic main Page", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)
app.include_router(secom_signup_router)


@app.get("/")
def read_root():
    return {"message": "FAST API 메인 페이지 ", "docs": "/docs"}


@app.get("/health/db")
async def read_db_health(
    db: AsyncSessionDep,
    adapter: DatabaseHealthAdapterDep,
):
    return await adapter.check_neon_now(db)


@app.get("/titanic/data")
def read_titanic_data(james: JamesControllerDep):
    df = james.get_titanic_data()
    return df.to_dict(orient="records")


@app.get("/titanic/count")
def read_titanic_count(james: JamesControllerDep):
    count = james.get_titanic_data_count()
    return {"count": count}


@app.get("/titanic/count/survived")
def read_titanic_count_survived(james: JamesControllerDep):
    count = james.get_titanic_data_count_survived()
    return {"count": count}


@app.get("/titanic/count/dead")
def read_titanic_count_dead(james: JamesControllerDep):
    count = james.get_titanic_data_count_dead()
    return {"count": count}


@app.get("/titanic/tree")
def read_titanic_tree(james: JamesControllerDep):
    tree = james.has_decision_tree_model()
    return {"tree": tree}


@app.get("/titanic/model")
def read_titanic_model(james: JamesControllerDep):
    model_name = james.get_model_name_and_accuracy()
    return JSONResponse(content=jsonable_encoder(model_name))


@app.get("/doro/data")
def read_doro_data(doro: DoroDirectorDep):
    df = doro.get_data()
    return df.to_dict(orient="records")





if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
