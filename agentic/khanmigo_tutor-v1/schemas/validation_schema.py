from pydantic import BaseModel, Field


class ValidationOutput(BaseModel):
    valid: bool

    errors: list[str] = Field(
        default_factory=list
    )

    warnings: list[str] = Field(
        default_factory=list
    )