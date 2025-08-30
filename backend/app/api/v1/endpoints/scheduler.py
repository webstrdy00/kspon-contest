"""
스케줄러 관리 API 엔드포인트
"""
from typing import Dict, Any
from fastapi import APIRouter, HTTPException, Depends
from app.core.deps import get_current_user_optional
from app.tasks.scheduler import scheduler

router = APIRouter()


@router.get("/status")
async def get_scheduler_status() -> Dict[str, Any]:
    """
    스케줄러 상태 조회
    """
    return scheduler.get_job_status()


@router.post("/start")
async def start_scheduler():
    """
    스케줄러 시작
    """
    try:
        scheduler.start()
        return {"status": "started", "message": "스케줄러가 시작되었습니다."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/stop")
async def stop_scheduler():
    """
    스케줄러 중지
    """
    try:
        scheduler.stop()
        return {"status": "stopped", "message": "스케줄러가 중지되었습니다."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/trigger/{job_id}")
async def trigger_job(job_id: str):
    """
    특정 작업 수동 실행
    
    Args:
        job_id: 작업 ID (collect_facilities, collect_fund, collect_performance, update_cache)
    """
    try:
        await scheduler.trigger_job(job_id)
        return {
            "status": "triggered",
            "job_id": job_id,
            "message": f"{job_id} 작업이 실행되었습니다."
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))