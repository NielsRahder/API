"""add content to post table

Revision ID: b6a391bedbbc
Revises: 02d6e13e0220
Create Date: 2025-07-02 15:18:00.455359

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b6a391bedbbc'
down_revision: Union[str, Sequence[str], None] = '02d6e13e0220'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column('content', sa.String(), nullable = False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
