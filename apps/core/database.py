from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

_engine: AsyncEngine | None = None
_async_session_maker: async_sessionmaker[AsyncSession] | None = None


def configure_engine(database_url: str) -> None:
    """DATABASE_URL이 있을 때만 엔진·세션 팩토리를 만든다."""
    global _engine, _async_session_maker
    if not database_url:
        return
    if _engine is not None:
        return
    _engine = create_async_engine(database_url, pool_pre_ping=True)
    _async_session_maker = async_sessionmaker(_engine, expire_on_commit=False)


def get_engine() -> AsyncEngine | None:
    return _engine


async def dispose_engine() -> None:
    global _engine, _async_session_maker
    if _engine is not None:
        await _engine.dispose()
        _engine = None
        _async_session_maker = None


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """라우트에서 Depends(get_async_session)로 AsyncSession을 주입."""
    if _async_session_maker is None:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=503,
            detail="DATABASE_URL이 설정되지 않았습니다. .env에 postgresql+psycopg://... 형식으로 추가하세요.",
        )
    async with _async_session_maker() as session:
        yield session
