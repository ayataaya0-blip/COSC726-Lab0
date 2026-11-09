
from typing import Literal

from pydantic import BaseModel, Field


TaskType = Literal[
    "conceptual_explanation",
    "calculation",
    "code_analysis",
    "algorithm_analysis",
    "definition",
    "comparison",
    "exercise",
    "quiz",
    "quiz_answer",
    "general_learning",
]


class UnderstandingOutput(BaseModel):
    goal: str = Field(min_length=1)

    task_type: TaskType

    detected_concepts: list[str] = Field(
        default_factory=list
    )

    student_need: str = Field(min_length=1)
