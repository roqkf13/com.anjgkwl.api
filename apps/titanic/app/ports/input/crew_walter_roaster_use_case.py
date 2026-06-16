from abc import ABC, abstractmethod
from titanic.adapter.inbound.api.schemas.crew_walter_roaster_schema import WalterRoasterSchema
from titanic.app.dtos.crew_walter_roaster_dto import WalterRoasterResponse

class WalterRoasterUseCase(ABC):

    @abstractmethod
    async def introduce_myself(self, schema: WalterRoasterSchema) -> WalterRoasterResponse:
        '''월터의 자기소개 메소드'''
        pass

    @abstractmethod
    async def get_train_set(self):
        '''훈련 데이터셋을 반환하는 메소드'''
        pass

    @abstractmethod
    async def get_test_set(self):
        '''테스트 데이터셋을 반환하는 메소드'''
        pass