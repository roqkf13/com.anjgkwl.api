import logging

from passlib.context import CryptContext

from secom.app.repositories.user_repository import UserRepository
from secom.app.schemas.user_schema import UserSchema

logger = logging.getLogger(__name__)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:

    def __init__(self, repository: UserRepository) -> None:
        self.user_repository = repository

    async def save_user(self, user_schema: UserSchema) -> None:
        password_hash = pwd_context.hash(user_schema.password)
        await self.user_repository.save_user(user_schema, password_hash)
        logger.info(
            "[UserService] save_user 레이어 완료 — user_id=%s email=%s name=%s role=%s",
            user_schema.user_id,
            user_schema.email,
            user_schema.name,
            user_schema.role,
        )
