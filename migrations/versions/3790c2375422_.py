"""empty message

Revision ID: 3790c2375422
Revises: 
Create Date: 2021-07-10 02:20:11.171860

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3790c2375422'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('article_type',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('type_name', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=15), nullable=False),
    sa.Column('password', sa.String(length=100), nullable=False),
    sa.Column('phone', sa.String(length=11), nullable=False),
    sa.Column('email', sa.String(length=30), nullable=True),
    sa.Column('icon', sa.String(length=100), nullable=True),
    sa.Column('isdelete', sa.Boolean(), nullable=True),
    sa.Column('rdatetime', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('article',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=50), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('padatetime', sa.DateTime(), nullable=True),
    sa.Column('click_num', sa.Integer(), nullable=True),
    sa.Column('save_num', sa.Integer(), nullable=True),
    sa.Column('love_num', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('type_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['type_id'], ['article_type.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('comment',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('comment', sa.String(length=255), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('article_id', sa.Integer(), nullable=True),
    sa.Column('cdatetime', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['article_id'], ['article.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comment')
    op.drop_table('article')
    op.drop_table('user')
    op.drop_table('article_type')
    # ### end Alembic commands ###
