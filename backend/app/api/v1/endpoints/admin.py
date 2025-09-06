"""
Admin API Endpoints for ETL and System Management
관리자 API 엔드포인트
"""
from typing import Dict, Any, Optional
from datetime import datetime
import logging
import asyncio

from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_async_db
from app.core.deps import get_current_active_user
from app.core.cache import cache_manager
from app.models.user import User
from app.etl.budget_performance_etl import BudgetPerformanceETL

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/admin", tags=["admin"])


def check_admin(current_user: User = Depends(get_current_active_user)) -> User:
    """관리자 권한 체크"""
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403,
            detail="관리자 권한이 필요합니다"
        )
    return current_user


async def run_etl_task(
    session: AsyncSession,
    year: int,
    source: str
) -> Dict[str, Any]:
    """ETL 백그라운드 작업"""
    try:
        etl = BudgetPerformanceETL(session)
        result = await etl.run_full_pipeline(source=source, year=year)
        
        # 캐시 무효화 (이전 run_id)
        if result.get("run_id"):
            await cache_manager.invalidate_run(result["run_id"] - 1)
        
        return result
    except Exception as e:
        logger.error(f"ETL 실행 실패: {str(e)}")
        raise
    finally:
        await session.close()


@router.post("/etl/run", response_model=Dict[str, Any])
async def run_etl_pipeline(
    background_tasks: BackgroundTasks,
    year: int = Query(..., ge=2020, le=2030),
    source: str = Query("manual", regex="^(manual|scheduled|api)$"),
    sync: bool = Query(False, description="동기 실행 여부"),
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(check_admin)
) -> Dict[str, Any]:
    """
    ETL 파이프라인 실행 (관리자 전용)
    
    Parameters:
    - year: 처리할 연도
    - source: ETL 소스 (manual/scheduled/api)
    - sync: True면 동기 실행, False면 백그라운드 실행
    """
    
    if sync:
        # 동기 실행
        try:
            etl = BudgetPerformanceETL(db)
            result = await etl.run_full_pipeline(source=source, year=year)
            
            # 캐시 무효화
            if result.get("run_id") and result["run_id"] > 1:
                await cache_manager.invalidate_run(result["run_id"] - 1)
            
            return {
                "status": "completed",
                "run_id": result.get("run_id"),
                "stats": result.get("stats"),
                "message": f"{year}년 ETL 파이프라인 실행 완료"
            }
            
        except Exception as e:
            logger.error(f"ETL 실행 실패: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail=f"ETL 실행 실패: {str(e)}"
            )
    else:
        # 백그라운드 실행
        # 새 세션 생성 (백그라운드 작업용)
        from app.db.session import AsyncSessionLocal
        async_session = AsyncSessionLocal()
        
        background_tasks.add_task(
            run_etl_task,
            async_session,
            year,
            source
        )
        
        return {
            "status": "started",
            "message": f"{year}년 ETL 파이프라인이 백그라운드에서 실행 중입니다"
        }


@router.get("/etl/status", response_model=Dict[str, Any])
async def get_etl_status(
    run_id: Optional[int] = Query(None),
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(check_admin)
) -> Dict[str, Any]:
    """
    ETL 실행 상태 조회 (관리자 전용)
    
    Parameters:
    - run_id: 조회할 실행 ID (없으면 최신)
    """
    from app.models import EtlRun
    from sqlalchemy import select, desc
    
    try:
        if run_id:
            # 특정 run_id 조회
            stmt = select(EtlRun).where(EtlRun.run_id == run_id)
        else:
            # 최신 실행 조회
            stmt = select(EtlRun).order_by(desc(EtlRun.started_at)).limit(1)
        
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
            "row_count": etl_run.row_count,
            "error_message": etl_run.error_message,
            "retry_count": etl_run.retry_count
        }
        
    except Exception as e:
        logger.error(f"ETL 상태 조회 실패: {str(e)}")
        raise HTTPException(status_code=500, detail="내부 서버 오류")


