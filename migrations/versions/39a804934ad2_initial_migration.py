"""Initial migration

Revision ID: 39a804934ad2
Revises: 
Create Date: 2024-02-05 10:42:00.424752

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '39a804934ad2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('news',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('platform', sa.String(length=50), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('date', sa.String(length=20), nullable=False),
    sa.Column('link', sa.String(length=200), nullable=False),
    sa.Column('hot_topic', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('platform_list',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('platform_name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('platform_name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('platform_list')
    op.drop_table('news')
    # ### end Alembic commands ###