from core.database import get_engine


async def init_secom_tables() -> None:
    """DATABASE_URL이 있을 때 테이블을 만든다. ORM 모델 연결 전까지는 no-op."""
    engine = get_engine()
    if engine is None:
        return
