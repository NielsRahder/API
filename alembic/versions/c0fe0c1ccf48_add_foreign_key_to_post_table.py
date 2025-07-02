"""add foreign key to post table

Revision ID: c0fe0c1ccf48
Revises: 84baf28fa32f
Create Date: 2025-07-02 15:41:16.335245

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c0fe0c1ccf48'
down_revision: Union[str, Sequence[str], None] = '84baf28fa32f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key("post_users_fk", source_table = "posts", referent_table = "users", local_cols = ["owner_id"], remote_cols=["id"], ondelete = "CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint("post_users_fk", "posts")
    op.drop_column("posts", "owner_id")
    pass
