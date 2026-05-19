import logging

from secom.app.schemas.user_schema import UserSchema

logger = logging.getLogger(__name__)


class UserModel:

    def __init__(self):
        pass

    def save_user(self, user_schema: UserSchema):
        logger.info(
            "[secom][Model] save_user - 레이어 진입 | user_id=%s email=%s name=%s role=%s",
            user_schema.user_id,
            user_schema.email,
            user_schema.name,
            user_schema.role,
        )
        print(
            f"[secom][Model] save_user - 레이어 진입 | "
            f"user_id={user_schema.user_id} email={user_schema.email} "
            f"name={user_schema.name} role={user_schema.role}",
            flush=True,
        )
        # TODO: DB INSERT 연결
        return user_schema
