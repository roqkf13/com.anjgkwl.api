from typing import Any

import pandas as pd

from titanic.app.ports.input.titanic_query import TitanicQueryPort
from titanic.app.repositories.walter_repository import WalterRepository
from titanic.app.schemas.titanic_problem_schema import PROBLEM_SUMMARY
from titanic.app.services.jack_service import JackService


class TitanicQueryImpl(TitanicQueryPort):
    def __init__(self, walter: WalterRepository, jack: JackService) -> None:
        self._walter = walter
        self._jack = jack

    def get_titanic_data(self) -> pd.DataFrame:
        return self._walter.get_data()

    def get_titanic_data_count(self) -> int:
        return self._walter.get_count()

    def get_titanic_data_count_survived(self) -> int:
        return self._walter.get_count_survived()

    def get_titanic_data_count_dead(self) -> int:
        return self._walter.get_count_dead()

    def has_decision_tree_model(self) -> bool:
        return self._jack.has_decision_tree_model()

    def get_model_name_and_accuracy(self) -> dict[str, Any]:
        payload = self._jack.get_model_name_and_accuracy()
        payload["problem_summary"] = PROBLEM_SUMMARY
        return payload
