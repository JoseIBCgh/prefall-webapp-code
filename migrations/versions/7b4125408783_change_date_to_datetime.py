"""change date to datetime

Revision ID: 7b4125408783
Revises: 9c592121801f
Create Date: 2023-09-22 11:39:02.370005

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7b4125408783'
down_revision = '9c592121801f'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('test', 'date', type_=sa.DateTime)

def downgrade():
    op.alter_column('test', 'date', type_=sa.Date)
