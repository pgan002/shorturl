"""Create urls table

Revision ID: 0001
Revises: 
Create Date: 2018-11-30 17:31:11.019772

"""
from alembic import op
from sqlalchemy import Column, TEXT


revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('urls',
                    Column('id', TEXT, primary_key=True, index=True),
                    Column('url', TEXT, nullable=False),
                    Column('auth_token', TEXT(16)))


def downgrade():
    op.drop_table('urls')
