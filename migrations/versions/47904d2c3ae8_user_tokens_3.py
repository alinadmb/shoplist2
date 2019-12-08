"""user tokens 3

Revision ID: 47904d2c3ae8
Revises: 6b153c183b9f
Create Date: 2019-12-07 22:54:32.224208

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '47904d2c3ae8'
down_revision = '6b153c183b9f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('list', 'item')
    op.drop_column('list', 'name')
    op.add_column('user', sa.Column('token', sa.String(length=32), nullable=True))
    op.add_column('user', sa.Column('token_expiration', sa.DateTime(), nullable=True))
    op.create_index(op.f('ix_user_token'), 'user', ['token'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_token'), table_name='user')
    op.drop_column('user', 'token_expiration')
    op.drop_column('user', 'token')
    op.add_column('list', sa.Column('name', sa.VARCHAR(length=30), nullable=True))
    op.add_column('list', sa.Column('item', sa.VARCHAR(length=30), nullable=True))
    # ### end Alembic commands ###