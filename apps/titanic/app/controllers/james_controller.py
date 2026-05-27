import logging
from typing import Any

from titanic.app.repositories.walter_repository import WalterRepository
from titanic.app.schemas.titanic_problem_schema import PROBLEM_SUMMARY
from titanic.app.services.jack_service import JackService

logger = logging.getLogger(__name__)


class JamesController:
    def __init__(self, service: JackService, reader: WalterRepository) -> None:
        self.service = service
        self.reader = reader

    def get_titanic_data(self):
        return self.reader.get_data()

    def get_titanic_data_count(self) -> int:
        return self.reader.get_count()

    def get_titanic_data_count_survived(self) -> int:
        return self.reader.get_count_survived()

    def get_titanic_data_count_dead(self) -> int:
        return self.reader.get_count_dead()

    def has_decision_tree_model(self) -> bool:
        return self.service.has_decision_tree_model()

    def get_model_name_and_accuracy(self) -> dict[str, Any]:
        payload = self.service.get_model_name_and_accuracy()
        payload["problem_summary"] = PROBLEM_SUMMARY
        return payload
