
from typing import Literal

from pydantic import BaseModel, Field



PlanAction = Literal[
    "retrieve_knowledge",
    "calculate",
    "run_python",
    "analyze_code",
    "analyze_complexity",
    "generate_exercise",
    "evaluate_exercise_answer",
    "manage_quiz",
    "evaluate_quiz_answer",
    "update_progress",
    "respond",
]



class PlanOutput(BaseModel):
    goal: str = Field(min_length=1)

    task_type: str = Field(min_length=1)

    detected_concepts: list[str] = Field(
        default_factory=list
    )

    student_need: str = Field(min_length=1)

    plan: list[str] = Field(
        default_factory=list
    )

    current_step: int = Field(
        default=0,
        ge=0
    )

    next_action: PlanAction

    tool_request: dict | None = None
