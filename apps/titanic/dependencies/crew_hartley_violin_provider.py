from titanic.app.ports.input.crew_hartley_violin_use_case import IntroduceHartleyUseCase
from titanic.app.use_cases.crew_hartley_violin_interactor import IntroduceHartleyInteractor


def get_introduce_hartley_use_case() -> IntroduceHartleyUseCase:
    return IntroduceHartleyInteractor()
