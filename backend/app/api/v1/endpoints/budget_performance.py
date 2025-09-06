"""
Budget-Performance Analysis API Endpoints
예산-성과 분석 API 엔드포인트
"""
from typing import List, Optional, Dict, Any
from datetime import datetime, date
import logging

from fastapi import APIRouter, Depends, HTTPException, Query, Header, Response, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_async_db
from app.core.deps import get_current_active_user
from app.core.cache import cache_manager
from app.models.user import User
from app.services.budget_analysis import BudgetAnalysisService
from app.schemas.budget_performance import (
    BudgetPerformanceOverview,
    BudgetPerformanceFilter,
    EfficiencyAnalysis,
    ROIAnalysis,
    TrendData,
    RegionComparison,
    ExportRequest
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/budget-performance", tags=["budget-performance"])


@router.on_event("startup")
async def startup_event():
    """API 시작 시 Redis 연결"""
    await cache_manager.connect()


@router.on_event("shutdown")
async def shutdown_event():
    """API 종료 시 Redis 연결 해제"""
    await cache_manager.disconnect()


@router.get("/meta/latest-run", response_model=Dict[str, Any])
async def get_latest_run(
    db: AsyncSession = Depends(get_async_db)
) -> Dict[str, Any]:
    """최신 ETL 실행 정보 조회"""
    service = BudgetAnalysisService(db)
    
    try:
        run_id = await service.get_latest_run_id()
        
        # ETL 실행 정보 조회
        from app.models import EtlRun
        from sqlalchemy import select
        
        stmt = select(EtlRun).where(EtlRun.run_id == run_id)
        result = await db.execute(stmt)
        etl_run = result.scalar_one_or_none()
        
        if not etl_run:
            raise HTTPException(
                status_code=404,
                detail="ETL 실행 정보를 찾을 수 없습니다"
            )
        
        return {
            "run_id": etl_run.run_id,
            "source": etl_run.source,
            "schema_version": etl_run.schema_version,
            "started_at": etl_run.started_at.isoformat() if etl_run.started_at else None,
            "finished_at": etl_run.finished_at.isoformat() if etl_run.finished_at else None,
            "status": etl_run.status,
            "row_count": etl_run.row_count
        }
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"최신 실행 정보 조회 실패: {e}")
        raise HTTPException(status_code=500, detail="내부 서버 오류")


@router.get("/overview", response_model=BudgetPerformanceOverview)
async def get_overview(
    response: Response,
    year: Optional[int] = Query(None, ge=2020, le=2030),
    region_code: Optional[str] = Query(None),
    sport_id: Optional[int] = Query(None),
    institution_id: Optional[int] = Query(None),
    group_by: Optional[str] = Query(None, regex="^(region|sport|institution|project)$"),
    granularity: Optional[str] = Query(None, regex="^(year|quarter|month)$"),
    if_none_match: Optional[str] = Header(None),
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_active_user)
) -> BudgetPerformanceOverview:
    """
    예산-성과 분석 개요 조회
    
    - 요약 통계
    - 하이라이트
    - 종목별 효율성
    - ROI 상위 수행자
    - 지역별 비교
    - 트렌드 데이터
    """
    service = BudgetAnalysisService(db)
    
    try:
        # 필터 생성
        filters = BudgetPerformanceFilter(
            year=year,
            region_code=region_code,
            sport_id=sport_id,
            institution_id=institution_id,
            group_by=group_by,
            granularity=granularity
        )
        
        # 최신 run_id 조회
        run_id = await service.get_latest_run_id()
        
        # 캐시 키 생성
        cache_params = {
            "year": year,
            "region_code": region_code,
            "sport_id": sport_id,
            "institution_id": institution_id,
            "group_by": group_by,
            "granularity": granularity
        }
        
        # 캐시 조회
        cached_data = await cache_manager.get("overview", cache_params, run_id)
        
        if cached_data:
            # ETag 생성 및 비교
            etag = cache_manager.generate_etag(cached_data, run_id)
            
            if if_none_match and if_none_match == etag:
                # 304 Not Modified
                return Response(status_code=status.HTTP_304_NOT_MODIFIED)
            
            response.headers["ETag"] = etag
            response.headers["Cache-Control"] = "public, max-age=300"
            return BudgetPerformanceOverview(**cached_data)
        
        # 데이터 조회
        overview = await service.get_overview(filters)
        
        # 딕셔너리로 변환
        overview_dict = overview.model_dump()
        
        # 캐시 저장
        await cache_manager.set(
            "overview",
            overview_dict,
            cache_params,
            run_id,
            ttl=300  # 5분
        )
        
        # ETag 생성
        etag = cache_manager.generate_etag(overview_dict, run_id)
        response.headers["ETag"] = etag
        response.headers["Cache-Control"] = "public, max-age=300"
        
        return overview
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"개요 조회 실패: {e}")
        raise HTTPException(status_code=500, detail="내부 서버 오류")


