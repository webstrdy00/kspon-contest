"""Indicator metadata model"""
from sqlalchemy import Column, Integer, String, Boolean, Text
from sqlalchemy.orm import relationship

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