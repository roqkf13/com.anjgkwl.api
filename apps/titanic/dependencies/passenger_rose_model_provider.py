from titanic.app.ports.input.passenger_rose_model_use_case import IntroduceRoseUseCase
from titanic.app.use_cases.passenger_rose_model_interactor import IntroduceRoseInteractor


def get_introduce_rose_use_case() -> IntroduceRoseUseCase:
    return IntroduceRoseInteractor()
