"""fixed datatype for market cap

Revision ID: 179c72cb633c
Revises: 1c191e652902
Create Date: 2022-07-01 15:31:10.979873

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '179c72cb633c'
down_revision = '1c191e652902'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=80), nullable=False),
    sa.Column('email', sa.String(length=320), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_users')),
    sa.UniqueConstraint('email', name=op.f('uq_users_email')),
    sa.UniqueConstraint('username', name=op.f('uq_users_username'))
    )
    op.drop_table('test')
    op.create_unique_constraint(op.f('uq_stocks_ticker'), 'stocks', ['ticker'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('uq_stocks_ticker'), 'stocks', type_='unique')
    op.create_table('test',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('info', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('id', name='test_pkey')
    )
    op.drop_table('users')
    # ### end Alembic commands ###