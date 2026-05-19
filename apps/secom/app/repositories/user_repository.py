import logging

from sqlmodel.ext.asyncio.session import AsyncSession

from secom.app.models.user_model import UserModel
from secom.app.schemas.user_schema import UserSchema

logger = logging.getLogger(__name__)


class UserRepository:

    def __init__(self, session: AsyncSession) -> None:
        self._user_model = UserModel(session)

    async def save_user(self, user_schema: UserSchema, password_hash: str) -> None:
        await self._user_model.save_user(user_schema, password_hash)
        logger.info(
            "[UserRepository] save_user 레이어 완료 — user_id=%s email=%s name=%s role=%s",
            user_schema.user_id,
            user_schema.email,
            user_schema.name,
            user_schema.role,
        )
