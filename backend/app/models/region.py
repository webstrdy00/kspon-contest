from sqlalchemy import String, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column
from geoalchemy2 import Geography
from typing import Optional

from .base import Base


class Region(Base):
    """행정구역 모델 (시/도, 시/군/구)"""
    
    code: Mapped[str] = mapped_column(String(10), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    full_name: Mapped[str] = mapped_column(String(200), nullable=False)
    level: Mapped[str] = mapped_column(String(10), nullable=False)
    parent_code: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    
    # 지리적 정보
    geometry: Mapped[Optional[str]] = mapped_column(Geography('POLYGON', srid=4326), nullable=True)
    center_lat: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    center_lng: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    
    # 인구 및 통계 정보
    population: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    area_sqkm: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    
    def __repr__(self):
        return f"<Region(code={self.code}, name={self.name})>"