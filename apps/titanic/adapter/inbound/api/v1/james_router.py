from __future__ import annotations

import csv
from io import StringIO
from typing import Any

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from sqlmodel.ext.asyncio.session import AsyncSession

from core.database import get_sqlmodel_session
from titanic.adapter.outbound.pg.james_pg_repository import JamesPgRepository
from titanic.app.ports.input.james_use_case import JamesUseCase
from titanic.app.ports.output.james_repository import JamesRepository
from titanic.app.use_cases.james_command import JamesCommand

james_router = APIRouter(prefix="/titanic/james", tags=["james"])

_HEADER_ALIASES: dict[str, str] = {
    "passengerid": "passenger",
    "passenger": "passenger",
    "survived": "survived",
    "pclass": "pclass",
    "name": "name",
    "sex": "gender",
    "gender": "gender",
    "age": "age",
    "sibsp": "sibsp",
    "parch": "parch",
    "ticket": "ticket",
    "fare": "fare",
    "cabin": "cabin",
    "embarked": "embarked",
}


def _normalize_row(row: dict[str, Any]) -> dict[str, str]:
    normalized: dict[str, str] = {}
    for raw_key, value in row.items():
        if raw_key is None:
            continue
        alias = _HEADER_ALIASES.get(raw_key.strip().lower())
        if alias is None:
            continue
        normalized[alias] = "" if value is None else str(value).strip()
    return normalized


async def _parse_csv_file(file: UploadFile) -> list[dict[str, str]]:
    filename = (file.filename or "").lower()
    if not filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="CSV 파일만 업로드할 수 있습니다.")

    raw = await file.read()
    if not raw:
        raise HTTPException(status_code=400, detail="빈 CSV 파일입니다.")

    text = raw.decode("utf-8-sig", errors="replace")
    reader = csv.DictReader(StringIO(text))
    if reader.fieldnames is None:
        raise HTTPException(status_code=400, detail="CSV 헤더를 읽을 수 없습니다.")

    return [_normalize_row(row) for row in reader]


@james_router.get("/passengers")
async def list_passengers(
    db: AsyncSession = Depends(get_sqlmodel_session),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=50, ge=1, le=200),
):
    repository = JamesPgRepository(db)
    total, items = await repository.list_paginated(page, page_size)
    return {"total": total, "page": page, "page_size": page_size, "items": items}


@james_router.post("/upload")
async def upload_titanic_file(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_sqlmodel_session),
):
    """Titanic CSV 파일을 업로드하고 NeonDB에 저장합니다."""
    records = await _parse_csv_file(file)
    if not records:
        raise HTTPException(status_code=400, detail="저장할 행이 없습니다.")

    repository: JamesRepository = JamesPgRepository(db)
    use_case: JamesUseCase = JamesCommand(repository)
    return await use_case.receive_uploaded_records(records)
