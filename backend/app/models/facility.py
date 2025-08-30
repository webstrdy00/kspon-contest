from sqlalchemy import String, Float, Integer, Boolean, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship, Mapped, mapped_column
from geoalchemy2 import Geography
from typing import Optional, Dict, Any

from .base import Base


class SportsFacility(Base):
    """체육시설 모델 (전국공공체육시설 API 데이터)"""
    
    # 기본 정보
    facility_code: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    facility_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    sub_facility_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    # 위치 정보
    region_code: Mapped[str] = mapped_column(String(10), ForeignKey('region.code'), nullable=False, index=True)
    address: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    location: Mapped[str] = mapped_column(Geography('POINT', srid=4326), nullable=False)
    
    # 운영 정보
    operator: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    website: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    is_public: Mapped[bool] = mapped_column(Boolean, default=True)
    is_free: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # 추가 정보
    capacity: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    opening_hours: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    facilities_detail: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    
    # 관계
    region: Mapped["Region"] = relationship("Region", foreign_keys=[region_code])
    
    def __repr__(self):
        return f"<SportsFacility(name={self.name}, type={self.facility_type})>"


class FacilityDemand(Base):
    """시설 수요 데이터 (한국스포츠과학원 실태조사 데이터)"""
    
    region_code: Mapped[str] = mapped_column(String(10), ForeignKey('region.code'), nullable=False, index=True)
    facility_type: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    
    # 수요 정보
    demand_percentage: Mapped[float] = mapped_column(Float, nullable=False)
    survey_year: Mapped[int] = mapped_column(Integer, nullable=False)
    
    # 인구통계학적 세분화
    age_group: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    gender: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    occupation: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    income_level: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    
    # 관계
    region: Mapped["Region"] = relationship("Region", foreign_keys=[region_code])
    
    def __repr__(self):
        return f"<FacilityDemand(region={self.region_code}, type={self.facility_type}, demand={self.demand_percentage}%)>"