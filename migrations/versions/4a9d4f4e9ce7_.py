"""empty message

Revision ID: 4a9d4f4e9ce7
Revises: a9b7be6a0868
Create Date: 2023-03-01 23:28:54.933250

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4a9d4f4e9ce7'
down_revision = 'a9b7be6a0868'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cmm_category',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('parent', sa.Integer(), nullable=True),
    sa.Column('date_created', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('date_updated', sa.DateTime(), nullable=True),
    sa.Column('trash', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('cmm_category')
    # ### end Alembic commands ###