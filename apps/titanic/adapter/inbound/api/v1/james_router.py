from __future__ import annotations

import csv
from io import StringIO
from typing import Any

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from titanic.adapter.outbound.pg.james_pg_repository import JamesPgRepository
from titanic.app.use_cases.james_use_case_impl import JamesUseCase

james_router = APIRouter(prefix="/titanic/james", tags=["james"])

_ALLOWED_ROW_KEYS = frozenset({
    "passenger",
    "survived",
    "pclass",
    "name",
    "age",
    "sibsp",
    "parch",
    "ticket",
    "fare",
    "cabin",
    "embarked",
    "gender",
})


def _normalize_row(row: dict[str, Any]) -> dict[str, Any]:
    normalized: dict[str, Any] = {}
    for raw_key, value in row.items():
        if raw_key is None:
            continue
        key = raw_key.strip()
        lower_key = key.lower()
        if lower_key == "sex":
            normalized["gender"] = value
        elif lower_key in _ALLOWED_ROW_KEYS:
            normalized[lower_key] = value
    return normalized


def _parse_csv_file(file: UploadFile) -> list[dict[str, Any]]:
    if file.content_type not in {
        "text/csv",
        "application/vnd.ms-excel",
        "text/plain",
    }:
        raise HTTPException(status_code=400, detail="CSV 파일을 업로드해주세요.")

    text = file.file.read().decode("utf-8", errors="replace")
    if not text.strip():
        raise HTTPException(status_code=400, detail="빈 CSV 파일입니다.")

    reader = csv.DictReader(StringIO(text))
    if reader.fieldnames is None:
        raise HTTPException(status_code=400, detail="CSV 헤더를 읽을 수 없습니다.")

    return [_normalize_row(row) for row in reader]


@james_router.get("/passengers")
async def list_passengers(
    db: AsyncSession = Depends(get_db),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=200),
):
    repository = JamesPgRepository(db)
    use_case = JamesUseCase(repository)
    return await use_case.list_paginated(page, page_size)


@james_router.post("/upload")
async def upload_titanic_file(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    """Titanic CSV 파일을 업로드하고 NeonDB에 저장합니다."""
    records = _parse_csv_file(file)
    repository = JamesPgRepository(db)
    use_case = JamesUseCase(repository)
    return await use_case.receive_uploaded_records(records)
