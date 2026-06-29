from dataclasses import dataclass

'''
캐릭터: 셜록 홈즈 (Sherlock)
역할 (keyword): analyst (분석가)
드라마 설정 및 시스템 기능: 경찰이 해결하지 못하는 미궁의 사건을 해결하는 사설 자문 탐정.
시스템의 가장 복잡한 추론 알고리즘을 수행하며, 핵심 데이터를 분석하여 실마리를 찾습니다.
'''

@dataclass(frozen=True)
class HolmesAnalystQuery:
    id: int
    name: str


@dataclass(frozen=True)
class HolmesAnalystResponse:
    id: int
    name: str
