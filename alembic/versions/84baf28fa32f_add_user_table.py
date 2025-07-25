"""add user table

Revision ID: 84baf28fa32f
Revises: b6a391bedbbc
Create Date: 2025-07-02 15:29:12.662632

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '84baf28fa32f'
down_revision: Union[str, Sequence[str], None] = 'b6a391bedbbc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
)
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
