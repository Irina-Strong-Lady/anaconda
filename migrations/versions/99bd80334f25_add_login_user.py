"""Add login user

Revision ID: 99bd80334f25
Revises: 6bc38d274195
Create Date: 2022-07-04 15:02:05.762323

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '99bd80334f25'
down_revision = '6bc38d274195'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('email', sa.String(length=64), nullable=True))
    op.add_column('users', sa.Column('password_hash', sa.String(length=128), nullable=True))
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_column('users', 'password_hash')
    op.drop_column('users', 'email')
    # ### end Alembic commands ###
