"""
Budget and Performance metric tables for analysis system
"""
from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Boolean, ForeignKey, Text, CheckConstraint, Index, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .base import Base


class IndicatorMeta(Base):
    """성과 지표 메타데이터"""
    __tablename__ = "indicator_meta"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)
    description = Column(Text)
    value_type = Column(String(20), nullable=False)  # int/float/percentage
    aggregation_rule = Column(String(20), nullable=False)  # sum/avg/weighted/max/min
    scaling = Column(String(20), default="none")  # none/minmax/zscore/log
    direction_positive = Column(Boolean, default=True)  # True면 값이 클수록 좋음
    unit = Column(String(50))  # 단위 (명, 원, %, 점 등)
    category = Column(String(50))  # 참여/만족도/성과/효율성
    
    # Relationships
    metrics = relationship("PerformanceMetric", back_populates="indicator")


class PerformanceMetric(Base):
    """성과 측정 데이터"""
    __tablename__ = "performance_metric"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    sport_id = Column(Integer, ForeignKey("sport.id"), nullable=False, index=True)
    indicator_id = Column(Integer, ForeignKey("indicator_meta.id"), nullable=False, index=True)
    institution_id = Column(Integer, ForeignKey("institution.id"), index=True)
    measured_on = Column(Date, nullable=False, index=True)
    value = Column(Float, nullable=False)
    normalized_value = Column(Float)  # 정규화된 값
    run_id = Column(Integer, ForeignKey("etl_runs.run_id"), nullable=False, index=True)
    
    # Relationships
    sport = relationship("Sport", back_populates="metrics")
    indicator = relationship("IndicatorMeta", back_populates="metrics")
    institution = relationship("Institution")
    etl_run = relationship("EtlRun", back_populates="performance_metrics")
    
    __table_args__ = (
        Index("idx_perf_sport_date", "sport_id", "measured_on"),
        Index("idx_perf_run_indicator", "run_id", "indicator_id"),
    )


class BudgetExecution(Base):
    """예산 집행 데이터"""
    __tablename__ = "budget_execution"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(Integer, nullable=False, index=True)
    quarter = Column(Integer)  # 1-4, NULL이면 연간
    institution_id = Column(Integer, ForeignKey("institution.id"), nullable=False, index=True)
    project_id = Column(Integer, ForeignKey("project.id"), nullable=False, index=True)
    allocated = Column(Numeric(18, 2), nullable=False)  # 배정 예산
    executed = Column(Numeric(18, 2), nullable=False)  # 집행 예산
    execution_rate = Column(Float)  # 집행률 (%)
    run_id = Column(Integer, ForeignKey("etl_runs.run_id"), nullable=False, index=True)
    
    # Relationships
    institution = relationship("Institution", back_populates="budget_executions")
    project = relationship("Project", back_populates="budget_executions")
    etl_run = relationship("EtlRun", back_populates="budget_executions")
    
    __table_args__ = (
        CheckConstraint("executed <= allocated", name="chk_budget_execution"),
        CheckConstraint("execution_rate >= 0 AND execution_rate <= 100", name="chk_execution_rate"),
        Index("idx_budget_year_inst_proj", "year", "institution_id", "project_id"),
    )


class EtlRun(Base):
    """ETL 실행 이력 테이블"""
    __tablename__ = "etl_runs"
    
    run_id = Column(Integer, primary_key=True, autoincrement=True)
    source = Column(String(50), nullable=False)  # budget/performance/mapping
    schema_version = Column(String(20))  # v1.0, v1.1 등
    started_at = Column(DateTime, nullable=False, default=func.now())
    finished_at = Column(DateTime)
    status = Column(String(20), nullable=False, default="running")  # running/success/failed/partial
    row_count = Column(Integer, default=0)
    error_message = Column(Text)
    task_id = Column(String(50))  # Celery/RQ task ID
    retry_count = Column(Integer, default=0)
    metadata = Column(Text)  # JSON 형태의 추가 메타데이터
    
    # Relationships
    budget_executions = relationship("BudgetExecution", back_populates="etl_run")
    performance_metrics = relationship("PerformanceMetric", back_populates="etl_run")
    aggregations = relationship("AggregationCache", back_populates="etl_run")
    
    __table_args__ = (
        Index("idx_etl_status_source", "status", "source"),
        Index("idx_etl_started", "started_at"),
    )


class AggregationCache(Base):
    """집계 캐시 테이블 (Materialized View 대체)"""
    __tablename__ = "aggregation_cache"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    run_id = Column(Integer, ForeignKey("etl_runs.run_id"), nullable=False, index=True)
    aggregation_type = Column(String(50), nullable=False)  # efficiency/roi/trend/region
    dimension_key = Column(String(255), nullable=False)  # year:2024:sport:1 형태
    year = Column(Integer, index=True)
    sport_id = Column(Integer, ForeignKey("sport.id"), index=True)
    region_code = Column(String(10), ForeignKey("region.code"), index=True)
    
    # 집계 값들
    budget_total = Column(Numeric(18, 2))
    budget_executed = Column(Numeric(18, 2))
    performance_score = Column(Float)
    efficiency = Column(Float)
    roi = Column(Float)
    rank = Column(Integer)
    grade = Column(String(2))  # S/A/B/C/D
    
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    etl_run = relationship("EtlRun", back_populates="aggregations")
    sport = relationship("Sport")
    region = relationship("Region")
    
    __table_args__ = (
        UniqueConstraint("run_id", "aggregation_type", "dimension_key", name="uq_agg_cache"),
        Index("idx_agg_type_year", "aggregation_type", "year"),
        Index("idx_agg_run_type", "run_id", "aggregation_type"),
    )