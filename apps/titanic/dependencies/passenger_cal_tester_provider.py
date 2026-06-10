from titanic.app.ports.input.passenger_cal_tester_use_case import IntroduceCalUseCase
from titanic.app.use_cases.passenger_cal_tester_interactor import IntroduceCalInteractor


def get_introduce_cal_use_case() -> IntroduceCalUseCase:
    return IntroduceCalInteractor()
