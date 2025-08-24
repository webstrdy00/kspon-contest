from typing import List, Optional
from fastapi import APIRouter, Query
from pydantic import BaseModel


router = APIRouter()


class SupplyDemandData(BaseModel):
    """수요-공급 분석 데이터 모델"""
    region_code: str
    region_name: str
    facility_type: str
    supply_count: int
    demand_percentage: float
    supply_demand_ratio: float
    coordinates: List[float]


class BudgetPerformanceData(BaseModel):
    """예산-성과 분석 데이터 모델"""
    region_code: str
    region_name: str
    sport_type: str
    budget_amount: int
    performance_score: float
    efficiency_ratio: float


@router.get("/supply-demand", response_model=List[SupplyDemandData])
async def get_supply_demand_analysis(
    facility_type: Optional[str] = Query(None, description="시설 유형 필터"),
    region_code: Optional[str] = Query(None, description="지역 코드 필터"),
):
    """수요-공급 분석 데이터 조회"""
    # TODO: 실제 데이터베이스에서 조회
    return [
        SupplyDemandData(
            region_code="11140",
            region_name="서울특별시 중구",
            facility_type="수영장",
            supply_count=5,
            demand_percentage=68.5,
            supply_demand_ratio=0.7,
            coordinates=[126.9966, 37.5633]
        )
    ]


@router.get("/budget-performance", response_model=List[BudgetPerformanceData])
async def get_budget_performance_analysis(
    sport_type: Optional[str] = Query(None, description="종목 필터"),
    region_code: Optional[str] = Query(None, description="지역 코드 필터"),
):
    """예산-성과 분석 데이터 조회"""
    # TODO: 실제 데이터베이스에서 조회
    return [
        BudgetPerformanceData(
            region_code="11140",
            region_name="서울특별시 중구",
            sport_type="양궁",
            budget_amount=100000000,
            performance_score=85.2,
            efficiency_ratio=1.2
        )
    ]


@router.get("/stats")
async def get_dashboard_stats():
    """대시보드 통계 데이터 조회"""
    # TODO: 실제 통계 계산
    return {
        "total_facilities": 12543,
        "total_regions": 229,
        "total_proposals": 1847,
        "active_users": 3521
    }