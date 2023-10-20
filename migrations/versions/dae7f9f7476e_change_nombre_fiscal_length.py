"""change nombre fiscal length

Revision ID: dae7f9f7476e
Revises: 0bffb6a89119
Create Date: 2023-10-20 04:47:10.736680

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dae7f9f7476e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('centros', 'nombreFiscal', type_=sa.String(length=100))


def downgrade():
    op.alter_column('centros', 'nombreFiscal', type_=sa.String(length=50))
