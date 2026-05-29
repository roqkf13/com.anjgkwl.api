from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

_engine: AsyncEngine | None = None
_async_session_maker: async_sessionmaker[AsyncSession] | None = None


def _normalize_neon_url(url: str) -> tuple[str, dict[str, object]]:
    """Neon URL의 sslmode 등 asyncpg/psycopg 비호환 쿼리를 정리한다."""
    connect_args: dict[str, object] = {}
    if "sslmode=require" in url or "sslmode=verify-full" in url:
        connect_args["ssl"] = True
    url = url.replace("?sslmode=require&channel_binding=require", "")
    url = url.replace("&sslmode=require", "").replace("?sslmode=require", "")
    url = url.replace("&sslmode=verify-full", "").replace("?sslmode=verify-full", "")
    url = url.replace("&channel_binding=require", "").replace(
        "?channel_binding=require", ""
    )
    if url.endswith("?"):
        url = url[:-1]
    return url, connect_args


def configure_engine(database_url: str) -> None:
    """DATABASE_URL(Neon postgresql+asyncpg://...) — SQLModel AsyncSession."""
    global _engine, _async_session_maker
    url = database_url.strip()
    if not url:
        return
    if _engine is not None:
        return

    url, connect_args = _normalize_neon_url(url)
    _engine = create_async_engine(
        url,
        pool_pre_ping=True,
        echo=False,
        connect_args=connect_args,
    )
    _async_session_maker = async_sessionmaker(
        _engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )


def get_engine() -> AsyncEngine | None:
    return _engine


async def dispose_engine() -> None:
    global _engine, _async_session_maker
    if _engine is not None:
        await _engine.dispose()
        _engine = None
        _async_session_maker = None


async def get_sqlmodel_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI Depends — 요청마다 SQLModel AsyncSession 주입."""
    if _async_session_maker is None:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=503,
            detail="DATABASE_URL이 설정되지 않았습니다. .env에 postgresql+asyncpg://... 형식으로 추가하세요.",
        )
    async with _async_session_maker() as session:
        yield session


get_async_session = get_sqlmodel_session
