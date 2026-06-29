from __future__ import annotations

from abc import ABC, abstractmethod

from tailor.apps.sherlock_homes.app.dtos.criminal_moriarty_disruptor_dto import MoriartyDisruptorQuery, MoriartyDisruptorResponse


class MoriartyDisruptorRepository(ABC):

    @abstractmethod
    def introduce_myself(self, query: MoriartyDisruptorQuery) -> MoriartyDisruptorResponse:
        '''모리어티의 자기 소개 레포지토리 추상 메소드'''
        pass
