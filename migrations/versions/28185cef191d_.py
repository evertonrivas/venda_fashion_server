"""empty message

Revision ID: 28185cef191d
Revises: 0a73f83b9065
Create Date: 2023-04-17 16:57:38.382920

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '28185cef191d'
down_revision = '0a73f83b9065'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('b2b_orders', schema=None) as batch_op:
        batch_op.add_column(sa.Column('total_itens', sa.DECIMAL(precision=10, scale=2), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('b2b_orders', schema=None) as batch_op:
        batch_op.drop_column('total_itens')

    # ### end Alembic commands ###