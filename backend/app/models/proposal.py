from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Text, JSON, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from .base import Base


class Proposal(Base):
    """정책 제안 모델"""
    
    # 기본 정보
    title = Column(String(300), nullable=False, index=True)  # 제안 제목
    content = Column(Text, nullable=False)  # 제안 내용
    summary = Column(Text, nullable=True)  # 요약
    
    # 작성자 정보
    author_id = Column(Integer, ForeignKey('user.id'), nullable=False, index=True)
    
    # 지역 정보
    target_region_code = Column(String(10), ForeignKey('region.code'), nullable=False, index=True)  # 대상 지역
    
    # 분류 정보
    category = Column(String(50), nullable=False, index=True)  # 카테고리 (시설, 예산, 정책 등)
    facility_type = Column(String(100), nullable=True)  # 관련 시설 유형
    sport_type = Column(String(100), nullable=True)  # 관련 종목
    
    # 근거 자료
    data_evidence = Column(JSON, nullable=True)  # 첨부된 데이터 근거 (차트, 통계 등)
    attached_files = Column(JSON, nullable=True)  # 첨부 파일 정보
    
    # 상태 정보
    status = Column(String(20), default='active', index=True)  # active, resolved, closed
    is_public = Column(Boolean, default=True)  # 공개 여부
    
    # 통계 정보
    view_count = Column(Integer, default=0)  # 조회수
    vote_up_count = Column(Integer, default=0)  # 찬성 투표 수
    vote_down_count = Column(Integer, default=0)  # 반대 투표 수
    comment_count = Column(Integer, default=0)  # 댓글 수
    
    # 랭킹 관련
    weekly_rank = Column(Integer, nullable=True)  # 주간 랭킹
    monthly_rank = Column(Integer, nullable=True)  # 월간 랭킹
    total_score = Column(Float, default=0.0)  # 종합 점수
    
    # 관계
    author = relationship("User", back_populates="proposals")
    target_region = relationship("Region", foreign_keys=[target_region_code])
    votes = relationship("ProposalVote", back_populates="proposal", cascade="all, delete-orphan")
    comments = relationship("ProposalComment", back_populates="proposal", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Proposal(title={self.title[:50]}..., votes={self.vote_up_count})>"


class ProposalVote(Base):
    """제안 투표 모델"""
    
    proposal_id = Column(Integer, ForeignKey('proposal.id'), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False, index=True)
    
    vote_type = Column(String(10), nullable=False)  # up, down
    
    # 관계
    proposal = relationship("Proposal", back_populates="votes")
    user = relationship("User", back_populates="votes")
    
    def __repr__(self):
        return f"<ProposalVote(proposal_id={self.proposal_id}, user_id={self.user_id}, type={self.vote_type})>"


class ProposalComment(Base):
    """제안 댓글 모델"""
    
    proposal_id = Column(Integer, ForeignKey('proposal.id'), nullable=False, index=True)
    author_id = Column(Integer, ForeignKey('user.id'), nullable=False, index=True)
    parent_comment_id = Column(Integer, ForeignKey('proposalcomment.id'), nullable=True)  # 대댓글 지원
    
    content = Column(Text, nullable=False)  # 댓글 내용
    
    # 상태
    is_deleted = Column(Boolean, default=False)  # 삭제 여부
    
    # 관계
    proposal = relationship("Proposal", back_populates="comments")
    author = relationship("User", foreign_keys=[author_id])
    parent_comment = relationship("ProposalComment", remote_side="ProposalComment.id")
    
    def __repr__(self):
        return f"<ProposalComment(proposal_id={self.proposal_id}, author_id={self.author_id})>"