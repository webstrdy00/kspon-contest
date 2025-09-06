"""Phase 3: Core dimension tables for budget-performance analysis

Revision ID: 001_phase3_core_dims
Revises: 5bde3e3b0d9a
Create Date: 2025-01-06

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import Integer, String, Float, Date, Boolean, Text

# revision identifiers, used by Alembic.
revision = '001_phase3_core_dims'
down_revision = '5bde3e3b0d9a'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create Institution table
    op.create_table(
        'institution',
        sa.Column('id', Integer, primary_key=True, autoincrement=True),
        sa.Column('name', String(255), nullable=False),
        sa.Column('type', String(50)),
        sa.Column('created_at', Date),
    )
    op.create_index('ix_institution_name', 'institution', ['name'], unique=True)
    
    # Create Sport table
    op.create_table(
        'sport',
        sa.Column('id', Integer, primary_key=True, autoincrement=True),
        sa.Column('code', String(50), nullable=False),
        sa.Column('name', String(100), nullable=False),
        sa.Column('category', String(50)),
        sa.Column('olympic_status', Boolean, default=False),
    )
    op.create_index('ix_sport_code', 'sport', ['code'], unique=True)
    
    # Create Project table
    op.create_table(
        'project',
        sa.Column('id', Integer, primary_key=True, autoincrement=True),
        sa.Column('name', String(255), nullable=False),
        sa.Column('code', String(50)),
        sa.Column('type', String(50)),
        sa.Column('description', String(500)),
    )
    op.create_index('ix_project_name', 'project', ['name'], unique=True)
    op.create_index('ix_project_code', 'project', ['code'], unique=True)
    
    # Create InstitutionRegion mapping table (SCD Type 2)
    op.create_table(
        'institution_region',
        sa.Column('id', Integer, primary_key=True, autoincrement=True),
        sa.Column('institution_id', Integer, sa.ForeignKey('institution.id'), nullable=False),
        sa.Column('region_code', String(10), sa.ForeignKey('region.code'), nullable=False),
        sa.Column('confidence', Float, default=1.0),
        sa.Column('valid_from', Date, nullable=False),
        sa.Column('valid_to', Date),
        sa.Column('source', String(50)),
    )
    op.create_index('ix_institution_region_inst', 'institution_region', ['institution_id'])
    op.create_index('ix_institution_region_region', 'institution_region', ['region_code'])
    op.create_constraint(
        'uq_inst_region_valid',
        'institution_region',
        ['institution_id', 'region_code', 'valid_from'],
        unique=True
    )
    # Create partial index for current mappings
    op.execute("""
        CREATE INDEX idx_inst_region_current 
        ON institution_region(institution_id, region_code) 
        WHERE valid_to IS NULL
    """)
    
    # Create ProjectSport mapping table
    op.create_table(
        'project_sport',
        sa.Column('id', Integer, primary_key=True, autoincrement=True),
        sa.Column('project_id', Integer, sa.ForeignKey('project.id'), nullable=False),
        sa.Column('sport_id', Integer, sa.ForeignKey('sport.id'), nullable=False),
        sa.Column('priority', Integer, default=1),
    )
    op.create_index('ix_project_sport_project', 'project_sport', ['project_id'])
    op.create_index('ix_project_sport_sport', 'project_sport', ['sport_id'])
    op.create_constraint(
        'uq_project_sport',
        'project_sport',
        ['project_id', 'sport_id'],
        unique=True
    )


def downgrade() -> None:
    op.drop_table('project_sport')
    op.drop_table('institution_region')
    op.drop_table('project')
    op.drop_table('sport')
    op.drop_table('institution')