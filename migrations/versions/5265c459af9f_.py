"""empty message

Revision ID: 5265c459af9f
Revises: b07b2694bf98
Create Date: 2022-10-12 13:51:53.984546

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '5265c459af9f'
down_revision = 'b07b2694bf98'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'avatar')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('avatar', postgresql.BYTEA(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
