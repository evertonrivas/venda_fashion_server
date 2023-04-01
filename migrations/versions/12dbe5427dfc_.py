"""empty message

Revision ID: 12dbe5427dfc
Revises: d1f5ed081759
Create Date: 2023-03-27 15:38:15.343252

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '12dbe5427dfc'
down_revision = 'd1f5ed081759'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cmm_colors_translate',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('hexcode', sa.String(length=8), nullable=False),
    sa.Column('color', sa.String(length=10), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('cmm_sizes_translate',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('size_name', sa.String(length=10), nullable=False),
    sa.Column('size', sa.String(length=5), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('cmm_size_translate')
    op.drop_table('cmm_color_translate')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cmm_color_translate',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('hexcode', mysql.VARCHAR(length=8), nullable=False),
    sa.Column('color', mysql.VARCHAR(length=10), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('cmm_size_translate',
    sa.Column('id', mysql.INTEGER(display_width=11), autoincrement=True, nullable=False),
    sa.Column('size_name', mysql.VARCHAR(length=10), nullable=True),
    sa.Column('size', mysql.VARCHAR(length=5), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.drop_table('cmm_sizes_translate')
    op.drop_table('cmm_colors_translate')
    # ### end Alembic commands ###