from __future__ import annotations

import logging

from pandas import DataFrame

from titanic.adapter.inbound.api.schemas.crew_smith_captain_schema import ChatResponse, ChatSchema, SmithCaptainSchema
from titanic.adapter.inbound.api.schemas.passenger_jack_trainer_schema import JackTrainerSchema
from titanic.adapter.inbound.api.schemas.passenger_cal_tester_schema import CalTesterSchema
from titanic.app.dtos.crew_smith_captain_dto import SmithCaptainQuery, SmithCaptainResponse
from titanic.app.ports.input.crew_andrews_architect_use_case import AndrewsArchitectUseCase
from titanic.app.ports.input.crew_smith_captain_use_case import SmithCaptainUseCase
from titanic.app.ports.input.crew_walter_roaster_use_case import WalterRoasterUseCase
from titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainerUseCase
from titanic.app.ports.input.passenger_rose_model_use_case import RoseModelUseCase
from titanic.app.ports.input.passenger_cal_tester_use_case import CalTesterUseCase
from titanic.app.ports.output.crew_smith_captain_port import SmithCaptainPort

logger = logging.getLogger(__name__)

class SmithCaptainInteractor(SmithCaptainUseCase):

    def __init__(
            self, 
            repository: SmithCaptainPort,
            andrews: AndrewsArchitectUseCase,
            jack: JackTrainerUseCase,
            rose: RoseModelUseCase,
            cal: CalTesterUseCase,
            walter: WalterRoasterUseCase 
    ):
        self.repository = repository
        self.andrews = andrews
        self.jack = jack
        self.rose = rose
        self.cal = cal
        self.walter = walter
  

    async def chat(self, schema: ChatSchema) -> ChatResponse:
        import pandas as pd
        logger.info(f"[SmithCaptainInteractor] chat 진입 | messages={schema.messages}")
        train_set : DataFrame = self.walter.get_train_set()
        test_set : DataFrame = self.walter.get_test_set()
        train_result : dict = self.jack.train_model(train_set)
        test_result : dict = self.cal.test_model(test_set)
        question : dict = self.andrews.analyze_intent(schema.messages)

        # 생존 통계
        survived_series = pd.to_numeric(train_set["survived"], errors="coerce").fillna(0)
        total = len(train_set)
        survived_count = int(survived_series.sum())
        dead_count = total - survived_count

        # 최고 정확도 모델
        ranking = test_result.get("ranking", [])
        best = ranking[0] if ranking else None

        lines = [
            f"[학습 데이터 {train_result.get('train_samples', total)}명 기준]",
            f"생존자 {survived_count}명 / 사망자 {dead_count}명",
        ]
        if best:
            lines.append(
                f"최고 정확도 모델: {best['model']} "
                f"(CV 정확도 {best['cv_mean_accuracy'] * 100:.1f}%)"
            )

        return ChatResponse(text="\n".join(lines))


    async def introduce_myself(self, schema: SmithCaptainSchema) -> SmithCaptainResponse:
        '''스미스 선장의 자기소개 인터렉트'''

        return await self.repository.introduce_myself(SmithCaptainQuery(
            id = schema.id,
            name = schema.name
        ))
