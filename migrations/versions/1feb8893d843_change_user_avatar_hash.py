"""change user.avatar_hash

Revision ID: 1feb8893d843
Revises: 11be0a7ab632
Create Date: 2022-10-17 14:07:56.728535

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1feb8893d843'
down_revision = '11be0a7ab632'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'avatar_hash')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('avatar_hash', sa.VARCHAR(length=128), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
