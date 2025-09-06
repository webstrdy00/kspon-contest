"""Phase 3: Aggregation cache table for performance optimization

Revision ID: 003_phase3_aggregation_cache
Revises: 002_phase3_metrics_budget
Create Date: 2025-01-06

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import Integer, String, Float, DateTime, Numeric

# revision identifiers, used by Alembic.
revision = '003_phase3_aggregation_cache'
down_revision = '002_phase3_metrics_budget'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create AggregationCache table
    op.create_table(
        'aggregation_cache',
        sa.Column('id', Integer, primary_key=True, autoincrement=True),
        sa.Column('run_id', Integer, sa.ForeignKey('etl_runs.run_id'), nullable=False),
        sa.Column('aggregation_type', String(50), nullable=False),
        sa.Column('dimension_key', String(255), nullable=False),
        sa.Column('year', Integer),
        sa.Column('sport_id', Integer, sa.ForeignKey('sport.id')),
        sa.Column('region_code', String(10), sa.ForeignKey('region.code')),
        sa.Column('budget_total', Numeric(18, 2)),
        sa.Column('budget_executed', Numeric(18, 2)),
        sa.Column('performance_score', Float),
        sa.Column('efficiency', Float),
        sa.Column('roi', Float),
        sa.Column('rank', Integer),
        sa.Column('grade', String(2)),
        sa.Column('created_at', DateTime, server_default=sa.func.now()),
    )
    
    # Create indexes for performance
    op.create_index('ix_aggregation_cache_run', 'aggregation_cache', ['run_id'])
    op.create_index('idx_agg_type_year', 'aggregation_cache', ['aggregation_type', 'year'])
    op.create_index('idx_agg_run_type', 'aggregation_cache', ['run_id', 'aggregation_type'])
    op.create_index('ix_aggregation_cache_year', 'aggregation_cache', ['year'])
    op.create_index('ix_aggregation_cache_sport', 'aggregation_cache', ['sport_id'])
    op.create_index('ix_aggregation_cache_region', 'aggregation_cache', ['region_code'])
    
    # Create unique constraint for cache key
    op.create_constraint(
        'uq_agg_cache',
        'aggregation_cache',
        ['run_id', 'aggregation_type', 'dimension_key'],
        unique=True
    )
    
    # Create materialized views for common aggregations
    op.execute("""
        CREATE MATERIALIZED VIEW IF NOT EXISTS mv_efficiency_by_year_sport AS
        SELECT 
            be.run_id,
            be.year,
            ps.sport_id,
            s.name as sport_name,
            SUM(be.allocated) as total_allocated,
            SUM(be.executed) as total_executed,
            AVG(be.execution_rate) as avg_execution_rate,
            COUNT(DISTINCT be.institution_id) as institution_count,
            COUNT(DISTINCT be.project_id) as project_count
        FROM budget_execution be
        JOIN project_sport ps ON ps.project_id = be.project_id
        JOIN sport s ON s.id = ps.sport_id
        GROUP BY be.run_id, be.year, ps.sport_id, s.name
    """)
    
    op.execute("""
        CREATE MATERIALIZED VIEW IF NOT EXISTS mv_roi_by_year_sport AS
        SELECT
            pm.run_id,
            EXTRACT(YEAR FROM pm.measured_on) as year,
            pm.sport_id,
            s.name as sport_name,
            COUNT(DISTINCT pm.indicator_id) as indicator_count,
            AVG(pm.normalized_value) as avg_normalized_score,
            SUM(pm.value) as total_value
        FROM performance_metric pm
        JOIN sport s ON s.id = pm.sport_id
        GROUP BY pm.run_id, EXTRACT(YEAR FROM pm.measured_on), pm.sport_id, s.name
    """)
    
    op.execute("""
        CREATE MATERIALIZED VIEW IF NOT EXISTS mv_region_summary AS
        SELECT
            ir.region_code,
            r.name as region_name,
            be.run_id,
            be.year,
            COUNT(DISTINCT ir.institution_id) as institution_count,
            SUM(be.allocated) as total_allocated,
            SUM(be.executed) as total_executed,
            AVG(be.execution_rate) as avg_execution_rate
        FROM institution_region ir
        JOIN region r ON r.code = ir.region_code
        JOIN budget_execution be ON be.institution_id = ir.institution_id
        WHERE ir.valid_to IS NULL
        GROUP BY ir.region_code, r.name, be.run_id, be.year
    """)
    
    # Create indexes on materialized views
    op.execute("CREATE UNIQUE INDEX idx_mv_eff_run_year_sport ON mv_efficiency_by_year_sport(run_id, year, sport_id)")
    op.execute("CREATE INDEX idx_mv_eff_year ON mv_efficiency_by_year_sport(year)")
    op.execute("CREATE INDEX idx_mv_eff_sport ON mv_efficiency_by_year_sport(sport_id)")
    
    op.execute("CREATE UNIQUE INDEX idx_mv_roi_run_year_sport ON mv_roi_by_year_sport(run_id, year, sport_id)")
    op.execute("CREATE INDEX idx_mv_roi_year ON mv_roi_by_year_sport(year)")
    op.execute("CREATE INDEX idx_mv_roi_sport ON mv_roi_by_year_sport(sport_id)")
    
    op.execute("CREATE UNIQUE INDEX idx_mv_region_run_year_code ON mv_region_summary(run_id, year, region_code)")
    op.execute("CREATE INDEX idx_mv_region_year ON mv_region_summary(year)")
    op.execute("CREATE INDEX idx_mv_region_code ON mv_region_summary(region_code)")


def downgrade() -> None:
    # Drop materialized views
    op.execute("DROP MATERIALIZED VIEW IF EXISTS mv_region_summary")
    op.execute("DROP MATERIALIZED VIEW IF EXISTS mv_roi_by_year_sport")
    op.execute("DROP MATERIALIZED VIEW IF EXISTS mv_efficiency_by_year_sport")
    
    # Drop aggregation cache table
    op.drop_table('aggregation_cache')