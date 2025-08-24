from fastapi import APIRouter

from app.api.v1.endpoints import facilities, reports, proposals, dashboard


api_router = APIRouter()

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


@api_router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "스포츠 데이터랩 API 서버가 정상 작동 중입니다."}