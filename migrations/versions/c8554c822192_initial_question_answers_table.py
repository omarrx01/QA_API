
"""initial question answers table

Revision ID: c8554c822192
Revises:
Create Date: 2026-11-14 23:41:18.682876
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# Revision identifiers used by Alembic
revision: str = "c8554c822192"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create the question_answers table and index."""

    op.create_table(
        "question_answers",
        sa.Column(
            "id",
            sa.UUID(),
            nullable=False
        ),
        sa.Column(
            "question",
            sa.Text(),
            nullable=False
        ),
        sa.Column(
            "answer",
            sa.Text(),
            nullable=False
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            nullable=False
        ),
        sa.PrimaryKeyConstraint("id")
    )

    op.create_index(
        "idx_created_at",
        "question_answers",
        ["created_at"],
        unique=False
    )


def downgrade() -> None:
    """Remove the question_answers table and index."""

    op.drop_index(
        "idx_created_at",
        table_name="question_answers"
    )

    op.drop_table("question_answers")
