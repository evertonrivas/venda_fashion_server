"""empty message

Revision ID: 930cef02dad2
Revises: 0e83fa3371b5
Create Date: 2023-02-22 14:07:47.558823

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '930cef02dad2'
down_revision = '0e83fa3371b5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cmm_products_grid', schema=None) as batch_op:
        batch_op.add_column(sa.Column('date_created', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
        batch_op.add_column(sa.Column('date_updated', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cmm_products_grid', schema=None) as batch_op:
        batch_op.drop_column('date_updated')
        batch_op.drop_column('date_created')

    # ### end Alembic commands ###