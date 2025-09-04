"""Add GIST index to SportsFacility.location

Revision ID: 5bde3e3b0d9a
Revises: 
Create Date: 2025-09-04

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '5bde3e3b0d9a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_index(
        'ix_sportsfacility_location',
        'sportsfacility',
        ['location'],
        postgresql_using='gist'
    )


def downgrade() -> None:
    op.drop_index('ix_sportsfacility_location', table_name='sportsfacility')