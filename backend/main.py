from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import uvicorn

from app.api.v1.api import api_router
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Starting up Sports Data Lab API...")
    yield
    # Shutdown
    print("🛑 Shutting down Sports Data Lab API...")


def create_application():
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description="스포츠 데이터랩: 시민을 위한 체육 정책 대시보드 API",
        version=settings.PROJECT_VERSION,
        openapi_url=f"{settings.API_V1_STR}/openapi.json" if settings.BACKEND_CORS_ORIGINS else None,
        lifespan=lifespan,
    )

    # Set all CORS enabled origins
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router, prefix=settings.API_V1_STR)

    return app


app = create_application()


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )