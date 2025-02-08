"""empty message

Revision ID: 79bcd744c576
Revises: 1989f23bb290
Create Date: 2025-02-04 13:55:56.079036

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa  # noqa


# revision identifiers, used by Alembic.
revision: str = "79bcd744c576"
down_revision: Union[str, None] = "1989f23bb290"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, "hotels", ["title"])


def downgrade() -> None:
    op.drop_constraint(None, "hotels", type_="unique")
