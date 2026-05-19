import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from secom.app.schemas.user_schema import UserSchema
from secom.app.services.user_service import UserService

logger = logging.getLogger(__name__)
router = APIRouter(tags=["secom"])


class SignupRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: str = Field(..., min_length=3, max_length=255)
    password: str = Field(..., min_length=8, max_length=128)
    passwordConfirm: str = Field(..., min_length=8, max_length=128)
    role: str = Field(default="user", description="admin | user")


class SignupResponse(BaseModel):
    message: str
    user_id: str
    name: str
    email: str
    role: str


def _payload_for_log(user_schema: UserSchema) -> dict:
    data = user_schema.model_dump()
    password = data.get("password")
    if password:
        data["password"] = f"*** (len={len(password)})"
    return data


class UserController:

    def __init__(self):
        pass

    def save_user(self, user_schema: UserSchema):
        logger.info(
            "[secom][Controller] save_user - 레이어 진입 | payload=%s",
            _payload_for_log(user_schema),
        )
        print(
            f"[secom][Controller] save_user - 레이어 진입 | payload={_payload_for_log(user_schema)}",
            flush=True,
        )
        user_service = UserService()
        return user_service.save_user(user_schema)

    def signup(self, body: SignupRequest) -> SignupResponse:
        if body.password != body.passwordConfirm:
            raise HTTPException(status_code=400, detail="비밀번호가 일치하지 않습니다.")
        if body.role not in ("admin", "user"):
            raise HTTPException(status_code=400, detail="role 은 admin 또는 user 여야 합니다.")

        user_schema = UserSchema(
            user_id=body.email.lower().strip(),
            password=body.password,
            email=body.email.lower().strip(),
            name=body.name.strip(),
            role=body.role,
        )

        self.save_user(user_schema)

        return SignupResponse(
            message="회원가입이 완료되었습니다.",
            user_id=user_schema.user_id,
            name=user_schema.name,
            email=user_schema.email,
            role=user_schema.role,
        )


@router.post("/signup", response_model=SignupResponse)
def post_signup(body: SignupRequest) -> SignupResponse:
    return UserController().signup(body)
