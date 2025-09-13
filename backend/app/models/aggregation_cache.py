"""Aggregation cache model"""
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Numeric,
    Float,
    UniqueConstraint,
    Index,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base


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