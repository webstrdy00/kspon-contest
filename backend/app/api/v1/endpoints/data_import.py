"""
공공데이터 수집 및 임포트 API 엔드포인트
"""
from typing import Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
import logging

from app.db import get_db
from app.core.deps import get_current_user_optional
from app.services.facilities_api_client import FacilitiesAPIClient
from app.services.fund_api_client import FundAPIClient
from app.services.performance_api_client import PerformanceAPIClient

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/import/facilities")
async def import_facilities_data(
    background_tasks: BackgroundTasks,
    city_name: Optional[str] = None,
    facility_type: Optional[str] = None,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    전국공공체육시설 데이터 수집 시작
    
    백그라운드에서 실행되며 완료 시 데이터베이스에 저장됩니다.
    """
    try:
        # 백그라운드 태스크로 실행
        background_tasks.add_task(
            _import_facilities_task,
            db,
            city_name,
            facility_type
        )
        
        return {
            "status": "started",
            "message": "체육시설 데이터 수집이 시작되었습니다.",
            "filters": {
                "city_name": city_name,
                "facility_type": facility_type
            }
        }
    except Exception as e:
        logger.error(f"체육시설 데이터 수집 시작 실패: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/import/fund")
async def import_fund_data(
    background_tasks: BackgroundTasks,
    year: Optional[int] = None,
    organization: Optional[str] = None,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    국민체육진흥기금 지원실적 데이터 수집 시작
    """
    try:
        background_tasks.add_task(
            _import_fund_task,
            db,
            year,
            organization
        )
        
        return {
            "status": "started",
            "message": "기금 지원실적 데이터 수집이 시작되었습니다.",
            "filters": {
                "year": year,
                "organization": organization
            }
        }
    except Exception as e:
        logger.error(f"기금 데이터 수집 시작 실패: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/import/performance")
async def import_performance_data(
    background_tasks: BackgroundTasks,
    year: Optional[int] = None,
    sport_type: Optional[str] = None,
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    체육인복지 경기력향상성과금 데이터 수집 시작
    """
    try:
        background_tasks.add_task(
            _import_performance_task,
            db,
            year,
            sport_type
        )
        
        return {
            "status": "started",
            "message": "성과금 데이터 수집이 시작되었습니다.",
            "filters": {
                "year": year,
                "sport_type": sport_type
            }
        }
    except Exception as e:
        logger.error(f"성과금 데이터 수집 시작 실패: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analysis/budget-performance/{year}")
async def get_budget_performance_analysis(
    year: int,
    sport_type: Optional[str] = None
) -> Dict[str, Any]:
    """
    예산 대비 성과 분석 데이터 조회
    
    기금 지원 데이터와 성과금 데이터를 결합하여 ROI 분석
    """
    try:
        # 기금 클라이언트
        fund_client = FundAPIClient()
        performance_client = PerformanceAPIClient()
        
        # 종목별 예산 조회
        budget_by_sport = await fund_client.get_budget_by_sport(year)
        
        # ROI 분석
        roi_analysis = await performance_client.calculate_roi_by_sport(year, budget_by_sport)
        
        # 특정 종목만 필터링
        if sport_type:
            roi_analysis = {
                k: v for k, v in roi_analysis.items() 
                if sport_type.lower() in k.lower()
            }
        
        return {
            "year": year,
            "analysis": roi_analysis,
            "summary": {
                "total_sports": len(roi_analysis),
                "best_performing": max(roi_analysis.items(), key=lambda x: x[1].get("roi_score", 0))[0] if roi_analysis else None,
                "worst_performing": min(roi_analysis.items(), key=lambda x: x[1].get("roi_score", 0))[0] if roi_analysis else None
            }
        }
    except Exception as e:
        logger.error(f"예산-성과 분석 실패: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/statistics/facilities")
async def get_facilities_statistics() -> Dict[str, Any]:
    """
    체육시설 통계 데이터 조회
    """
    try:
        client = FacilitiesAPIClient()
        stats = await client.get_facility_statistics()
        
        return {
            "statistics": stats,
            "generated_at": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"체육시설 통계 조회 실패: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# 백그라운드 태스크 함수들
async def _import_facilities_task(
    db: Session,
    city_name: Optional[str],
    facility_type: Optional[str]
):
    """체육시설 데이터 수집 백그라운드 태스크"""
    try:
        client = FacilitiesAPIClient()
        facilities = await client.get_all_facilities(city_name, facility_type)
        
        # TODO: 데이터베이스에 저장
        logger.info(f"체육시설 데이터 {len(facilities)}개 수집 완료")
        
        # 데이터 파싱 및 저장
        for facility in facilities:
            parsed = client.parse_facility_data(facility)
            # TODO: DB 저장 로직
            
    except Exception as e:
        logger.error(f"체육시설 데이터 수집 실패: {str(e)}")


async def _import_fund_task(
    db: Session,
    year: Optional[int],
    organization: Optional[str]
):
    """기금 데이터 수집 백그라운드 태스크"""
    try:
        client = FundAPIClient()
        fund_data = await client.get_all_fund_support(year, organization)
        
        logger.info(f"기금 데이터 {len(fund_data)}개 수집 완료")
        
        # 데이터 파싱 및 저장
        for item in fund_data:
            parsed = client.parse_fund_data(item)
            # TODO: DB 저장 로직
            
    except Exception as e:
        logger.error(f"기금 데이터 수집 실패: {str(e)}")


async def _import_performance_task(
    db: Session,
    year: Optional[int],
    sport_type: Optional[str]
):
    """성과금 데이터 수집 백그라운드 태스크"""
    try:
        client = PerformanceAPIClient()
        performance_data = await client.get_all_performance_rewards(year, sport_type)
        
        logger.info(f"성과금 데이터 {len(performance_data)}개 수집 완료")
        
        # 데이터 파싱 및 저장
        for item in performance_data:
            parsed = client.parse_performance_data(item)
            # TODO: DB 저장 로직
            
    except Exception as e:
        logger.error(f"성과금 데이터 수집 실패: {str(e)}")


from datetime import datetime