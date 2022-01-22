"""create models brand user discountcode

Revision ID: 86fc0c35249d
Revises: 
Create Date: 2022-01-22 12:15:49.626307

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '86fc0c35249d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('brand',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('surname', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('discount_code',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(length=255), nullable=False),
    sa.Column('brand_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('usable', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['brand_id'], ['brand.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('discount_code')
    op.drop_table('user')
    op.drop_table('brand')
    # ### end Alembic commands ###
