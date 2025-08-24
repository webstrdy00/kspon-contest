from sqlalchemy import Column, String, Float, Integer
from geoalchemy2 import Geography

from .base import Base


class Region(Base):
    """행정구역 모델 (시/도, 시/군/구)"""
    
    code = Column(String(10), unique=True, nullable=False, index=True)  # 행정구역 코드
    name = Column(String(100), nullable=False)  # 지역명
    full_name = Column(String(200), nullable=False)  # 전체 지역명 (예: 서울특별시 강남구)
    level = Column(String(10), nullable=False)  # sido, sigungu
    parent_code = Column(String(10), nullable=True)  # 상위 행정구역 코드
    
    # 지리적 정보
    geometry = Column(Geography('POLYGON', srid=4326), nullable=True)  # 행정구역 경계
    center_lat = Column(Float, nullable=True)  # 중심 위도
    center_lng = Column(Float, nullable=True)  # 중심 경도
    
    # 인구 및 통계 정보
    population = Column(Integer, nullable=True)  # 인구수
    area_sqkm = Column(Float, nullable=True)  # 면적(㎢)
    
    def __repr__(self):
        return f"<Region(code={self.code}, name={self.name})>"