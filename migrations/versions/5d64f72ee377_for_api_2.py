"""for api 2

Revision ID: 5d64f72ee377
Revises: a1ca920e0570
Create Date: 2019-12-07 21:01:34.602963

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5d64f72ee377'
down_revision = 'a1ca920e0570'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('list', 'item')
    op.drop_column('list', 'name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('list', sa.Column('name', sa.VARCHAR(length=30), nullable=True))
    op.add_column('list', sa.Column('item', sa.VARCHAR(length=30), nullable=True))
    # ### end Alembic commands ###
