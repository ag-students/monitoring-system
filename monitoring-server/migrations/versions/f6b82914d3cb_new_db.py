"""new db

Revision ID: f6b82914d3cb
Revises: 
Create Date: 2022-04-18 00:13:57.775665

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f6b82914d3cb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tmp',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.String(length=10), nullable=False),
    sa.Column('time', sa.String(length=10), nullable=False),
    sa.Column('move', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=20), nullable=False),
    sa.Column('surname', sa.String(length=30), nullable=False),
    sa.Column('e_mail', sa.String(length=30), nullable=False),
    sa.Column('address', sa.String(length=30), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('rooms',
    sa.Column('id_room', sa.Integer(), nullable=False),
    sa.Column('mac', sa.String(length=20), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id_room')
    )
    op.create_table('my_data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_room', sa.Integer(), nullable=True),
    sa.Column('date', sa.String(length=10), nullable=False),
    sa.Column('time', sa.String(length=10), nullable=False),
    sa.Column('day_part', sa.Integer(), nullable=False),
    sa.Column('is_abnormal', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['id_room'], ['rooms.id_room'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('sample_data',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('id_room', sa.Integer(), nullable=True),
    sa.Column('day_part', sa.Integer(), nullable=False),
    sa.Column('time_diff', sa.Integer(), nullable=False),
    sa.Column('timer', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['id_room'], ['rooms.id_room'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('sample_data')
    op.drop_table('my_data')
    op.drop_table('rooms')
    op.drop_table('users')
    op.drop_table('tmp')
    # ### end Alembic commands ###