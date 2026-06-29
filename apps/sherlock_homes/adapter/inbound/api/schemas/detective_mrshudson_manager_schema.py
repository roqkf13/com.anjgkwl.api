from pydantic import BaseModel, Field

'''
캐릭터: 허드슨 부인 (Mrs. Hudson)
역할 (keyword): manager (세션/환경 관리)
드라마 설정 및 시스템 기능: 사설 탐정들의 아지트인 베이커가 221B의 집주인.
셜록과 존이 자유롭게 활동할 수 있도록 에이전트의 세션 상태와 런타임 인프라 환경을 안정적으로 관리합니다.
'''

class MrshudsonManagerSchema(BaseModel):

    id: int = Field(0, description="허드슨 부인 ID")
    name: str = Field("허드슨 부인 (Mrs. Hudson)", description="베이커가 221B 집주인, 세션/환경 관리자")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 11,
                "name": "MrsHudson manager",
            }
        }
    }
