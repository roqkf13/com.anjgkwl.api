from datetime import datetime
from typing import Optional

from sqlalchemy import Column, DateTime, func
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    """Pydantic + SQLAlchemy 단일 클래스 (users 테이블)."""

    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(max_length=255, index=True, unique=True)
    email: str = Field(max_length=255, index=True, unique=True)
    name: str = Field(max_length=100)
    password_hash: str = Field(max_length=255)
    role: str = Field(default="user", max_length=20)
    age: Optional[int] = Field(default=None)
    created_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(DateTime(timezone=True), server_default=func.now(), nullable=False),
    )
