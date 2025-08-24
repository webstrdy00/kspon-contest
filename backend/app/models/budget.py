from sqlalchemy import Column, String, Integer, Float, ForeignKey, Text, Date
from sqlalchemy.orm import relationship

from .base import Base


class SportsbudgetSupport(Base):
    """체육 예산 지원 데이터 (국민체육진흥기금 API 데이터)"""
    
    # 기본 정보
    support_id = Column(String(100), unique=True, nullable=False, index=True)  # 지원 ID
    business_name = Column(String(300), nullable=False)  # 사업명
    detailed_business = Column(String(300), nullable=True)  # 세부사업명
    
    # 지원 정보
    support_amount = Column(Integer, nullable=False)  # 지원금액 (원)
    support_year = Column(Integer, nullable=False, index=True)  # 지원년도
    support_date = Column(Date, nullable=True)  # 지원일자
    
    # 대상 정보
    target_organization = Column(String(300), nullable=False)  # 지원대상기관
    region_code = Column(String(10), ForeignKey('region.code'), nullable=True, index=True)  # 추정 지역코드
    sport_type = Column(String(100), nullable=True, index=True)  # 종목 (텍스트 분석으로 추출)
    
    # 분류 정보
    support_category = Column(String(100), nullable=True)  # 지원 분야 (시설, 인력, 프로그램 등)
    business_type = Column(String(100), nullable=True)  # 사업 유형
    
    # 메모 및 추가 정보
    description = Column(Text, nullable=True)  # 상세 설명
    notes = Column(Text, nullable=True)  # 메모 (데이터 처리 과정에서 추가된 정보)
    
    # 관계
    region = relationship("Region", foreign_keys=[region_code])
    
    def __repr__(self):
        return f"<SportsbudgetSupport(business={self.business_name}, amount={self.support_amount:,}원)>"


class PerformanceReward(Base):
    """경기력 향상 성과금 데이터 (체육인복지 API 데이터)"""
    
    # 기본 정보
    reward_id = Column(String(100), unique=True, nullable=False, index=True)  # 성과금 ID
    sport_type = Column(String(100), nullable=False, index=True)  # 종목명
    
    # 성과 정보
    monthly_amount = Column(Integer, nullable=False)  # 월정금액 (원)
    performance_level = Column(String(50), nullable=True)  # 성과 등급 (금메달, 은메달 등)
    competition_type = Column(String(100), nullable=True)  # 대회 유형 (올림픽, 아시안게임 등)
    
    # 시기 정보
    award_year = Column(Integer, nullable=False, index=True)  # 수여 연도
    award_date = Column(Date, nullable=True)  # 수여일자
    
    # 지역 정보 (추가 데이터로 보완 필요)
    estimated_region_code = Column(String(10), ForeignKey('region.code'), nullable=True, index=True)
    athlete_info = Column(Text, nullable=True)  # 선수 정보 (개인정보 제외)
    
    # 관계
    region = relationship("Region", foreign_keys=[estimated_region_code])
    
    def __repr__(self):
        return f"<PerformanceReward(sport={self.sport_type}, amount={self.monthly_amount:,}원/월)>"