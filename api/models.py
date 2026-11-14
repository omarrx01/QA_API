
import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Index, Text
from sqlalchemy.dialects.postgresql import UUID

from api.database import Base


class QuestionAnswer(Base):
    __tablename__ = "question_answers"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    __table_args__ = (
        Index("idx_created_at", "created_at"),
    )