@router.get("/efficiency", response_model=List[EfficiencyAnalysis])
async def get_efficiency_analysis(
    response: Response,
    year: int = Query(..., ge=2020, le=2030),
    limit: int = Query(10, ge=1, le=100),
    if_none_match: Optional[str] = Header(None),
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_active_user)
) -> List[EfficiencyAnalysis]:
    """종목별 효율성 분석"""
    service = BudgetAnalysisService(db)
    
    try:
        # 최신 run_id 조회
        run_id = await service.get_latest_run_id()
        
        # 캐시 파라미터
        cache_params = {"year": year, "limit": limit}
        
        # 캐시 조회
        cached_data = await cache_manager.get("efficiency", cache_params, run_id)
        
        if cached_data:
            # ETag 처리
            etag = cache_manager.generate_etag(cached_data, run_id)
            
            if if_none_match and if_none_match == etag:
                return Response(status_code=status.HTTP_304_NOT_MODIFIED)
            
            response.headers["ETag"] = etag
            response.headers["Cache-Control"] = "public, max-age=300"
            
            return [EfficiencyAnalysis(**item) for item in cached_data]
        
        # 데이터 조회
        analyses = await service.get_efficiency_by_sport(year, limit)
        
        # 캐시용 데이터 변환
        cache_data = [analysis.model_dump() for analysis in analyses]
        
        # 캐시 저장
        await cache_manager.set(
            "efficiency",
            cache_data,
            cache_params,
            run_id,
            ttl=300
        )
        
        # ETag 생성
        etag = cache_manager.generate_etag(cache_data, run_id)
        response.headers["ETag"] = etag
        response.headers["Cache-Control"] = "public, max-age=300"
        
        return analyses
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"효율성 분석 조회 실패: {e}")
        raise HTTPException(status_code=500, detail="내부 서버 오류")


@router.get("/roi", response_model=List[ROIAnalysis])
async def get_roi_analysis(
    response: Response,
    year: int = Query(..., ge=2020, le=2030),
    limit: int = Query(10, ge=1, le=100),
    if_none_match: Optional[str] = Header(None),
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_active_user)
) -> List[ROIAnalysis]:
    """ROI 분석"""
    service = BudgetAnalysisService(db)
    
    try:
        # 최신 run_id 조회
        run_id = await service.get_latest_run_id()
        
        # 캐시 파라미터
        cache_params = {"year": year, "limit": limit}
        
        # 캐시 조회
        cached_data = await cache_manager.get("roi", cache_params, run_id)
        
        if cached_data:
            # ETag 처리
            etag = cache_manager.generate_etag(cached_data, run_id)
            
            if if_none_match and if_none_match == etag:
                return Response(status_code=status.HTTP_304_NOT_MODIFIED)
            
            response.headers["ETag"] = etag
            response.headers["Cache-Control"] = "public, max-age=300"
            
            return [ROIAnalysis(**item) for item in cached_data]
        
        # 데이터 조회
        analyses = await service.get_roi_analysis(year, limit)
        
        # 캐시용 데이터 변환
        cache_data = [analysis.model_dump() for analysis in analyses]
        
        # 캐시 저장
        await cache_manager.set(
            "roi",
            cache_data,
            cache_params,
            run_id,
            ttl=300
        )
        
        # ETag 생성
        etag = cache_manager.generate_etag(cache_data, run_id)
        response.headers["ETag"] = etag
        response.headers["Cache-Control"] = "public, max-age=300"
        
        return analyses
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"ROI 분석 조회 실패: {e}")
        raise HTTPException(status_code=500, detail="내부 서버 오류")


