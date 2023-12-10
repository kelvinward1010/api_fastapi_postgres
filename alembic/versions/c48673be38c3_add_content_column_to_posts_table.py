"""add content column to posts table

Revision ID: c48673be38c3
Revises: 11fbfedc9b3d
Create Date: 2023-12-10 14:56:11.191766

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c48673be38c3'
down_revision: Union[str, None] = '11fbfedc9b3d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
