from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from tailor.apps.sherlock_homes.adapter.outbound.pg.police_mycroft_libraraian_pg_repository import MycroftLibraraianPgRepository
from tailor.apps.sherlock_homes.app.ports.output.police_mycroft_libraraian_repository import MycroftLibraraianRepository
from tailor.core.matrix.grid_oracle_database_manager import get_db
from tailor.apps.sherlock_homes.app.ports.input.police_mycroft_libraraian_use_case import MycroftLibraraianUseCase
from tailor.apps.sherlock_homes.app.use_cases.police_mycroft_libraraian_interactor import MycroftLibraraianInteractor

'''
캐릭터: 마이크로프트 홈즈 (Mycroft)
역할 (keyword): libraraian (지식/정보 창고)
드라마 설정 및 시스템 기능: 영국 정부의 핵심 관료이자 최고 국가 정보망을 통제하는 인물.
정부 기관 레벨의 거대 글로벌 컨텍스트 및 마스터 지식 베이스를 관리합니다.
'''

def get_mycroft_libraraian_use_case(
        db: AsyncSession = Depends(get_db)
) -> MycroftLibraraianUseCase:
    repository: MycroftLibraraianRepository = MycroftLibraraianPgRepository(session=db)
    return MycroftLibraraianInteractor(repository=repository)
