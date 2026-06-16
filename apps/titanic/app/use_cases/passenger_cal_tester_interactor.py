from __future__ import annotations

import logging
import statistics
from typing import Any

from titanic.adapter.inbound.api.schemas.passenger_cal_tester_schema import CalTesterSchema
from titanic.app.dtos.passenger_cal_tester_dto import CalTesterQuery, CalTesterResponse
from titanic.app.ports.input.passenger_cal_tester_use_case import CalTesterUseCase
from titanic.app.ports.output.passenger_cal_tester_repository import CalTesterRepository
from titanic.app.ports.input.passenger_rose_model_use_case import SurvivalPredictionStrategy
from titanic.app.use_cases.passenger_rose_model_interactor import (
    DecisionTreeStrategy,
    KNNStrategy,
    LogisticRegressionStrategy,
    RandomForestStrategy,
    _build_training_set,
)

logger = logging.getLogger(__name__)


def _cross_validate(
    strategy_cls: type[SurvivalPredictionStrategy],
    X: list[list[float]],
    y: list[int],
    n_splits: int = 5,
) -> list[float]:
    """StratifiedKFold n_splits번 학습·평가 후 각 폴드 정확도를 반환한다."""
    from sklearn.model_selection import StratifiedKFold

    kf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
    fold_scores: list[float] = []

    for train_idx, val_idx in kf.split(X, y):
        X_train = [X[i] for i in train_idx]
        y_train = [y[i] for i in train_idx]
        X_val   = [X[i] for i in val_idx]
        y_val   = [y[i] for i in val_idx]

        strategy = strategy_cls()
        strategy.fit(X_train, y_train)

        correct = sum(
            1 for i, x in enumerate(X_val)
            if strategy.predict(x)["survived"] == y_val[i]
        )
        fold_scores.append(correct / len(y_val))

    return fold_scores


class CalTesterInteractor(CalTesterUseCase):

    def __init__(self, repository: CalTesterRepository) -> None:
        self.repository = repository
        self._scores: dict[str, Any] = {}

    async def introduce_myself(self, schema: CalTesterSchema) -> CalTesterResponse:
        '''칼 테스터의 자기소개 메소드'''
        query = CalTesterQuery(id=schema.id, name=schema.name)
        return await self.repository.introduce_myself(query)

    async def test_model(self, schema: CalTesterSchema) -> CalTesterResponse:
        """로즈가 훈련시킨 모델에 점수를 메기는 메소드.

        4개 전략 각각에 대해 5-겹 Stratified K-Fold 교차검증을 수행하고
        정확도 순위를 매긴다.
        """
        records = await self.repository.get_scoring_data()
        X, y, _, _ = _build_training_set(records)

        strategy_classes: list[tuple[str, type[SurvivalPredictionStrategy]]] = [
            ("random_forest",       RandomForestStrategy),
            ("logistic_regression", LogisticRegressionStrategy),
            ("decision_tree",       DecisionTreeStrategy),
            ("knn",                 KNNStrategy),
        ]

        scores: dict[str, Any] = {}
        for name, cls in strategy_classes:
            fold_scores = _cross_validate(cls, X, y, n_splits=5)
            mean_acc = statistics.mean(fold_scores)
            std_acc  = statistics.stdev(fold_scores)
            scores[name] = {
                "cv_mean_accuracy": round(mean_acc, 4),
                "cv_std":           round(std_acc, 4),
                "fold_scores":      [round(s, 4) for s in fold_scores],
            }
            logger.info(f"[CalTesterInteractor] {name} | mean={mean_acc:.4f} std={std_acc:.4f}")

        ranked = sorted(
            scores.items(),
            key=lambda kv: kv[1]["cv_mean_accuracy"],
            reverse=True,
        )
        self._scores = {
            "ranking": [
                {"rank": i + 1, "model": name, **info}
                for i, (name, info) in enumerate(ranked)
            ],
            "sample_count": len(X),
            "cv_folds": 5,
        }

        best_name, best_info = ranked[0]
        return CalTesterResponse(
            id=len(X),
            name=(
                f"[{schema.name}] 채점 완료 ({len(X)}건, 5-fold CV) | "
                f"1위={best_name} ({best_info['cv_mean_accuracy']:.1%})"
            ),
        )

    def get_latest_scores(self) -> dict[str, Any]:
        """마지막 채점 결과를 반환한다. test_model 선호출 필요."""
        return self._scores
