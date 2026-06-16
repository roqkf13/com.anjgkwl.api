from __future__ import annotations

import statistics
from typing import Any

from titanic.adapter.inbound.api.schemas.passenger_rose_model_schema import RoseModelSchema
from titanic.app.dtos.passenger_rose_model_dto import RoseModelQuery, RoseModelResponse
from titanic.app.ports.input.passenger_rose_model_use_case import (
    RoseModelUseCase,
    SurvivalPredictionStrategy,
)
from titanic.app.ports.output.passenger_rose_model_repository import RoseModelRepository

# ---------------------------------------------------------------------------
# Feature engineering
# ---------------------------------------------------------------------------

_EMBARKED_MAP: dict[str, float] = {"C": 0.0, "Q": 1.0, "S": 2.0}
_FEATURE_NAMES = ["pclass", "gender", "age", "fare", "embarked", "family_size", "is_alone"]


def _compute_medians(records: list[dict[str, Any]]) -> tuple[float, float]:
    ages = [r["age"] for r in records if r.get("age") is not None]
    fares = [r["fare"] for r in records if r.get("fare") is not None]
    return (
        statistics.median(ages) if ages else 30.0,
        statistics.median(fares) if fares else 14.45,
    )


def _to_feature_vector(r: dict[str, Any], age_med: float, fare_med: float) -> list[float]:
    """Record → [pclass, gender, age, fare, embarked, family_size, is_alone]"""
    pclass = float(r.get("pclass") or 2)
    gender = 1.0 if (r.get("gender") or "").lower() == "male" else 0.0
    age = float(r["age"]) if r.get("age") is not None else age_med
    fare = float(r["fare"]) if r.get("fare") is not None else fare_med
    embarked = _EMBARKED_MAP.get(r.get("embarked") or "", 2.0)
    sibsp = float(r.get("sibsp") or 0)
    parch = float(r.get("parch") or 0)
    family_size = sibsp + parch + 1.0
    is_alone = 1.0 if family_size == 1.0 else 0.0
    return [pclass, gender, age, fare, embarked, family_size, is_alone]


def _build_training_set(
    records: list[dict[str, Any]],
) -> tuple[list[list[float]], list[int], float, float]:
    age_med, fare_med = _compute_medians(records)
    labeled = [r for r in records if r.get("survived") is not None]
    X = [_to_feature_vector(r, age_med, fare_med) for r in labeled]
    y = [int(r["survived"]) for r in labeled]
    return X, y, age_med, fare_med


# ---------------------------------------------------------------------------
# Concrete strategies — titanic-algorithm.md TOP 10 중 scikit-learn 구현체
# ---------------------------------------------------------------------------

class RandomForestStrategy(SurvivalPredictionStrategy):
    """#2 배깅 앙상블. 튜닝 없이도 안정적인 baseline."""

    def __init__(self, n_estimators: int = 100) -> None:
        from sklearn.ensemble import RandomForestClassifier
        self._model = RandomForestClassifier(n_estimators=n_estimators, random_state=42)

    @property
    def name(self) -> str:
        return "random_forest"

    def fit(self, X: list[list[float]], y: list[int]) -> None:
        self._model.fit(X, y)

    def predict(self, x: list[float]) -> dict[str, Any]:
        pred = int(self._model.predict([x])[0])
        prob = self._model.predict_proba([x])[0].tolist()
        importance = {
            name: round(v, 4)
            for name, v in zip(_FEATURE_NAMES, self._model.feature_importances_.tolist())
        }
        return {
            "algorithm": self.name,
            "survived": pred,
            "probability": {"not_survived": round(prob[0], 4), "survived": round(prob[1], 4)},
            "feature_importance": importance,
        }


class LogisticRegressionStrategy(SurvivalPredictionStrategy):
    """#5 이진 분류 베이스라인. 아웃라이어 존재 시 표준화(StandardScaler) 적용."""

    def __init__(self, max_iter: int = 1000) -> None:
        from sklearn.linear_model import LogisticRegression
        from sklearn.preprocessing import StandardScaler
        self._model = LogisticRegression(max_iter=max_iter, random_state=42)
        self._scaler = StandardScaler()

    @property
    def name(self) -> str:
        return "logistic_regression"

    def fit(self, X: list[list[float]], y: list[int]) -> None:
        self._model.fit(self._scaler.fit_transform(X), y)

    def predict(self, x: list[float]) -> dict[str, Any]:
        x_s = self._scaler.transform([x])
        pred = int(self._model.predict(x_s)[0])
        prob = self._model.predict_proba(x_s)[0].tolist()
        return {
            "algorithm": self.name,
            "survived": pred,
            "probability": {"not_survived": round(prob[0], 4), "survived": round(prob[1], 4)},
        }


class DecisionTreeStrategy(SurvivalPredictionStrategy):
    """#6 규칙 기반 직관적 모델. 분류 흐름 시각화에 유리."""

    def __init__(self, max_depth: int = 5) -> None:
        from sklearn.tree import DecisionTreeClassifier
        self._model = DecisionTreeClassifier(max_depth=max_depth, random_state=42)

    @property
    def name(self) -> str:
        return "decision_tree"

    def fit(self, X: list[list[float]], y: list[int]) -> None:
        self._model.fit(X, y)

    def predict(self, x: list[float]) -> dict[str, Any]:
        pred = int(self._model.predict([x])[0])
        prob = self._model.predict_proba([x])[0].tolist()
        return {
            "algorithm": self.name,
            "survived": pred,
            "probability": {"not_survived": round(prob[0], 4), "survived": round(prob[1], 4)},
        }


class KNNStrategy(SurvivalPredictionStrategy):
    """#8 K-최근접 이웃. 승객 유사도 기반 분류. 표준화 필수."""

    def __init__(self, n_neighbors: int = 5) -> None:
        from sklearn.neighbors import KNeighborsClassifier
        from sklearn.preprocessing import StandardScaler
        self._model = KNeighborsClassifier(n_neighbors=n_neighbors)
        self._scaler = StandardScaler()

    @property
    def name(self) -> str:
        return "knn"

    def fit(self, X: list[list[float]], y: list[int]) -> None:
        self._model.fit(self._scaler.fit_transform(X), y)

    def predict(self, x: list[float]) -> dict[str, Any]:
        x_s = self._scaler.transform([x])
        pred = int(self._model.predict(x_s)[0])
        prob = self._model.predict_proba(x_s)[0].tolist()
        return {
            "algorithm": self.name,
            "survived": pred,
            "probability": {"not_survived": round(prob[0], 4), "survived": round(prob[1], 4)},
        }


# ---------------------------------------------------------------------------
# Interactor
# ---------------------------------------------------------------------------

class RoseModelInteractor(RoseModelUseCase):

    def __init__(self, repository: RoseModelRepository) -> None:
        self.repository = repository

    async def introduce_myself(self, schema: RoseModelSchema) -> RoseModelResponse:
        return await self.repository.introduce_myself(
            RoseModelQuery(id=schema.id, name=schema.name)
        )

    async def analyze_rose_survival(self) -> list[dict[str, Any]]:
        return await self.repository.get_all_records()

    async def predict_survival(
        self,
        passenger_data: dict[str, Any],
        strategy: SurvivalPredictionStrategy,
    ) -> dict[str, Any]:
        records = await self.repository.get_all_records()
        X, y, age_med, fare_med = _build_training_set(records)
        strategy.fit(X, y)
        x = _to_feature_vector(passenger_data, age_med, fare_med)
        return strategy.predict(x)
