"""empty message

Revision ID: 586380cbdaef
Revises: 80f8a11a55b1
Create Date: 2023-11-02 11:14:20.647656

"""
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "586380cbdaef"
down_revision: Union[str, None] = "80f8a11a55b1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "user",
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )
    op.create_unique_constraint(None, "user", ["phone_number"])
    op.create_unique_constraint(None, "user", ["email"])
    op.create_unique_constraint(None, "user", ["username"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "user", type_="unique")
    op.drop_constraint(None, "user", type_="unique")
    op.drop_constraint(None, "user", type_="unique")
    op.drop_column("user", "updated_at")
    # ### end Alembic commands ###
