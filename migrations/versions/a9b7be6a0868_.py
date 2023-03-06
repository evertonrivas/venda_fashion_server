"""empty message

Revision ID: a9b7be6a0868
Revises: 75d1d0f5fee1
Create Date: 2023-02-28 22:56:34.913214

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a9b7be6a0868'
down_revision = '75d1d0f5fee1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cmm_product_model',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('date_created', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('date_updated', sa.DateTime(), nullable=True),
    sa.Column('trash', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('cmm_product_type',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('date_created', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('date_updated', sa.DateTime(), nullable=True),
    sa.Column('trash', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('cmm_products_sku', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id_type', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('id_model', sa.Integer(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cmm_products_sku', schema=None) as batch_op:
        batch_op.drop_column('id_model')
        batch_op.drop_column('id_type')

    op.drop_table('cmm_product_type')
    op.drop_table('cmm_product_model')
    # ### end Alembic commands ###