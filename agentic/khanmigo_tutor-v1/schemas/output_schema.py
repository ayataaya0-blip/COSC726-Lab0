from pydantic import BaseModel, Field


class TutorOutput(BaseModel):
    response: str = Field(
        min_length=1,
    )

    language: str

    subject: str

    topic: str | None = None

    intent: str

    action: str

    tool_used: str | None = None

    grounded: bool = False