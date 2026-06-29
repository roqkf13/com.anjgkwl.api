from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from tailor.apps.sherlock_homes.adapter.outbound.pg.detective_mary_operator_pg_repository import MaryOperatorPgRepository
from tailor.apps.sherlock_homes.app.ports.output.detective_mary_operator_repository import MaryOperatorRepository
from tailor.core.matrix.grid_oracle_database_manager import get_db
from tailor.apps.sherlock_homes.app.ports.input.detective_mary_operator_use_case import MaryOperatorUseCase
from tailor.apps.sherlock_homes.app.use_cases.detective_mary_operator_interactor import MaryOperatorInteractor

'''
캐릭터: 메리 왓슨 (Mary)
역할 (keyword): operator (특수 작전/보안)
드라마 설정 및 시스템 기능: 사설 탐정단에 합류한 전직 비밀 요원.
베이커가 팀의 안전을 도모하듯, 시스템 내부의 예외 처리(Exception), 보안 우회 로직 및 긴급 특수 작전 코드를 수행합니다.
'''

def get_mary_operator_use_case(
        db: AsyncSession = Depends(get_db)
) -> MaryOperatorUseCase:
    repository: MaryOperatorRepository = MaryOperatorPgRepository(session=db)
    return MaryOperatorInteractor(repository=repository)
