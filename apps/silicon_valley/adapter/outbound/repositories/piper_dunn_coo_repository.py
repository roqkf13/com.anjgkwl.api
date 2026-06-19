from __future__ import annotations

import logging

logger = logging.getLogger(__name__)

from sqlalchemy.ext.asyncio import AsyncSession

from silicon_valley.app.dtos.piper_dunn_coo_dto import DunnCooQuery, DunnCooResponse


class DunnCooRepository:

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def introduce_myself(self, query: DunnCooQuery) -> DunnCooResponse:
        '''재러드 던의 자기소개 레포지토리 구현 메소드'''
        logger.info(f"[DunnCooRepository] introduce_myself 진입 | request_data={query}")

        return DunnCooResponse(
            id=query.id * 10000,
            name=query.name + "가 레포지토리에 다녀옴",
        )
