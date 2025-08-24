from typing import List, Optional
from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.db import get_db


router = APIRouter()


class ProposalResponse(BaseModel):
    """정책 제안 응답 모델"""
    id: int
    title: str
    summary: Optional[str]
    author_name: str
    target_region_code: str
    target_region_name: str
    category: str
    vote_up_count: int
    vote_down_count: int
    view_count: int
    created_at: str
    status: str


class ProposalDetailResponse(BaseModel):
    """정책 제안 상세 응답 모델"""
    id: int
    title: str
    content: str
    summary: Optional[str]
    author_name: str
    target_region_code: str
    target_region_name: str
    category: str
    facility_type: Optional[str]
    sport_type: Optional[str]
    data_evidence: Optional[dict]
    vote_up_count: int
    vote_down_count: int
    view_count: int
    comment_count: int
    weekly_rank: Optional[int]
    monthly_rank: Optional[int]
    created_at: str
    updated_at: str
    status: str


class ProposalCreateRequest(BaseModel):
    """정책 제안 생성 요청 모델"""
    title: str
    content: str
    summary: Optional[str]
    target_region_code: str
    category: str
    facility_type: Optional[str] = None
    sport_type: Optional[str] = None
    data_evidence: Optional[dict] = None


class ProposalVoteRequest(BaseModel):
    """투표 요청 모델"""
    vote_type: str  # up, down


@router.get("/", response_model=List[ProposalResponse])
async def get_proposals(
    category: Optional[str] = Query(None, description="카테고리 필터"),
    region_code: Optional[str] = Query(None, description="지역 코드 필터"),
    status: Optional[str] = Query("active", description="상태 필터"),
    sort_by: str = Query("recent", description="정렬 기준: recent, popular, votes"),
    limit: int = Query(20, le=100, description="결과 개수 제한"),
    offset: int = Query(0, ge=0, description="결과 시작 위치"),
    db: Session = Depends(get_db)
):
    """정책 제안 목록 조회"""
    # TODO: 실제 데이터베이스 쿼리 구현
    return [
        ProposalResponse(
            id=1,
            title="마포구 홍대 인근 실내 클라이밍짐 설치 요청",
            summary="20대 인구가 많은 마포구에 젊은층이 선호하는 클라이밍 시설이 부족합니다.",
            author_name="김체육",
            target_region_code="11440",
            target_region_name="서울특별시 마포구",
            category="시설",
            vote_up_count=247,
            vote_down_count=13,
            view_count=1205,
            created_at="2025-01-20T14:30:00",
            status="active"
        ),
        ProposalResponse(
            id=2,
            title="강남구 생활체육 프로그램 확대 제안",
            summary="직장인들을 위한 야간 생활체육 프로그램이 부족합니다.",
            author_name="이건강",
            target_region_code="11680",
            target_region_name="서울특별시 강남구",
            category="프로그램",
            vote_up_count=189,
            vote_down_count=8,
            view_count=856,
            created_at="2025-01-18T09:15:00",
            status="active"
        )
    ]


@router.get("/{proposal_id}", response_model=ProposalDetailResponse)
async def get_proposal_detail(
    proposal_id: int,
    db: Session = Depends(get_db)
):
    """정책 제안 상세 조회"""
    # TODO: 실제 데이터베이스에서 제안 조회 및 조회수 증가
    return ProposalDetailResponse(
        id=proposal_id,
        title="마포구 홍대 인근 실내 클라이밍짐 설치 요청",
        content="마포구는 20대 인구 비율이 전국 평균보다 15% 높지만, 젊은층이 선호하는 클라이밍 시설은 1곳뿐입니다. 특히 홍대 인근 지역은 대학생과 젊은 직장인이 많이 거주하지만 가까운 곳에 클라이밍 시설이 없어 타 지역으로 이동해야 하는 불편함이 있습니다.",
        summary="20대 인구가 많은 마포구에 젊은층이 선호하는 클라이밍 시설이 부족합니다.",
        author_name="김체육",
        target_region_code="11440",
        target_region_name="서울특별시 마포구",
        category="시설",
        facility_type="클라이밍장",
        sport_type="클라이밍",
        data_evidence={
            "population_chart": "20대 인구 비율 차트 데이터",
            "facility_distribution": "클라이밍장 분포 지도 데이터",
            "demand_survey": "체육시설 수요 조사 결과"
        },
        vote_up_count=247,
        vote_down_count=13,
        view_count=1205,
        comment_count=34,
        weekly_rank=1,
        monthly_rank=3,
        created_at="2025-01-20T14:30:00",
        updated_at="2025-01-20T14:30:00",
        status="active"
    )


@router.post("/")
async def create_proposal(
    request: ProposalCreateRequest,
    db: Session = Depends(get_db)
):
    """새로운 정책 제안 생성"""
    # TODO: 사용자 인증 확인 및 제안 생성
    return {
        "message": "정책 제안이 성공적으로 등록되었습니다.",
        "proposal_id": 123
    }


@router.post("/{proposal_id}/vote")
async def vote_proposal(
    proposal_id: int,
    request: ProposalVoteRequest,
    db: Session = Depends(get_db)
):
    """정책 제안 투표"""
    # TODO: 사용자 인증 확인 및 투표 처리
    if request.vote_type not in ["up", "down"]:
        raise HTTPException(status_code=400, detail="유효하지 않은 투표 유형입니다.")
    
    return {
        "message": f"투표가 완료되었습니다. ({request.vote_type})",
        "current_votes": {
            "up": 248 if request.vote_type == "up" else 247,
            "down": 13 if request.vote_type == "down" else 13
        }
    }


@router.get("/rankings/weekly")
async def get_weekly_rankings(
    limit: int = Query(10, le=50, description="결과 개수 제한"),
    db: Session = Depends(get_db)
):
    """주간 인기 제안 랭킹"""
    # TODO: 실제 랭킹 계산
    return {
        "period": "2025년 1월 3주차",
        "rankings": [
            {
                "rank": 1,
                "proposal_id": 1,
                "title": "마포구 홍대 인근 실내 클라이밍짐 설치 요청",
                "vote_count": 247,
                "region_name": "서울특별시 마포구"
            },
            {
                "rank": 2,
                "proposal_id": 2,
                "title": "강남구 생활체육 프로그램 확대 제안",
                "vote_count": 189,
                "region_name": "서울특별시 강남구"
            }
        ]
    }


@router.get("/categories")
async def get_proposal_categories(db: Session = Depends(get_db)):
    """제안 카테고리 목록 조회"""
    return {
        "categories": [
            {"value": "시설", "label": "체육시설", "description": "새로운 체육시설 건설이나 기존 시설 개선"},
            {"value": "프로그램", "label": "생활체육 프로그램", "description": "생활체육 프로그램 신설이나 확대"},
            {"value": "예산", "label": "예산 및 지원", "description": "체육 분야 예산 배정이나 지원 정책"},
            {"value": "정책", "label": "정책 개선", "description": "체육 관련 제도나 정책 개선"}
        ]
    }