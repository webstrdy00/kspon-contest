from typing import List, Optional
from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.db import get_db


router = APIRouter()


class RegionalReportResponse(BaseModel):
    """지역별 리포트 응답 모델"""
    id: int
    region_code: str
    region_name: str
    report_title: str
    summary: Optional[str]
    generation_date: str
    view_count: int
    download_count: int
    rating_average: float


class ReportDetailResponse(BaseModel):
    """리포트 상세 응답 모델"""
    id: int
    region_code: str
    region_name: str
    report_title: str
    summary: Optional[str]
    key_insights: Optional[dict]
    facility_stats: Optional[dict]
    supply_demand_analysis: Optional[dict]
    budget_stats: Optional[dict]
    comparison_data: Optional[dict]
    charts_data: Optional[dict]
    generation_date: str


class ReportGenerationRequest(BaseModel):
    """리포트 생성 요청 모델"""
    region_code: str
    report_type: str = "comprehensive"  # comprehensive, facility, budget
    include_comparison: bool = True
    comparison_regions: Optional[List[str]] = None


@router.get("/", response_model=List[RegionalReportResponse])
async def get_regional_reports(
    region_code: Optional[str] = Query(None, description="지역 코드 필터"),
    report_type: Optional[str] = Query(None, description="리포트 유형 필터"),
    limit: int = Query(20, le=100, description="결과 개수 제한"),
    offset: int = Query(0, ge=0, description="결과 시작 위치"),
    db: Session = Depends(get_db)
):
    """지역별 리포트 목록 조회"""
    # TODO: 실제 데이터베이스 쿼리 구현
    return [
        RegionalReportResponse(
            id=1,
            region_code="11140",
            region_name="서울특별시 중구",
            report_title="중구 체육환경 종합 리포트",
            summary="중구는 20대 인구 비율이 높지만 젊은층 선호 시설이 부족합니다.",
            generation_date="2025-01-25T10:00:00",
            view_count=145,
            download_count=23,
            rating_average=4.2
        )
    ]


@router.get("/{report_id}", response_model=ReportDetailResponse)
async def get_report_detail(
    report_id: int,
    db: Session = Depends(get_db)
):
    """리포트 상세 조회"""
    # TODO: 실제 데이터베이스에서 리포트 조회
    return ReportDetailResponse(
        id=report_id,
        region_code="11140",
        region_name="서울특별시 중구",
        report_title="중구 체육환경 종합 리포트",
        summary="중구는 20대 인구 비율이 높지만 젊은층 선호 시설이 부족합니다.",
        key_insights={
            "population_characteristics": "20대 인구 비율 전국 평균 대비 15% 높음",
            "facility_shortage": "풋살장, 클라이밍짐 등 젊은층 선호 시설 부족",
            "budget_efficiency": "1인당 체육예산 서울시 평균 대비 85% 수준"
        },
        facility_stats={
            "total_facilities": 45,
            "public_facilities": 28,
            "facilities_per_1000_people": 3.2,
            "most_common_type": "체육관"
        },
        supply_demand_analysis={
            "high_demand_low_supply": ["풋살장", "클라이밍장"],
            "oversupplied": ["골프연습장"],
            "balanced": ["수영장", "체육관"]
        },
        budget_stats={
            "total_budget_2023": 2400000000,
            "per_capita_budget": 180000,
            "major_investments": ["체육센터 리모델링", "생활체육 프로그램"]
        },
        comparison_data={
            "vs_national_average": {
                "facilities_per_capita": 0.85,
                "budget_per_capita": 0.92,
                "satisfaction_score": 1.1
            },
            "vs_neighboring_regions": [
                {"region": "종로구", "facilities_ratio": 1.2},
                {"region": "용산구", "facilities_ratio": 0.9}
            ]
        },
        charts_data={
            "facility_distribution": [
                {"type": "체육관", "count": 12},
                {"type": "수영장", "count": 8},
                {"type": "테니스장", "count": 6}
            ],
            "age_group_demand": [
                {"age": "20대", "demand": 72},
                {"age": "30대", "demand": 65},
                {"age": "40대", "demand": 58}
            ]
        },
        generation_date="2025-01-25T10:00:00"
    )


@router.post("/generate")
async def generate_report(
    request: ReportGenerationRequest,
    db: Session = Depends(get_db)
):
    """새로운 리포트 생성"""
    # TODO: 리포트 생성 로직 구현
    return {
        "message": f"{request.region_code} 지역의 {request.report_type} 리포트 생성이 시작되었습니다.",
        "report_id": 123,
        "estimated_completion_time": "2-3분"
    }


@router.get("/{report_id}/download")
async def download_report_pdf(
    report_id: int,
    db: Session = Depends(get_db)
):
    """리포트 PDF 다운로드"""
    # TODO: PDF 파일 생성 및 다운로드 구현
    raise HTTPException(status_code=501, detail="PDF 다운로드 기능은 아직 구현중입니다.")