from __future__ import annotations

from abc import ABC, abstractmethod

from tailor.apps.sherlock_homes.app.dtos.police_mycroft_libraraian_dto import MycroftLibraraianQuery, MycroftLibraraianResponse


class MycroftLibraraianRepository(ABC):

    @abstractmethod
    def introduce_myself(self, query: MycroftLibraraianQuery) -> MycroftLibraraianResponse:
        '''마이크로프트 홈즈의 자기 소개 레포지토리 추상 메소드'''
        pass
