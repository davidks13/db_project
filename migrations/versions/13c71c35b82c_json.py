"""json

Revision ID: 13c71c35b82c
Revises: 9ed281b1f58d
Create Date: 2023-12-26 00:38:02.793493

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB


# revision identifiers, used by Alembic.
revision = '13c71c35b82c'
down_revision = '9ed281b1f58d'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('products', sa.Column('json_data', JSONB, nullable=True))

def downgrade():
    op.drop_column('products', 'json_data')