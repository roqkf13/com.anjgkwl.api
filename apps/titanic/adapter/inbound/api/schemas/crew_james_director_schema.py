from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field


class IntroduceResponseSchema(BaseModel):
    """GET /titanic/james/myself 응답."""
    id: int
    name: str


class ManifestRecordSchema(BaseModel):
    """업로드되어 저장된 승객 한 명의 요약."""
    passenger_id: Optional[str] = None
    name: Optional[str] = None
    gender: Optional[str] = None
    age: Optional[str] = None
    sib_sp: Optional[str] = None
    parch: Optional[str] = None
    survived: Optional[str] = None


class UploadResponseSchema(BaseModel):
    """POST /titanic/james/upload 응답. 프론트엔드 계약: {count, records}."""
    count: int = Field(..., description="저장된 레코드 수")
    records: list[ManifestRecordSchema]
