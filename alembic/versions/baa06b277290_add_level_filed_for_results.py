"""add level filed for results

Revision ID: baa06b277290
Revises: 6d69f78ca0d4
Create Date: 2024-11-30 00:39:13.060266

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "baa06b277290"
down_revision: Union[str, None] = "6d69f78ca0d4"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("results", sa.Column("level", sa.Integer(), nullable=False))
    op.create_index(op.f("ix_results_id"), "results", ["id"], unique=False)
    op.drop_constraint("users_username_key", "users", type_="unique")
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)
    op.create_index(op.f("ix_users_username"), "users", ["username"], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_users_username"), table_name="users")
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.create_unique_constraint("users_username_key", "users", ["username"])
    op.drop_index(op.f("ix_results_id"), table_name="results")
    op.drop_column("results", "level")
    # ### end Alembic commands ###
