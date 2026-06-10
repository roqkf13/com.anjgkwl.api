from titanic.app.ports.input.passenger_jack_trainer_use_case import IntroduceJackUseCase
from titanic.app.use_cases.passenger_jack_trainer_interactor import IntroduceJackInteractor


def get_introduce_jack_use_case() -> IntroduceJackUseCase:
    return IntroduceJackInteractor()
