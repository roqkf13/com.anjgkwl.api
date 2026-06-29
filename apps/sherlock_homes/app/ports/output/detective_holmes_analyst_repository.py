from __future__ import annotations

from abc import ABC, abstractmethod

from tailor.apps.sherlock_homes.app.dtos.detective_holmes_analyst_dto import HolmesAnalystQuery, HolmesAnalystResponse


class HolmesAnalystRepository(ABC):

    @abstractmethod
    def introduce_myself(self, query: HolmesAnalystQuery) -> HolmesAnalystResponse:
        '''셜록 홈즈의 자기 소개 레포지토리 추상 메소드'''
        pass
