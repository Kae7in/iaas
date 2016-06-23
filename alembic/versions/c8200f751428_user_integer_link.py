"""user_integer_link

Revision ID: c8200f751428
Revises: ec8a855c65f2
Create Date: 2016-06-22 00:36:55.333603

"""

# revision identifiers, used by Alembic.
revision = 'c8200f751428'
down_revision = 'ec8a855c65f2'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('integers',
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id'))
    )
    op.add_column('users',
        sa.Relationship('integers', backref='user')
    )


def downgrade():
    pass
