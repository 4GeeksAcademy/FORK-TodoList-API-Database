"""empty message

Revision ID: 47dbd9667559
Revises: 
Create Date: 2024-12-13 16:36:53.808157

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '47dbd9667559'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=225), nullable=False),
    sa.Column('gender', sa.Enum('MALE', 'FEMALE', 'OTHERS', name='genders'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('todos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('label', sa.String(length=99), nullable=True),
    sa.Column('is_done', sa.Boolean(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('todos')
    op.drop_table('user')
    # ### end Alembic commands ###