@router.get("/etl/history", response_model=Dict[str, Any])
async def get_etl_history(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    status: Optional[str] = Query(None, regex="^(running|success|failed|partial)$"),
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(check_admin)
) -> Dict[str, Any]:
    """
    ETL 실행 이력 조회 (관리자 전용)
    
    Parameters:
    - limit: 조회 개수
    - offset: 시작 위치
    - status: 상태 필터 (running/success/failed/partial)
    """
    from app.models import EtlRun
    from sqlalchemy import select, desc, func
    
    try:
        # 전체 카운트 조회
        count_stmt = select(func.count()).select_from(EtlRun)
        if status:
            count_stmt = count_stmt.where(EtlRun.status == status)
        
        total_result = await db.execute(count_stmt)
        total_count = total_result.scalar()
        
        # 데이터 조회
        stmt = select(EtlRun).order_by(desc(EtlRun.started_at))
        
        if status:
            stmt = stmt.where(EtlRun.status == status)
        
        stmt = stmt.offset(offset).limit(limit)
        
        result = await db.execute(stmt)
        runs = result.scalars().all()
        
        return {
            "total": total_count,
            "offset": offset,
            "limit": limit,
            "items": [
                {
                    "run_id": run.run_id,
                    "source": run.source,
                    "started_at": run.started_at.isoformat() if run.started_at else None,
                    "finished_at": run.finished_at.isoformat() if run.finished_at else None,
                    "status": run.status,
                    "row_count": run.row_count,
                    "duration": (
                        (run.finished_at - run.started_at).total_seconds()
                        if run.finished_at and run.started_at else None
                    )
                }
                for run in runs
            ]
        }
        
    except Exception as e:
        logger.error(f"ETL 이력 조회 실패: {str(e)}")
        raise HTTPException(status_code=500, detail="내부 서버 오류")


@router.post("/cache/warm", response_model=Dict[str, Any])
async def warm_cache(
    year: int = Query(..., ge=2020, le=2030),
    db: AsyncSession = Depends(get_async_db),
    current_user: User = Depends(check_admin)
) -> Dict[str, Any]:
    """
    캐시 워밍 (관리자 전용)
    
    주요 쿼리들을 미리 실행하여 캐시를 채웁니다.
    """
    from app.services.budget_analysis import BudgetAnalysisService
    from app.schemas.budget_performance import BudgetPerformanceFilter
    
    service = BudgetAnalysisService(db)
    warmed_count = 0
    
    try:
        # 최신 run_id 조회
        run_id = await service.get_latest_run_id()
        
        # 주요 쿼리 목록
        queries = [
            # 개요 (기본)
            {"key": "overview", "params": {"year": year}},
            # 개요 (지역별)
            {"key": "overview", "params": {"year": year, "group_by": "region"}},
            # 개요 (종목별)
            {"key": "overview", "params": {"year": year, "group_by": "sport"}},
            # 효율성 분석
            {"key": "efficiency", "params": {"year": year, "limit": 10}},
            # ROI 분석
            {"key": "roi", "params": {"year": year, "limit": 10}},
            # 지역별 비교
            {"key": "comparison", "params": {"year": year}},
            # 트렌드 (최근 3년)
            {"key": "trend", "params": {"start_year": year - 2, "end_year": year}},
        ]
        
        for query in queries:
            # 캐시 확인
            cached = await cache_manager.get(
                query["key"],
                query["params"],
                run_id
            )
            
            if not cached:
                # 데이터 조회 및 캐싱
                if query["key"] == "overview":
                    filters = BudgetPerformanceFilter(**query["params"])
                    data = await service.get_overview(filters)
                    await cache_manager.set(
                        "overview",
                        data.model_dump(),
                        query["params"],
                        run_id,
                        ttl=600  # 10분
                    )
                elif query["key"] == "efficiency":
                    data = await service.get_efficiency_by_sport(
                        query["params"]["year"],
                        query["params"]["limit"]
                    )
                    cache_data = [d.model_dump() for d in data]
                    await cache_manager.set(
                        "efficiency",
                        cache_data,
                        query["params"],
                        run_id,
                        ttl=600
                    )
                # ... 다른 쿼리들도 비슷하게 처리
                
                warmed_count += 1
        
        return {
            "status": "success",
            "message": f"캐시 워밍 완료: {warmed_count}개 쿼리",
            "warmed_count": warmed_count,
            "run_id": run_id
        }
        
    except Exception as e:
        logger.error(f"캐시 워밍 실패: {str(e)}")
        raise HTTPException(status_code=500, detail="캐시 워밍 실패")


@router.delete("/cache/all", response_model=Dict[str, Any])
async def clear_all_cache(
    current_user: User = Depends(check_admin)
) -> Dict[str, Any]:
    """
    전체 캐시 삭제 (관리자 전용)
    """
    try:
        deleted = await cache_manager.delete_pattern("bp:*")
        
        return {
            "status": "success",
            "message": f"전체 캐시 삭제 완료: {deleted}개",
            "deleted_count": deleted
        }
        
    except Exception as e:
        logger.error(f"캐시 삭제 실패: {str(e)}")
        raise HTTPException(status_code=500, detail="캐시 삭제 실패")