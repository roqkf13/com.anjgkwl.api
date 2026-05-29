import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import get_settings
from matrix.app.chat_router import router as chat_router
from scout.app import controllers as scout_controllers
from secom.app.controllers.user_controller import router as secom_signup_router
from secom.app.database_init import init_secom_tables
from core.database import configure_engine, dispose_engine, get_engine
from core.deps import (
    AsyncSessionDep,
    DatabaseHealthAdapterDep,
    DoroDirectorDep,
)
from titanic.adapter.inbound.api.v1 import titanic_v1_routers

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:     %(message)s",
)
logger = logging.getLogger(__name__)


async def _init_titanic_tables() -> None:
    from titanic.adapter.outbound.orm.titanic_model import Base

    engine = get_engine()
    if engine is None:
        logger.warning("DATABASE_URL 없음 — titanic_passengers 테이블 생성을 건너뜁니다.")
        return
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Neon titanic_passengers 테이블 준비 완료")


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    configure_engine(settings.database_url)
    await init_secom_tables()
    await _init_titanic_tables()
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
for scout_router in scout_controllers.scout_routers:
    app.include_router(scout_router)
for titanic_router in titanic_v1_routers:
    app.include_router(titanic_router)


@app.get("/")
def read_root():
    return {"message": "FAST API 메인 페이지 ", "docs": "/docs"}


@app.get("/health/db")
async def read_db_health(
    db: AsyncSessionDep,
    adapter: DatabaseHealthAdapterDep,
):
    return await adapter.check_neon_now(db)


@app.get("/doro/data")
def read_doro_data(doro: DoroDirectorDep):
    df = doro.get_data()
    return df.to_dict(orient="records")





if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
