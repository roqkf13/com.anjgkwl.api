import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from secom.app.deps import get_user_controller
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


class UserController:

    def __init__(self, user_service: UserService) -> None:
        self.user_service = user_service

    async def save_user(self, user_schema: UserSchema) -> None:
        await self.user_service.save_user(user_schema)
        logger.info(
            "[UserController] save_user 레이어 완료 — user_id=%s email=%s name=%s role=%s",
            user_schema.user_id,
            user_schema.email,
            user_schema.name,
            user_schema.role,
        )

    async def signup(self, body: SignupRequest) -> SignupResponse:
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

        try:
            await self.save_user(user_schema)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e)) from e

        return SignupResponse(
            message="회원가입이 완료되었습니다.",
            user_id=user_schema.user_id,
            name=user_schema.name,
            email=user_schema.email,
            role=user_schema.role,
        )


@router.post("/signup", response_model=SignupResponse)
async def post_signup(
    body: SignupRequest,
    controller: Annotated[UserController, Depends(get_user_controller)],
) -> SignupResponse:
    return await controller.signup(body)
