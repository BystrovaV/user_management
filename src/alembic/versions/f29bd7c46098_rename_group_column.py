"""Rename group column

Revision ID: f29bd7c46098
Revises: ea5b93b1ec3f
Create Date: 2023-11-22 11:18:27.041365

"""
from typing import Sequence, Union

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f29bd7c46098"
down_revision: Union[str, None] = "ea5b93b1ec3f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("user", "group", new_column_name="group_id")


def downgrade() -> None:
    op.alter_column("user", "group_id", new_column_name="group")
