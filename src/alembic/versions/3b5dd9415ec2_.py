"""empty message

Revision ID: 3b5dd9415ec2
Revises: 9d7ed5687ef4
Create Date: 2023-11-09 10:59:18.841246

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "3b5dd9415ec2"
down_revision: Union[str, None] = "9d7ed5687ef4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "user", "password", existing_type=sa.VARCHAR(length=80), nullable=False
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "user", "password", existing_type=sa.VARCHAR(length=80), nullable=True
    )
    # ### end Alembic commands ###
