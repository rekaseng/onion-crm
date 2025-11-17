"""Rename permission table to permissions

Revision ID: 59be03ad69ce
Revises: b6326d58fe89
Create Date: 2024-07-01 12:35:13.330081

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '59be03ad69ce'
down_revision: Union[str, None] = 'b6326d58fe89'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Rename the table from 'permission' to 'permissions'
    op.rename_table('permission', 'permissions')


def downgrade() -> None:
    # Rename the table from 'permissions' back to 'permission'
    op.rename_table('permissions', 'permission')
