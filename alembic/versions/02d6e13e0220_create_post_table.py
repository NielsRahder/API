"""create post table

Revision ID: 02d6e13e0220
Revises: 
Create Date: 2025-07-02 13:55:03.430268

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '02d6e13e0220'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable = False, primary_key = True), 
                            sa.Column('title', sa.String(), nullable = False))
    pass


def downgrade() -> None:
    op.drop_table("posts")
    pass
