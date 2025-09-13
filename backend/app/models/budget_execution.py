"""Budget execution model"""
from sqlalchemy import (
    Column,
    Integer,
    Numeric,
    Float,
    ForeignKey,
    CheckConstraint,
    Index,
)
from sqlalchemy.orm import relationship

from .base import Base


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