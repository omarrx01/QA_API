
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class QuestionAnswerCreate(BaseModel):
    question: str = Field(min_length=1)
    answer: str = Field(min_length=1)


class QuestionAnswerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    question: str
    answer: str
    created_at: datetime
