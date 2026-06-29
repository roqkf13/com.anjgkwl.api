from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from tailor.apps.sherlock_homes.adapter.outbound.pg.criminal_eurus_prophet_pg_repository import EurusProphetPgRepository
from tailor.apps.sherlock_homes.app.ports.output.criminal_eurus_prophet_repository import EurusProphetRepository
from tailor.core.matrix.grid_oracle_database_manager import get_db
from tailor.apps.sherlock_homes.app.ports.input.criminal_eurus_prophet_use_case import EurusProphetUseCase
from tailor.apps.sherlock_homes.app.use_cases.criminal_eurus_prophet_interactor import EurusProphetInteractor

'''
캐릭터: 유라루스 홈즈 (Eurus)
역할 (keyword): prophet (예측/예언가)
드라마 설정 및 시스템 기능: 섬에 격리된 최강 지능의 범죄자.
인간의 행동을 완벽히 읽고 프로그래밍하듯 미래를 통제하며, 타겟 모델의 트렌드 예측 및 비선형적 시나리오를 모델링합니다.
'''

def get_eurus_prophet_use_case(
        db: AsyncSession = Depends(get_db)
) -> EurusProphetUseCase:
    repository: EurusProphetRepository = EurusProphetPgRepository(session=db)
    return EurusProphetInteractor(repository=repository)
