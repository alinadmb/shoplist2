"""add email

Revision ID: 39aa5d2cfe79
Revises: e0f7486c0640
Create Date: 2019-12-01 23:02:57.700791

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '39aa5d2cfe79'
down_revision = 'e0f7486c0640'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('email', sa.String(length=30), nullable=True))
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_column('user', 'email')
    # ### end Alembic commands ###
