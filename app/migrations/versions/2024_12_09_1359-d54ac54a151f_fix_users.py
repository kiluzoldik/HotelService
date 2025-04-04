"""fix: users

Revision ID: d54ac54a151f
Revises: e9ec254a6492
Create Date: 2024-12-09 13:59:33.456722

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "d54ac54a151f"
down_revision: Union[str, None] = "e9ec254a6492"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("users", sa.Column("hashed_password", sa.String(length=200), nullable=False))
    op.drop_column("users", "password")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "users",
        sa.Column("password", sa.VARCHAR(length=200), autoincrement=False, nullable=False),
    )
    op.drop_column("users", "hashed_password")
    # ### end Alembic commands ###
