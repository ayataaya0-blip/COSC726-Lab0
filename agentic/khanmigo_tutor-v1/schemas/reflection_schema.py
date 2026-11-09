from typing import Literal

from pydantic import BaseModel, Field


ReflectionDecision = Literal[
    "respond",
    "replan",
]


class ReflectionOutput(BaseModel):
    decision: ReflectionDecision

    reason: str = Field(min_length=1)

    sufficient: bool