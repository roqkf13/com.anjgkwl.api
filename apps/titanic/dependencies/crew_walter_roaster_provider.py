from titanic.app.ports.input.crew_walter_roaster_use_case import IntroduceWalterUseCase
from titanic.app.use_cases.crew_walter_roaster_interactor import IntroduceWalterInteractor


def get_introduce_walter_use_case() -> IntroduceWalterUseCase:
    return IntroduceWalterInteractor()
