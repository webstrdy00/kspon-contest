from fastapi import APIRouter

from app.api.v1.endpoints import (
    facilities, reports, proposals, dashboard, auth, 
    data_import, scheduler, csv_upload
)


api_router = APIRouter()

# Authentication endpoints
api_router.include_router(
    auth.router, prefix="/auth", tags=["authentication"]
)

# Dashboard endpoints
api_router.include_router(
    dashboard.router, prefix="/dashboard", tags=["dashboard"]
)

# Sports facilities endpoints
api_router.include_router(
    facilities.router, prefix="/facilities", tags=["facilities"]
)

# Regional reports endpoints
api_router.include_router(
    reports.router, prefix="/reports", tags=["reports"]
)

# Policy proposals endpoints
api_router.include_router(
    proposals.router, prefix="/proposals", tags=["proposals"]
)

# Data import endpoints
api_router.include_router(
    data_import.router, prefix="/data", tags=["data-import"]
)

# Scheduler endpoints
api_router.include_router(
    scheduler.router, prefix="/scheduler", tags=["scheduler"]
)

# CSV upload endpoints
api_router.include_router(
    csv_upload.router, prefix="/csv", tags=["csv-upload"]
)


@api_router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "스포츠 데이터랩 API 서버가 정상 작동 중입니다."}