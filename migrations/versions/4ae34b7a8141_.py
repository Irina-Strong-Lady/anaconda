"""empty message

Revision ID: 4ae34b7a8141
Revises: a88a010d9d60
Create Date: 2022-10-17 10:25:32.091479

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4ae34b7a8141'
down_revision = 'a88a010d9d60'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'avatar')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('avatar', sa.VARCHAR(length=128), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
