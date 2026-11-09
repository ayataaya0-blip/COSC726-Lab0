from pydantic import BaseModel, Field


class ToolRequest(BaseModel):
    tool_name: str = Field(
        min_length=1,
    )

    arguments: dict = Field(
        default_factory=dict,
    )


class ToolResult(BaseModel):
    status: str

    tool: str

    result: object | None = None

    error: str | None = None