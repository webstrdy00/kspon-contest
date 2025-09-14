from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
import uvicorn

from app.api.v1.api import api_router
from app.core.config import settings
from app.tasks.scheduler import scheduler

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        # 필요시 파일 핸들러 추가 가능
        # logging.FileHandler('app.log')
    ]
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("🚀 Starting up Sports Data Lab API...")
    
    # 스케줄러 자동 시작 (환경변수로 제어)
    if getattr(settings, 'AUTO_START_SCHEDULER', False):
        try:
            scheduler.start()
            logger.info("📅 Data collection scheduler started")
        except Exception as e:
            logger.error(f"Failed to start scheduler: {e}")
    
    yield
    
    # Shutdown
    if scheduler.is_running:
        try:
            scheduler.stop()
            logger.info("📅 Data collection scheduler stopped")
        except Exception as e:
            logger.error(f"Error stopping scheduler: {e}")
        
    logger.info("🛑 Shutting down Sports Data Lab API...")


def create_application():
    logger.info(f"Creating FastAPI application: {settings.PROJECT_NAME} v{settings.PROJECT_VERSION}")
    
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description="스포츠 데이터랩: 시민을 위한 체육 정책 대시보드 API",
        version=settings.PROJECT_VERSION,
        openapi_url=f"{settings.API_V1_STR}/openapi.json" if settings.BACKEND_CORS_ORIGINS else None,
        lifespan=lifespan,
    )

    # Set all CORS enabled origins
    logger.info(f"Setting up CORS for origins: {settings.BACKEND_CORS_ORIGINS}")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    logger.info(f"Including API router with prefix: {settings.API_V1_STR}")
    app.include_router(api_router, prefix=settings.API_V1_STR)

    return app


app = create_application()


if __name__ == "__main__":
    logger.info("Starting Uvicorn server...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )