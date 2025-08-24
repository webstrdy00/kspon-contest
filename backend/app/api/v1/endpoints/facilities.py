from typing import List, Optional
from fastapi import APIRouter, Query, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.db import get_db


router = APIRouter()


class FacilityResponse(BaseModel):
    """체육시설 응답 모델"""
    facility_code: str
    name: str
    facility_type: str
    address: Optional[str]
    latitude: float
    longitude: float
    region_code: str
    region_name: str
    operator: Optional[str]
    is_public: bool


class FacilityDemandResponse(BaseModel):
    """시설 수요 응답 모델"""
    region_code: str
    region_name: str
    facility_type: str
    demand_percentage: float
    survey_year: int


@router.get("/", response_model=List[FacilityResponse])
async def get_facilities(
    facility_type: Optional[str] = Query(None, description="시설 유형 필터"),
    region_code: Optional[str] = Query(None, description="지역 코드 필터"),
    limit: int = Query(100, le=1000, description="결과 개수 제한"),
    offset: int = Query(0, ge=0, description="결과 시작 위치"),
    db: Session = Depends(get_db)
):
    """체육시설 목록 조회"""
    # TODO: 실제 데이터베이스 쿼리 구현
    return [
        FacilityResponse(
            facility_code="FAC001",
            name="서울시민수영장",
            facility_type="수영장",
            address="서울특별시 중구 세종대로 110",
            latitude=37.5665,
            longitude=126.9780,
            region_code="11140",
            region_name="서울특별시 중구",
            operator="서울특별시",
            is_public=True
        )
    ]


@router.get("/demand", response_model=List[FacilityDemandResponse])
async def get_facility_demand(
    facility_type: Optional[str] = Query(None, description="시설 유형 필터"),
    region_code: Optional[str] = Query(None, description="지역 코드 필터"),
    db: Session = Depends(get_db)
):
    """시설 수요 데이터 조회"""
    # TODO: 실제 데이터베이스 쿼리 구현
    return [
        FacilityDemandResponse(
            region_code="11140",
            region_name="서울특별시 중구",
            facility_type="수영장",
            demand_percentage=68.5,
            survey_year=2023
        )
    ]


@router.get("/types")
async def get_facility_types(db: Session = Depends(get_db)):
    """사용 가능한 시설 유형 목록 조회"""
    # TODO: 실제 데이터베이스에서 시설 유형 목록 조회
    return {
        "facility_types": [
            "수영장", "체육관", "테니스장", "축구장", "야구장", 
            "농구장", "배드민턴장", "탁구장", "골프장", "스케이트장"
        ]
    }


@router.get("/statistics")
async def get_facility_statistics(
    region_code: Optional[str] = Query(None, description="지역 코드 필터"),
    db: Session = Depends(get_db)
):
    """시설 통계 조회"""
    # TODO: 실제 통계 계산
    return {
        "total_facilities": 12543,
        "public_facilities": 8765,
        "private_facilities": 3778,
        "by_type": {
            "체육관": 2341,
            "수영장": 876,
            "테니스장": 1456,
            "축구장": 987
        },
        "by_region_top5": [
            {"region_name": "서울특별시", "count": 2341},
            {"region_name": "부산광역시", "count": 1876},
            {"region_name": "대구광역시", "count": 1234}
        ]
    }