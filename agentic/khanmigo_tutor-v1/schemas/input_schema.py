
from pydantic import BaseModel, Field


class TutorInput(BaseModel):

    student_id: str = Field(
        default="default_student",
        min_length=1,
    )

    message: str = Field(
        min_length=1,
        max_length=4000,
    )

    language: str = Field(
        default="English",
    )

    subject: str = Field(
        default="Computer Science",
    )

    topic: str | None = None

    # Explicit request to replace the pending exercise
    force_new_exercise: bool = False
