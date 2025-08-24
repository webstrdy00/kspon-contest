from sqlalchemy import Column, String, Integer, ForeignKey, Text, JSON, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime

from .base import Base


class RegionalReport(Base):
    """지역별 리포트 모델"""
    
    # 기본 정보
    region_code = Column(String(10), ForeignKey('region.code'), nullable=False, index=True)
    report_title = Column(String(300), nullable=False)  # 리포트 제목
    report_type = Column(String(50), default='comprehensive', index=True)  # comprehensive, facility, budget
    
    # 생성 정보
    generated_by_user_id = Column(Integer, ForeignKey('user.id'), nullable=True, index=True)  # 요청한 사용자
    generation_date = Column(DateTime, default=datetime.utcnow)  # 생성 일시
    
    # 리포트 데이터
    summary = Column(Text, nullable=True)  # 요약
    key_insights = Column(JSON, nullable=True)  # 주요 인사이트
    
    # 시설 현황 데이터
    facility_stats = Column(JSON, nullable=True)  # 시설 통계
    supply_demand_analysis = Column(JSON, nullable=True)  # 수요-공급 분석
    
    # 예산 및 성과 데이터
    budget_stats = Column(JSON, nullable=True)  # 예산 통계
    performance_stats = Column(JSON, nullable=True)  # 성과 통계
    
    # 비교 분석 데이터
    comparison_data = Column(JSON, nullable=True)  # 타 지역 대비 비교
    national_average_comparison = Column(JSON, nullable=True)  # 전국 평균 대비 비교
    
    # 차트 및 시각화 데이터
    charts_data = Column(JSON, nullable=True)  # 차트 데이터
    map_data = Column(JSON, nullable=True)  # 지도 데이터
    
    # 파일 정보
    pdf_file_path = Column(String(500), nullable=True)  # PDF 파일 경로
    pdf_generated_at = Column(DateTime, nullable=True)  # PDF 생성 일시
    
    # 통계
    view_count = Column(Integer, default=0)  # 조회수
    download_count = Column(Integer, default=0)  # 다운로드 수
    
    # 평가
    rating_average = Column(Float, default=0.0)  # 평균 평점
    rating_count = Column(Integer, default=0)  # 평점 개수
    
    # 관계
    region = relationship("Region", foreign_keys=[region_code])
    generated_by = relationship("User", foreign_keys=[generated_by_user_id])
    ratings = relationship("ReportRating", back_populates="report", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<RegionalReport(region={self.region_code}, type={self.report_type}, date={self.generation_date})>"


class ReportRating(Base):
    """리포트 평가 모델"""
    
    report_id = Column(Integer, ForeignKey('regionalreport.id'), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False, index=True)
    
    rating = Column(Integer, nullable=False)  # 1-5 점 평점
    feedback = Column(Text, nullable=True)  # 피드백 코멘트
    
    # 관계
    report = relationship("RegionalReport", back_populates="ratings")
    user = relationship("User", foreign_keys=[user_id])
    
    def __repr__(self):
        return f"<ReportRating(report_id={self.report_id}, user_id={self.user_id}, rating={self.rating})>"