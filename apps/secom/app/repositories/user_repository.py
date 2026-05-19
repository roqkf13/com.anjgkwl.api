import logging

from secom.app.schemas.user_schema import UserSchema
from secom.app.models.user_model import UserModel

logger = logging.getLogger(__name__)


def _payload_for_log(user_schema: UserSchema) -> dict:
    data = user_schema.model_dump()
    password = data.get("password")
    if password:
        data["password"] = f"*** (len={len(password)})"
    return data


class UserRepository:

    def __init__(self):
        pass

    def save_user(self, user_schema: UserSchema):
        logger.info(
            "[secom][Repository] save_user - 레이어 진입 | payload=%s",
            _payload_for_log(user_schema),
        )
        print(
            f"[secom][Repository] save_user - 레이어 진입 | payload={_payload_for_log(user_schema)}",
            flush=True,
        )
        user_model = UserModel()
        return user_model.save_user(user_schema)
