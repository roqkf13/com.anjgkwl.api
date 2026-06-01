from __future__ import annotations

from pydantic import BaseModel, Field


class JamesPassengerRecordSchema(BaseModel):
    """CSV 업로드·정규화 후 승객 한 행."""

    passenger: str = ""
    survived: str = ""
    pclass: str = ""
    name: str = ""
    gender: str = ""
    age: str = ""
    sibsp: str = ""
    parch: str = ""
    ticket: str = ""
    fare: str = ""
    cabin: str = ""
    embarked: str = ""


class JamesPassengerItemSchema(BaseModel):
    """DB에 저장된 승객 한 행."""

    id: int
    passenger: str | None = None
    survived: str | None = None
    pclass: str | None = None
    name: str | None = None
    gender: str | None = None
    age: str | None = None
    sibsp: str | None = None
    parch: str | None = None
    ticket: str | None = None
    fare: str | None = None
    cabin: str | None = None
    embarked: str | None = None


class JamesPassengerListResponse(BaseModel):
    """GET /titanic/james/passengers 응답."""

    total: int
    page: int
    page_size: int = Field(..., serialization_alias="pageSize")
    items: list[JamesPassengerItemSchema]

    model_config = {"populate_by_name": True}


class JamesUploadResponse(BaseModel):
    """POST /titanic/james/upload 응답."""

    count: int
    records: list[JamesPassengerRecordSchema]
    stored_count: int = Field(..., serialization_alias="storedCount")
    message: str

    model_config = {"populate_by_name": True}
