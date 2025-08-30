from sqlalchemy import String, Integer, Boolean, ForeignKey, Text, JSON, DateTime, Float
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from typing import Optional, List, Dict, Any

from .base import Base


class Proposal(Base):
    """정책 제안 모델"""
    
    # 기본 정보
    title: Mapped[str] = mapped_column(String(300), nullable=False, index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    
    # 작성자 정보
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False, index=True)
    
    # 지역 정보
    target_region_code: Mapped[str] = mapped_column(String(10), ForeignKey('region.code'), nullable=False, index=True)
    
    # 분류 정보
    category: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    facility_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    sport_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    
    # 근거 자료
    data_evidence: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    attached_files: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    
    # 상태 정보
    status: Mapped[str] = mapped_column(String(20), default='active', index=True)
    is_public: Mapped[bool] = mapped_column(Boolean, default=True)
    
    # 통계 정보
    view_count: Mapped[int] = mapped_column(Integer, default=0)
    vote_up_count: Mapped[int] = mapped_column(Integer, default=0)
    vote_down_count: Mapped[int] = mapped_column(Integer, default=0)
    comment_count: Mapped[int] = mapped_column(Integer, default=0)
    
    # 랭킹 관련
    weekly_rank: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    monthly_rank: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    total_score: Mapped[float] = mapped_column(Float, default=0.0)
    
    # 관계
    author: Mapped["User"] = relationship("User", back_populates="proposals")
    target_region: Mapped["Region"] = relationship("Region", foreign_keys=[target_region_code])
    votes: Mapped[List["ProposalVote"]] = relationship("ProposalVote", back_populates="proposal", cascade="all, delete-orphan")
    comments: Mapped[List["ProposalComment"]] = relationship("ProposalComment", back_populates="proposal", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Proposal(title={self.title[:50]}..., votes={self.vote_up_count})>"


class ProposalVote(Base):
    """제안 투표 모델"""
    
    proposal_id: Mapped[int] = mapped_column(Integer, ForeignKey('proposal.id'), nullable=False, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False, index=True)
    
    vote_type: Mapped[str] = mapped_column(String(10), nullable=False)
    
    # 관계
    proposal: Mapped["Proposal"] = relationship("Proposal", back_populates="votes")
    user: Mapped["User"] = relationship("User", back_populates="votes")
    
    def __repr__(self):
        return f"<ProposalVote(proposal_id={self.proposal_id}, user_id={self.user_id}, type={self.vote_type})>"


class ProposalComment(Base):
    """제안 댓글 모델"""
    
    proposal_id: Mapped[int] = mapped_column(Integer, ForeignKey('proposal.id'), nullable=False, index=True)
    author_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=False, index=True)
    parent_comment_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey('proposalcomment.id'), nullable=True)
    
    content: Mapped[str] = mapped_column(Text, nullable=False)
    
    # 상태
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # 관계
    proposal: Mapped["Proposal"] = relationship("Proposal", back_populates="comments")
    author: Mapped["User"] = relationship("User", foreign_keys=[author_id])
    parent_comment: Mapped[Optional["ProposalComment"]] = relationship("ProposalComment", remote_side="ProposalComment.id")
    
    def __repr__(self):
        return f"<ProposalComment(proposal_id={self.proposal_id}, author_id={self.author_id})>"