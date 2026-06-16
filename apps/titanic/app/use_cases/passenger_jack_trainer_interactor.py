from __future__ import annotations

import logging
from typing import Any

from kiwipiepy import Kiwi

from titanic.adapter.inbound.api.schemas.passenger_jack_trainer_schema import JackTrainerSchema
from titanic.app.dtos.passenger_jack_trainer_dto import JackTrainerQuery, JackTrainerResponse
from titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainerUseCase
from titanic.app.ports.output.passenger_jack_trainer_repository import JackTrainerRepository
from titanic.app.ports.input.passenger_rose_model_use_case import SurvivalPredictionStrategy
from titanic.app.use_cases.passenger_rose_model_interactor import (
    DecisionTreeStrategy,
    KNNStrategy,
    LogisticRegressionStrategy,
    RandomForestStrategy,
    _build_training_set,
    _to_feature_vector,
)

logger = logging.getLogger(__name__)


class JackTrainerInteractor(JackTrainerUseCase):

    def __init__(self, repository: JackTrainerRepository) -> None:
        self.repository = repository
        self.kiwi = Kiwi()
        self._strategies: dict[str, SurvivalPredictionStrategy] = {}
        self._age_med: float = 30.0
        self._fare_med: float = 14.45

    async def introduce_myself(self, schema: JackTrainerSchema) -> JackTrainerResponse:
        '''잭 트레이너의 자기소개 메소드'''
        query = JackTrainerQuery(id=schema.id, name=schema.name)
        return await self.repository.introduce_myself(query)

    async def train_models(self, schema: JackTrainerSchema) -> JackTrainerResponse:
        """로즈가 제안한 모델들을 훈련시키는 메소드.

        titanic-algorithm.md 기준 scikit-learn 구현체 4종을 DB 전체 데이터로 일괄 학습한다.
        훈련된 전략들은 인스턴스에 보관하여 predict_survival에서 재사용된다.

        학습 순서 (titanic-algorithm.md 우선순위):
          #2 RandomForest  — 배깅 앙상블, 안정적 baseline
          #5 LogisticRegression — 이진 분류 baseline, 아웃라이어에 강함 (표준화)
          #6 DecisionTree  — 규칙 기반, 흐름 시각화 용이
          #8 KNN           — 승객 유사도 기반, 직관적 결과 (표준화)
        """
        records = await self.repository.get_training_data()
        X, y, self._age_med, self._fare_med = _build_training_set(records)

        candidates: list[SurvivalPredictionStrategy] = [
            RandomForestStrategy(),
            LogisticRegressionStrategy(),
            DecisionTreeStrategy(),
            KNNStrategy(),
        ]
        for strategy in candidates:
            strategy.fit(X, y)

        self._strategies = {s.name: s for s in candidates}

        logger.info(
            f"[JackTrainerInteractor] 훈련 완료 | "
            f"샘플={len(X)}, 모델={list(self._strategies)}"
        )
        return JackTrainerResponse(
            id=len(X),
            name=(
                f"로즈의 {len(candidates)}개 모델 훈련 완료 "
                f"({len(X)}건) | {', '.join(s.name for s in candidates)}"
            ),
        )

    async def get_model_info(self) -> dict[str, Any]:
        """훈련된 전략 목록과 상태를 반환한다."""
        if not self._strategies:
            return {"trained": False, "models": []}
        return {
            "trained": True,
            "models": list(self._strategies.keys()),
            "training_samples": "인스턴스 재사용 필요 (train_models 선호출)",
        }

    async def analyze_jack_dawson(self) -> dict[str, Any]:
        """형태소 분석 기반 의도 파악 기능 상태 반환."""
        return {"analyzer": "kiwipiepy", "status": "ready"}

    async def predict_survival(self, passenger_data: dict[str, Any]) -> dict[str, Any]:
        """훈련된 모든 전략으로 생존 여부를 예측하고 소프트 보팅으로 최종 판정한다."""
        if not self._strategies:
            await self.train_models(JackTrainerSchema())

        x = _to_feature_vector(passenger_data, self._age_med, self._fare_med)

        results: dict[str, Any] = {}
        survival_probs: list[float] = []

        for name, strategy in self._strategies.items():
            result = strategy.predict(x)
            results[name] = result
            survival_probs.append(result["probability"]["survived"])

        avg_survival_prob = sum(survival_probs) / len(survival_probs)
        ensemble_survived = 1 if avg_survival_prob >= 0.5 else 0

        return {
            "ensemble": {
                "survived": ensemble_survived,
                "avg_survival_probability": round(avg_survival_prob, 4),
                "method": "soft_voting",
            },
            "individual": results,
        }

    async def analyze_message_intent(self, user_message: str) -> dict:
        """사용자의 질문(message)을 형태소 분석하여 키워드와 의도를 파악한다."""
        logger.info(f"[JackTrainerInteractor] 전처리 및 분석 시작 | message: {user_message}")

        tokens = self.kiwi.tokenize(user_message)

        keywords = []
        has_quantity_modifier = False
        has_count_unit = False

        for t in tokens:
            if t.tag in ("NNG", "NNP"):
                keywords.append(t.form)
            if t.tag == "MM" and t.form == "몇":
                has_quantity_modifier = True
            if t.tag == "NNB" and t.form in ("명", "개", "사람", "분"):
                has_count_unit = True

        is_count_query = has_quantity_modifier or has_count_unit or ("몇" in user_message)

        result = {"keywords": keywords, "is_count_query": is_count_query}
        logger.info(f"[JackTrainerInteractor] 분석 완료 | 결과: {result}")
        return result
