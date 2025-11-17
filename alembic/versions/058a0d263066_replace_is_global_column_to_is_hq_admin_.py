"""Replace is_global column to is_hq_admin and Added is__admin column to Roles Table

Revision ID: 058a0d263066
Revises: 59be03ad69ce
Create Date: 2024-07-01 17:42:35.557615

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '058a0d263066'
down_revision: Union[str, None] = '59be03ad69ce'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('roles',
                  sa.Column('is_admin', sa.Boolean(), nullable=False, server_default=sa.sql.expression.false()))
    op.add_column('roles',
                  sa.Column('is_hq_admin', sa.Boolean(), nullable=False, server_default=sa.sql.expression.false()))
    op.drop_column('roles', 'is_global')
    op.create_unique_constraint('uq_roles_name', 'roles', ['name'])
    # ### end Alembic commands ###

    # set server_default to None after initial creation
    op.alter_column('roles', 'is_admin', server_default=None)
    op.alter_column('roles', 'is_hq_admin', server_default=None)


def downgrade() -> None:
    op.drop_constraint('uq_roles_name', 'roles', type_='unique')
    op.add_column('roles',
                  sa.Column('is_global', sa.Boolean(), nullable=False, server_default=sa.sql.expression.false()))
    op.drop_column('roles', 'is_hq_admin')
    op.drop_column('roles', 'is_admin')
    # ### end Alembic commands ###

    # set server_default to None after initial creation
    op.alter_column('roles', 'is_global', server_default=None)
