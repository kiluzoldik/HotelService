"""initial version

Revision ID: 701794109d73
Revises:
Create Date: 2024-12-03 16:29:30.223798

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "701794109d73"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "hotels",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=100), nullable=False),
        sa.Column("location", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("hotels")
