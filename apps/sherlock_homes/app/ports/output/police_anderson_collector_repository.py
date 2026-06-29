from __future__ import annotations

from abc import ABC, abstractmethod

from tailor.apps.sherlock_homes.app.dtos.police_anderson_collector_dto import AndersonCollectorQuery, AndersonCollectorResponse


class AndersonCollectorRepository(ABC):

    @abstractmethod
    def introduce_myself(self, query: AndersonCollectorQuery) -> AndersonCollectorResponse:
        '''앤더슨의 자기 소개 레포지토리 추상 메소드'''
        pass
