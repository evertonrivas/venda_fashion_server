"""empty message

Revision ID: 75d1d0f5fee1
Revises: 1926387b120d
Create Date: 2023-02-28 22:15:21.179402

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '75d1d0f5fee1'
down_revision = '1926387b120d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('b2b_collection',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('date_created', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('date_updated', sa.DateTime(), nullable=True),
    sa.Column('trash', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('b2b_collection_price',
    sa.Column('id_collection', sa.Integer(), nullable=False),
    sa.Column('id_table_price', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id_collection', 'id_table_price')
    )
    with op.batch_alter_table('cmm_users', schema=None) as batch_op:
        batch_op.alter_column('token',
               existing_type=mysql.VARCHAR(length=50),
               type_=sa.String(length=255),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('cmm_users', schema=None) as batch_op:
        batch_op.alter_column('token',
               existing_type=sa.String(length=255),
               type_=mysql.VARCHAR(length=50),
               existing_nullable=True)

    op.drop_table('b2b_collection_price')
    op.drop_table('b2b_collection')
    # ### end Alembic commands ###
