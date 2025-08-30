from sqlalchemy import String, Boolean, Integer, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from typing import Optional, List, Dict, Any

from .base import Base


class User(Base):
    """사용자 모델"""
    
    # 기본 정보
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # 프로필 정보
    display_name: Mapped[str] = mapped_column(String(100), nullable=False)
    avatar_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    bio: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # 지역 정보
    region_code: Mapped[Optional[str]] = mapped_column(String(10), ForeignKey('region.code'), nullable=True, index=True)
    interested_regions: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    
    # 계정 상태
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # 활동 통계
    proposal_count: Mapped[int] = mapped_column(Integer, default=0)
    vote_count: Mapped[int] = mapped_column(Integer, default=0)
    like_received: Mapped[int] = mapped_column(Integer, default=0)
    report_count: Mapped[int] = mapped_column(Integer, default=0)
    
    # 관심사
    interested_sports: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    interested_facility_types: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    
    # 알림 설정
    notification_settings: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    
    # 관계
    region: Mapped[Optional["Region"]] = relationship("Region", foreign_keys=[region_code])
    proposals: Mapped[List["Proposal"]] = relationship("Proposal", back_populates="author", cascade="all, delete-orphan")
    votes: Mapped[List["ProposalVote"]] = relationship("ProposalVote", back_populates="user", cascade="all, delete-orphan")
    badges: Mapped[List["UserBadge"]] = relationship("UserBadge", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(username={self.username}, display_name={self.display_name})>"


class UserBadge(Base):
    """사용자 배지 모델"""
    
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False, index=True)
    badge_type: Mapped[str] = mapped_column(String(50), nullable=False)
    badge_name: Mapped[str] = mapped_column(String(100), nullable=False)
    badge_description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    badge_icon: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    # 획득 정보
    earned_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    earned_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # 관계
    user: Mapped["User"] = relationship("User", back_populates="badges")
    
    def __repr__(self):
        return f"<UserBadge(user_id={self.user_id}, badge={self.badge_name})>"