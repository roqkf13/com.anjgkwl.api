import logging

from kiwipiepy import Kiwi

from titanic.adapter.inbound.api.schemas.passenger_jack_trainer_schema import JackTrainerSchema
from titanic.app.dtos.passenger_jack_trainer_dto import JackTrainerQuery, JackTrainerResponse
from titanic.app.ports.output.passenger_jack_trainer_repository import JackTrainerRepository

logger = logging.getLogger(__name__)


class JackTrainerInteractor:

    def __init__(self, repository: JackTrainerRepository):
        self.repository = repository
        self.kiwi = Kiwi()

    async def analyze_message_intent(self, user_message:str) -> dict:
        '''사용자의 질문(message)을 형태소 분석하여 키워드와 의도를 파악한다'''

        logger.info(f"[JackTrainerInteractor] 전처리 및 분석 시작 | message: {user_message}")
        
        # 1. Kiwi 토큰화 진행
        tokens = self.kiwi.tokenize(user_message)
        
        keywords = []
        has_quantity_modifier = False  # '몇' 존재 여부
        has_count_unit = False        # '명', '개' 존재 여부
        
        # 2. 형태소 루프를 돌며 품사 태깅 분석
        for t in tokens:
            # 일반명사(NNG), 고유명사(NNP) 추출
            if t.tag in ('NNG', 'NNP'):
                keywords.append(t.form)
                
            # '몇' (의문 관형사 MM)
            if t.tag == 'MM' and t.form == '몇':
                has_quantity_modifier = True
                
            # '명', '개', '사람' (수량 의존명사 NNB)
            if t.tag == 'NNB' and t.form in ('명', '개', '사람', '분'):
                has_count_unit = True

        # 3. 종합하여 카운트 질문(수량 질의)인지 최종 판단
        is_count_query = has_quantity_modifier or has_count_unit or ("몇" in user_message)

        analysis_result = {
            "keywords": keywords,         # 예: ['탑승객']
            "is_count_query": is_count_query # 예: True
        }
        
        logger.info(f"[JackTrainerInteractor] 분석 완료 | 결과: {analysis_result}")
        return analysis_result

    async def introduce_myself(self, schema: JackTrainerSchema) -> JackTrainerResponse:
        '''잭 트레이너의 자기소개 인터렉트'''

        return await self.repository.introduce_myself(JackTrainerQuery(
            id = schema.id,
            name = schema.name
        ))