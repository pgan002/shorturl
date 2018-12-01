"""Create stats table

Revision ID: 0002
Revises: 0001
Create Date: 2018-11-30 17:46:54.067383

"""
from alembic import op
from sqlalchemy import Column, TEXT, INT, ForeignKey, PrimaryKeyConstraint


revision = '0002'
down_revision = '0001'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('stats',
                    Column('id', TEXT, ForeignKey('urls.id'), index=True),
                    Column('ip', TEXT, nullable=False),
                    Column('count', INT, nullable=False, default=0),
                    PrimaryKeyConstraint('id', 'ip'))


def downgrade():
    op.drop_table('stats')
