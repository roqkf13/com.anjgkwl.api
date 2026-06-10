from __future__ import annotations

from pydantic import BaseModel


class IntroduceResponseSchema(BaseModel):
    """GET /titanic/jack/myself 응답."""
    id: int
    name: str
