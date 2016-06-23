"""Add a column

Revision ID: ec8a855c65f2
Revises:
Create Date: 2016-06-16 22:05:10.496430

"""

# revision identifiers, used by Alembic.
revision = 'ec8a855c65f2'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa
from sqlalchemy import Column, Integer


def upgrade():
    op.add_column('integers',
        Column('label', Integer)
    )


def downgrade():
    pass
