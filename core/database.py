"""호환 레이어 — 실제 구현은 `database` 모듈."""

from database import (
    configure_engine,
    dispose_engine,
    get_db,
    get_engine,
)

get_sqlmodel_session = get_db
get_async_session = get_db
