"""fixed datatype for num shares

Revision ID: a20717255c14
Revises: 179c72cb633c
Create Date: 2022-07-01 15:44:46.669316

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a20717255c14'
down_revision = '179c72cb633c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('stocks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('timeseries', sa.JSON(), nullable=True),
    sa.Column('ticker', sa.String(length=10), nullable=True),
    sa.Column('name', sa.String(length=100), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('exchange', sa.String(length=8), nullable=True),
    sa.Column('sector', sa.String(length=30), nullable=True),
    sa.Column('industry', sa.String(length=30), nullable=True),
    sa.Column('market_cap', sa.BIGINT(), nullable=True),
    sa.Column('no_shares', sa.BIGINT(), nullable=True),
    sa.Column('trail_pe_ratio', sa.Float(), nullable=True),
    sa.Column('fwd_pe_ratio', sa.Float(), nullable=True),
    sa.Column('d_yield', sa.Float(), nullable=True),
    sa.Column('high_52w', sa.Float(), nullable=True),
    sa.Column('low_52w', sa.Float(), nullable=True),
    sa.Column('eps', sa.JSON(), nullable=True),
    sa.Column('last_cache_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_stocks')),
    sa.UniqueConstraint('ticker', name=op.f('uq_stocks_ticker'))
    )
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
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('stocks')
    # ### end Alembic commands ###
