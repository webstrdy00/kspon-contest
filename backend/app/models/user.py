from sqlalchemy import Column, String, Boolean, Integer, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from datetime import datetime

from .base import Base


class User(Base):
    """사용자 모델"""
    
    # 기본 정보
    username = Column(String(50), unique=True, nullable=False, index=True)  # 사용자명
    email = Column(String(100), unique=True, nullable=False, index=True)  # 이메일
    hashed_password = Column(String(255), nullable=False)  # 해시된 비밀번호
    
    # 프로필 정보
    display_name = Column(String(100), nullable=False)  # 표시명
    avatar_url = Column(String(500), nullable=True)  # 아바타 이미지 URL
    bio = Column(Text, nullable=True)  # 자기소개
    
    # 지역 정보
    region_code = Column(String(10), ForeignKey('region.code'), nullable=True, index=True)  # 거주지역
    interested_regions = Column(JSON, nullable=True)  # 관심 지역 목록
    
    # 계정 상태
    is_active = Column(Boolean, default=True)  # 활성 상태
    is_verified = Column(Boolean, default=False)  # 이메일 인증 상태
    
    # 활동 통계
    proposal_count = Column(Integer, default=0)  # 작성한 제안 수
    vote_count = Column(Integer, default=0)  # 투표 참여 수
    like_received = Column(Integer, default=0)  # 받은 공감 수
    report_count = Column(Integer, default=0)  # 생성한 리포트 수
    
    # 관심사
    interested_sports = Column(JSON, nullable=True)  # 관심 종목
    interested_facility_types = Column(JSON, nullable=True)  # 관심 시설 유형
    
    # 알림 설정
    notification_settings = Column(JSON, nullable=True)  # 알림 설정
    
    # 관계
    region = relationship("Region", foreign_keys=[region_code])
    proposals = relationship("Proposal", back_populates="author", cascade="all, delete-orphan")
    votes = relationship("ProposalVote", back_populates="user", cascade="all, delete-orphan")
    badges = relationship("UserBadge", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(username={self.username}, display_name={self.display_name})>"


class UserBadge(Base):
    """사용자 배지 모델"""
    
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False, index=True)
    badge_type = Column(String(50), nullable=False)  # 배지 유형
    badge_name = Column(String(100), nullable=False)  # 배지명
    badge_description = Column(Text, nullable=True)  # 배지 설명
    badge_icon = Column(String(500), nullable=True)  # 배지 아이콘 URL
    
    # 획득 정보
    earned_at = Column(DateTime, default=datetime.utcnow)  # 획득 일시
    earned_reason = Column(Text, nullable=True)  # 획득 사유
    
    # 관계
    user = relationship("User", back_populates="badges")
    
    def __repr__(self):
        return f"<UserBadge(user_id={self.user_id}, badge={self.badge_name})>"