from typing import List, Union, Optional
from pydantic import AnyHttpUrl, BaseSettings, validator
from pydantic_settings import BaseSettings
import secrets


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    PROJECT_NAME: str = "스포츠 데이터랩 API"
    PROJECT_VERSION: str = "1.0.0"
    
    # JWT Authentication
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost:3000",  # Next.js dev server
        "http://localhost:8000",  # FastAPI dev server
    ]

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Database
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "sports_data_lab"
    POSTGRES_PASSWORD: str = "sports_data_lab"
    POSTGRES_DB: str = "sports_data_lab"
    DATABASE_URL: Optional[str] = None

    @validator("DATABASE_URL", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: dict) -> str:
        if isinstance(v, str):
            return v
        return f"postgresql://{values.get('POSTGRES_USER')}:{values.get('POSTGRES_PASSWORD')}@{values.get('POSTGRES_SERVER')}/{values.get('POSTGRES_DB')}"

    # External APIs - 공공데이터포털
    DATA_GO_KR_API_KEY: Optional[str] = None
    
    # API Base URLs
    DATA_GO_KR_BASE_URL: str = "http://apis.data.go.kr"
    
    # 전국공공체육시설 API
    FACILITIES_API_URL: str = "http://apis.data.go.kr/B554287/PublicSportsFacilitiesService"
    
    # 국민체육진흥기금 API URLs
    FUND_SUPPORT_API_URL: str = "http://apis.data.go.kr/B551014/SRVC_API_SPRT_FUND"
    FUND_BUSINESS_API_URL: str = "http://apis.data.go.kr/B551014/SRVC_API_SPRT_BIZ"
    
    # 체육인복지 경기력향상성과금 API
    PERFORMANCE_REWARD_API_URL: str = "http://apis.data.go.kr/B551014/SRVC_API_ATHLT_WLFARE"
    
    # API 설정
    API_TIMEOUT: int = 30
    API_MAX_RETRIES: int = 3
    API_PAGE_SIZE: int = 100

    # Cache
    REDIS_URL: Optional[str] = None
    
    # Scheduler
    AUTO_START_SCHEDULER: bool = False  # 서버 시작 시 스케줄러 자동 시작 여부

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()