from pydantic import BaseModel, Field


class GenreGameSchema(BaseModel):
    title: str = Field(..., min_length=1)
    summary: str = Field(default="")
    steam_app_id: int = Field(..., ge=1)


class GenreHubSchema(BaseModel):
    id: str
    label: str
    description: str
    representative_title: str
    traits: list[str]
    games: list[GenreGameSchema]
