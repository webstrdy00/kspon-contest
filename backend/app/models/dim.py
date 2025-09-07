"""
Dimension tables for budget-performance analysis system
"""
from sqlalchemy import Column, Integer, String, Float, Date, Boolean, ForeignKey, UniqueConstraint, CheckConstraint, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import text
from .base import Base


class Institution(Base):
    """기관 디멘션 테이블"""
    __tablename__ = "institution"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, index=True, nullable=False)
    type = Column(String(50))  # 중앙/지방/산하기관
    created_at = Column(Date)
    
    # Relationships
    regions = relationship("InstitutionRegion", back_populates="institution")
    budget_executions = relationship("BudgetExecution", back_populates="institution")


class Sport(Base):
    """종목 디멘션 테이블"""
    __tablename__ = "sport"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False)
    category = Column(String(50))  # 개인/단체/시설/혼합
    olympic_status = Column(Boolean, default=False)
    
    # Relationships
    projects = relationship("ProjectSport", back_populates="sport")
    metrics = relationship("PerformanceMetric", back_populates="sport")


class Project(Base):
    """사업 디멘션 테이블"""
    __tablename__ = "project"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, index=True, nullable=False)
    code = Column(String(50), unique=True)
    type = Column(String(50))  # 육성/지원/시설/연구
    description = Column(String(500))
    
    # Relationships
    sports = relationship("ProjectSport", back_populates="project")
    budget_executions = relationship("BudgetExecution", back_populates="project")


class InstitutionRegion(Base):
    """기관-지역 매핑 테이블 (SCD Type 2)"""
    __tablename__ = "institution_region"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    institution_id = Column(Integer, ForeignKey("institution.id"), nullable=False, index=True)
    region_code = Column(String(10), ForeignKey("region.code"), nullable=False, index=True)
    confidence = Column(Float, default=1.0)  # 매핑 신뢰도
    valid_from = Column(Date, nullable=False)
    valid_to = Column(Date)  # NULL이면 현재 유효
    source = Column(String(50))  # 매핑 출처
    
    # Relationships
    institution = relationship("Institution", back_populates="regions")
    region = relationship("Region", back_populates="institution_mappings")
    
    __table_args__ = (
        UniqueConstraint("institution_id", "region_code", "valid_from", name="uq_inst_region_valid"),
        Index(
            "idx_inst_region_current",
            "institution_id",
            "region_code",
            postgresql_where=text("valid_to IS NULL")
        ),
    )


class ProjectSport(Base):
    """사업-종목 매핑 테이블"""
    __tablename__ = "project_sport"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("project.id"), nullable=False, index=True)
    sport_id = Column(Integer, ForeignKey("sport.id"), nullable=False, index=True)
    priority = Column(Integer, default=1)  # 우선순위
    
    # Relationships
    project = relationship("Project", back_populates="sports")
    sport = relationship("Sport", back_populates="projects")
    
    __table_args__ = (
        UniqueConstraint("project_id", "sport_id", name="uq_project_sport"),
    )