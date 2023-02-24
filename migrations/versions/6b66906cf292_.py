"""empty message

Revision ID: 6b66906cf292
Revises: f67f60b82e1b
Create Date: 2023-02-24 09:49:23.579784

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '6b66906cf292'
down_revision = 'f67f60b82e1b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
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

    # ### end Alembic commands ###
