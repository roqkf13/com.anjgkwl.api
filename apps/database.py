import os
from collections.abc import AsyncGenerator

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

load_dotenv()

# Neon 등 PostgreSQL 비동기 URL 예: postgresql+psycopg://user:pass@host/db
DATABASE_URL = (os.getenv("DATABASE_URL") or "").strip()

_engine: AsyncEngine | None = None
_async_session_maker: async_sessionmaker[AsyncSession] | None = None

if DATABASE_URL:
    _engine = create_async_engine(DATABASE_URL, echo=True)
    _async_session_maker = async_sessionmaker(
        _engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

Base = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI Depends(get_db)용 비동기 DB 세션."""
    if _async_session_maker is None:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=503,
            detail="DATABASE_URL이 설정되지 않았습니다. .env에 연결 문자열을 추가하세요.",
        )
    async with _async_session_maker() as session:
        yield session