@router.get("/comparison", response_model=List[RegionComparison])
async def get_regional_comparison(
    response: Response,
    year: int = Query(..., ge=2020, le=2030),
    if_none_match: Optional[str] = Header(None),
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_active_user)
) -> List[RegionComparison]:
    """지역별 비교 분석"""
    service = BudgetAnalysisService(db)
    
    try:
        # 최신 run_id 조회
        run_id = await service.get_latest_run_id()
        
        # 캐시 파라미터
        cache_params = {"year": year}
        
        # 캐시 조회
        cached_data = await cache_manager.get("comparison", cache_params, run_id)
        
        if cached_data:
            # ETag 처리
            etag = cache_manager.generate_etag(cached_data, run_id)
            
            if if_none_match and if_none_match == etag:
                return Response(status_code=status.HTTP_304_NOT_MODIFIED)
            
            response.headers["ETag"] = etag
            response.headers["Cache-Control"] = "public, max-age=300"
            
            return [RegionComparison(**item) for item in cached_data]
        
        # 데이터 조회
        comparisons = await service.get_regional_comparison(year)
        
        # 캐시용 데이터 변환
        cache_data = [comp.model_dump() for comp in comparisons]
        
        # 캐시 저장
        await cache_manager.set(
            "comparison",
            cache_data,
            cache_params,
            run_id,
            ttl=300
        )
        
        # ETag 생성
        etag = cache_manager.generate_etag(cache_data, run_id)
        response.headers["ETag"] = etag
        response.headers["Cache-Control"] = "public, max-age=300"
        
        return comparisons
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"지역별 비교 조회 실패: {e}")
        raise HTTPException(status_code=500, detail="내부 서버 오류")


@router.get("/trend", response_model=List[TrendData])
async def get_trend_analysis(
    response: Response,
    start_year: int = Query(..., ge=2020, le=2030),
    end_year: int = Query(..., ge=2020, le=2030),
    sport_id: Optional[int] = Query(None),
    region_code: Optional[str] = Query(None),
    if_none_match: Optional[str] = Header(None),
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_active_user)
) -> List[TrendData]:
    """트렌드 분석"""
    if start_year > end_year:
        raise HTTPException(
            status_code=400,
            detail="시작 연도가 종료 연도보다 클 수 없습니다"
        )
    
    service = BudgetAnalysisService(db)
    
    try:
        # 최신 run_id 조회
        run_id = await service.get_latest_run_id()
        
        # 캐시 파라미터
        cache_params = {
            "start_year": start_year,
            "end_year": end_year,
            "sport_id": sport_id,
            "region_code": region_code
        }
        
        # 캐시 조회
        cached_data = await cache_manager.get("trend", cache_params, run_id)
        
        if cached_data:
            # ETag 처리
            etag = cache_manager.generate_etag(cached_data, run_id)
            
            if if_none_match and if_none_match == etag:
                return Response(status_code=status.HTTP_304_NOT_MODIFIED)
            
            response.headers["ETag"] = etag
            response.headers["Cache-Control"] = "public, max-age=300"
            
            return [TrendData(**item) for item in cached_data]
        
        # 데이터 조회
        trends = await service.get_trend_data(
            start_year, end_year, sport_id, region_code
        )
        
        # 캐시용 데이터 변환
        cache_data = [trend.model_dump() for trend in trends]
        
        # 캐시 저장
        await cache_manager.set(
            "trend",
            cache_data,
            cache_params,
            run_id,
            ttl=300
        )
        
        # ETag 생성
        etag = cache_manager.generate_etag(cache_data, run_id)
        response.headers["ETag"] = etag
        response.headers["Cache-Control"] = "public, max-age=300"
        
        return trends
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"트렌드 분석 조회 실패: {e}")
        raise HTTPException(status_code=500, detail="내부 서버 오류")


@router.post("/export", response_model=Dict[str, str])
async def export_data(
    request: ExportRequest,
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_active_user)
) -> Dict[str, str]:
    """
    데이터 내보내기
    
    지원 형식:
    - CSV
    - XLSX
    - JSON
    """
    # TODO: 실제 내보내기 구현
    # 1. 백그라운드 작업으로 처리
    # 2. 파일 생성
    # 3. 다운로드 URL 반환
    
    return {
        "status": "processing",
        "message": "내보내기 작업이 시작되었습니다",
        "task_id": "export_12345"
    }


@router.post("/cache/invalidate", response_model=Dict[str, Any])
async def invalidate_cache(
    run_id: Optional[int] = Query(None),
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(get_current_active_user)
) -> Dict[str, Any]:
    """
    캐시 무효화 (관리자 전용)
    
    - run_id 지정 시: 해당 run_id의 캐시만 삭제
    - run_id 미지정 시: 모든 캐시 삭제
    """
    # 관리자 권한 체크
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="관리자 권한이 필요합니다"
        )
    
    try:
        if run_id:
            # 특정 run_id 캐시 무효화
            deleted = await cache_manager.invalidate_run(run_id)
            message = f"Run ID {run_id}의 캐시 {deleted}개 삭제"
        else:
            # 모든 캐시 삭제
            deleted = await cache_manager.delete_pattern("bp:*")
            message = f"전체 캐시 {deleted}개 삭제"
        
        return {
            "status": "success",
            "message": message,
            "deleted_count": deleted
        }
        
    except Exception as e:
        logger.error(f"캐시 무효화 실패: {e}")
        raise HTTPException(status_code=500, detail="캐시 무효화 실패")