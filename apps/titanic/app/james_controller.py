from titanic.app.jack_service import JackService
from titanic.app.walter_reader import WalterReader


class JamesController:
    def __init__(self):
        self.service = JackService()
        self.reader = WalterReader()

    def get_titanic_data(self):
        return self.reader.get_data()

    def get_titanic_data_count(self):
        return self.reader.get_count()

    def get_titanic_data_count_survived(self):
        return self.reader.get_count_survived()

    def get_titanic_data_count_dead(self):
        return self.reader.get_count_dead()


    def get_model_name_and_accuracy(self):
        return self.service.get_model_name_and_accuracy()

    def has_decision_tree_model(self) -> bool:
        from sklearn.tree import DecisionTreeClassifier

        return isinstance(self.service.rose.model, DecisionTreeClassifier)