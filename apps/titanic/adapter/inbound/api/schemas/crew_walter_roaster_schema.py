from __future__ import annotations

from pydantic import BaseModel


class IntroduceResponseSchema(BaseModel):
    """GET /titanic/walter/myself 응답."""
    id: int
    name: str
