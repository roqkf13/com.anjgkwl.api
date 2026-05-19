import logging

from secom.app.repositories.user_repository import UserRepository
from secom.app.schemas.user_schema import UserSchema

logger = logging.getLogger(__name__)


def _payload_for_log(user_schema: UserSchema) -> dict:
    data = user_schema.model_dump()
    password = data.get("password")
    if password:
        data["password"] = f"*** (len={len(password)})"
    return data


class UserService:

    def __init__(self):
        pass

    def save_user(self, user_schema: UserSchema):
        logger.info(
            "[secom][Service] save_user - 레이어 진입 | payload=%s",
            _payload_for_log(user_schema),
        )
        print(
            f"[secom][Service] save_user - 레이어 진입 | payload={_payload_for_log(user_schema)}",
            flush=True,
        )
        user_repository = UserRepository()
        return user_repository.save_user(user_schema)
