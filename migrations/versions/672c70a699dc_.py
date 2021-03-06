"""empty message

Revision ID: 672c70a699dc
Revises: 3790c2375422
Create Date: 2021-08-03 12:38:42.828771

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '672c70a699dc'
down_revision = '3790c2375422'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('photo',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('photo_name', sa.String(length=50), nullable=False),
    sa.Column('photo_datatime', sa.DateTime(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('photo')
    # ### end Alembic commands ###
