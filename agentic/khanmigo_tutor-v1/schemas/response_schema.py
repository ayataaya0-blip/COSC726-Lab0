from pydantic import BaseModel, Field


class ResponseOutput(BaseModel):
    response: str = Field(min_length=1)