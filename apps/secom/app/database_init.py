from sqlmodel import SQLModel

from core.database import get_engine
from secom.app.models import user_entity  # noqa: F401


async def init_secom_tables() -> None:
    engine = get_engine()
    if engine is None:
        return
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
