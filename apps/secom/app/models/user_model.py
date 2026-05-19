import logging

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from secom.app.models.user_entity import User
from secom.app.schemas.user_schema import UserSchema

logger = logging.getLogger(__name__)


class UserModel:

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save_user(self, user_schema: UserSchema, password_hash: str) -> User:
        result = await self._session.exec(
            select(User).where(User.email == user_schema.email)
        )
        if result.first() is not None:
            raise ValueError("이미 등록된 이메일입니다.")

        user = User(
            user_id=user_schema.user_id,
            email=user_schema.email,
            name=user_schema.name,
            password_hash=password_hash,
            role=user_schema.role,
        )
        self._session.add(user)
        await self._session.commit()
        await self._session.refresh(user)

        logger.info(
            "[UserModel] save_user 레이어 완료 — user_id=%s name=%s (id=%s)",
            user.user_id,
            user.name,
            user.id,
        )
        return user
