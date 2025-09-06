"""Phase 3: Performance metrics and budget execution tables

Revision ID: 002_phase3_metrics_budget
Revises: 001_phase3_core_dims
Create Date: 2025-01-06

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import Integer, String, Float, Date, DateTime, Boolean, Text, Numeric

# revision identifiers, used by Alembic.
revision = '002_phase3_metrics_budget'
down_revision = '001_phase3_core_dims'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create ETL runs table first (referenced by other tables)
    op.create_table(
        'etl_runs',
        sa.Column('run_id', Integer, primary_key=True, autoincrement=True),
        sa.Column('source', String(50), nullable=False),
        sa.Column('schema_version', String(20)),
        sa.Column('started_at', DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column('finished_at', DateTime),
        sa.Column('status', String(20), nullable=False, default='running'),
        sa.Column('row_count', Integer, default=0),
        sa.Column('error_message', Text),
        sa.Column('task_id', String(50)),
        sa.Column('retry_count', Integer, default=0),
        sa.Column('metadata', Text),
    )
    op.create_index('idx_etl_status_source', 'etl_runs', ['status', 'source'])
    op.create_index('idx_etl_started', 'etl_runs', ['started_at'])
    
    # Create IndicatorMeta table
    op.create_table(
        'indicator_meta',
        sa.Column('id', Integer, primary_key=True, autoincrement=True),
        sa.Column('name', String(255), nullable=False),
        sa.Column('description', Text),
        sa.Column('value_type', String(20), nullable=False),
        sa.Column('aggregation_rule', String(20), nullable=False),
        sa.Column('scaling', String(20), default='none'),
        sa.Column('direction_positive', Boolean, default=True),
        sa.Column('unit', String(50)),
        sa.Column('category', String(50)),
    )
    op.create_index('ix_indicator_meta_name', 'indicator_meta', ['name'], unique=True)
    
    # Create PerformanceMetric table
    op.create_table(
        'performance_metric',
        sa.Column('id', Integer, primary_key=True, autoincrement=True),
        sa.Column('sport_id', Integer, sa.ForeignKey('sport.id'), nullable=False),
        sa.Column('indicator_id', Integer, sa.ForeignKey('indicator_meta.id'), nullable=False),
        sa.Column('institution_id', Integer, sa.ForeignKey('institution.id')),
        sa.Column('measured_on', Date, nullable=False),
        sa.Column('value', Float, nullable=False),
        sa.Column('normalized_value', Float),
        sa.Column('run_id', Integer, sa.ForeignKey('etl_runs.run_id'), nullable=False),
    )
    op.create_index('idx_perf_sport_date', 'performance_metric', ['sport_id', 'measured_on'])
    op.create_index('idx_perf_run_indicator', 'performance_metric', ['run_id', 'indicator_id'])
    op.create_index('ix_performance_metric_sport', 'performance_metric', ['sport_id'])
    op.create_index('ix_performance_metric_indicator', 'performance_metric', ['indicator_id'])
    op.create_index('ix_performance_metric_measured', 'performance_metric', ['measured_on'])
    op.create_index('ix_performance_metric_run', 'performance_metric', ['run_id'])
    
    # Create BudgetExecution table
    op.create_table(
        'budget_execution',
        sa.Column('id', Integer, primary_key=True, autoincrement=True),
        sa.Column('year', Integer, nullable=False),
        sa.Column('quarter', Integer),
        sa.Column('institution_id', Integer, sa.ForeignKey('institution.id'), nullable=False),
        sa.Column('project_id', Integer, sa.ForeignKey('project.id'), nullable=False),
        sa.Column('allocated', Numeric(18, 2), nullable=False),
        sa.Column('executed', Numeric(18, 2), nullable=False),
        sa.Column('execution_rate', Float),
        sa.Column('run_id', Integer, sa.ForeignKey('etl_runs.run_id'), nullable=False),
    )
    op.create_index('idx_budget_year_inst_proj', 'budget_execution', 
                    ['year', 'institution_id', 'project_id'])
    op.create_index('ix_budget_execution_year', 'budget_execution', ['year'])
    op.create_index('ix_budget_execution_inst', 'budget_execution', ['institution_id'])
    op.create_index('ix_budget_execution_proj', 'budget_execution', ['project_id'])
    op.create_index('ix_budget_execution_run', 'budget_execution', ['run_id'])
    
    # Add check constraints
    op.create_check_constraint(
        'chk_budget_execution',
        'budget_execution',
        'executed <= allocated'
    )
    op.create_check_constraint(
        'chk_execution_rate',
        'budget_execution',
        'execution_rate >= 0 AND execution_rate <= 100'
    )


def downgrade() -> None:
    op.drop_constraint('chk_execution_rate', 'budget_execution')
    op.drop_constraint('chk_budget_execution', 'budget_execution')
    op.drop_table('budget_execution')
    op.drop_table('performance_metric')
    op.drop_table('indicator_meta')
    op.drop_table('etl_runs')