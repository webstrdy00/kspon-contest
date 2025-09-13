"""Performance metric model"""
from sqlalchemy import Column, Integer, Float, Date, ForeignKey, Index
from sqlalchemy.orm import relationship

from .base import Base


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