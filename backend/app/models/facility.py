from sqlalchemy import Column, String, Float, Integer, Boolean, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from geoalchemy2 import Geography

from .base import Base


class SportsFacility(Base):
    """체육시설 모델 (전국공공체육시설 API 데이터)"""
    
    # 기본 정보
    facility_code = Column(String(50), unique=True, nullable=False, index=True)  # 시설 코드
    name = Column(String(200), nullable=False)  # 시설명
    facility_type = Column(String(100), nullable=False, index=True)  # 시설유형명
    sub_facility_type = Column(String(100), nullable=True)  # 세부 시설유형
    
    # 위치 정보
    region_code = Column(String(10), ForeignKey('region.code'), nullable=False, index=True)
    address = Column(Text, nullable=True)  # 주소
    latitude = Column(Float, nullable=False)  # 위도
    longitude = Column(Float, nullable=False)  # 경도
    location = Column(Geography('POINT', srid=4326), nullable=False)  # PostGIS Point
    
    # 운영 정보
    operator = Column(String(200), nullable=True)  # 운영기관
    phone = Column(String(20), nullable=True)  # 전화번호
    website = Column(String(500), nullable=True)  # 홈페이지
    is_public = Column(Boolean, default=True)  # 공공시설 여부
    is_free = Column(Boolean, default=False)  # 무료 여부
    
    # 추가 정보
    capacity = Column(Integer, nullable=True)  # 수용인원
    opening_hours = Column(JSON, nullable=True)  # 운영시간
    facilities_detail = Column(JSON, nullable=True)  # 세부시설 정보
    
    # 관계
    region = relationship("Region", foreign_keys=[region_code])
    
    def __repr__(self):
        return f"<SportsFacility(name={self.name}, type={self.facility_type})>"


class FacilityDemand(Base):
    """시설 수요 데이터 (한국스포츠과학원 실태조사 데이터)"""
    
    region_code = Column(String(10), ForeignKey('region.code'), nullable=False, index=True)
    facility_type = Column(String(100), nullable=False, index=True)  # 시설 유형
    
    # 수요 정보
    demand_percentage = Column(Float, nullable=False)  # 필요하다고 응답한 비율(%)
    survey_year = Column(Integer, nullable=False)  # 조사 연도
    
    # 인구통계학적 세분화
    age_group = Column(String(20), nullable=True)  # 연령대 (20대, 30대 등)
    gender = Column(String(10), nullable=True)  # 성별
    occupation = Column(String(50), nullable=True)  # 직업군
    income_level = Column(String(20), nullable=True)  # 소득수준
    
    # 관계
    region = relationship("Region", foreign_keys=[region_code])
    
    def __repr__(self):
        return f"<FacilityDemand(region={self.region_code}, type={self.facility_type}, demand={self.demand_percentage}%)>"