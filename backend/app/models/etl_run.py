"""ETL run record model"""
from sqlalchemy import Column, Integer, String, DateTime, Text, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base


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
    extra_metadata = Column("metadata", Text)  # JSON 형태의 추가 메타데이터
    
    @property
    def metadata(self):  # pragma: no cover - simple alias
        return self.extra_metadata
    
    @metadata.setter
    def metadata(self, value):  # pragma: no cover - simple alias
        self.extra_metadata = value
    
    # Relationships
    budget_executions = relationship("BudgetExecution", back_populates="etl_run")
    performance_metrics = relationship("PerformanceMetric", back_populates="etl_run")
    aggregations = relationship("AggregationCache", back_populates="etl_run")
    
    __table_args__ = (
        Index("idx_etl_status_source", "status", "source"),
        Index("idx_etl_started", "started_at"),
    )