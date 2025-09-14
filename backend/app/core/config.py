from typing import List, Union, Optional
from pydantic import field_validator, PostgresDsn, Field
from pydantic_settings import BaseSettings
import secrets


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = Field(default_factory=lambda: secrets.token_urlsafe(32))
    PROJECT_NAME: str = "스포츠 데이터랩 API"
    PROJECT_VERSION: str = "1.0.0"
    
    # JWT Authentication
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30  

    # CORS 
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Database
    POSTGRES_SERVER: Optional[str] = None
    POSTGRES_USER: Optional[str] = None
    POSTGRES_PASSWORD: Optional[str] = None
    POSTGRES_DB: Optional[str] = None
    DATABASE_URL: Optional[PostgresDsn] = None

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], info) -> str:
        if v:
            return v
        data = info.data
        required = ["POSTGRES_SERVER", "POSTGRES_USER", "POSTGRES_PASSWORD", "POSTGRES_DB"]
        missing = [name for name in required if not data.get(name)]
        if missing:
            missing_vars = ", ".join(missing)
            raise ValueError(
                f"Missing environment variables for database configuration: {missing_vars}"
            )
        return PostgresDsn.build(
            scheme="postgresql",
            username=data["POSTGRES_USER"],
            password=data["POSTGRES_PASSWORD"],
            host=data["POSTGRES_SERVER"],
            path=f"/{data['POSTGRES_DB']}",
        )

    # External APIs - 공공데이터포털
    DATA_GO_KR_API_KEY: Optional[str] = None
    
    # API Base URLs -
    DATA_GO_KR_BASE_URL: Optional[str] = None
    
    # 전국공공체육시설 API
    FACILITIES_API_URL: str = "http://apis.data.go.kr/B554287/PublicSportsFacilitiesService"
    
    # 국민체육진흥기금 API URLs
    FUND_SUPPORT_API_URL: str = "https://apis.data.go.kr/B551014/SRVC_OD_API_FUN_OBJ_ORG_API"
    FUND_BUSINESS_API_URL: Optional[str] = None
    FUND_EVALUATION_API_URL: Optional[str] = None  # 기금지원사업평가 API
    FUND_COMPREHENSIVE_API_URL: Optional[str] = None  # 종합지원실적지표 API
    
    # 체육인복지 경기력향상성과금 API
    PERFORMANCE_REWARD_API_URL: str = "https://apis.data.go.kr/B551014/SRVC_TODZ_USFUN_PIRPEN_NON_DSPSN"
    
    # API 설정
    API_TIMEOUT: int = 30
    API_MAX_RETRIES: int = 3
    API_PAGE_SIZE: int = 100

    # Cache
    REDIS_URL: Optional[str] = None
    
    # Scheduler
    AUTO_START_SCHEDULER: bool = False  

    model_config = {
        "case_sensitive": True,
        "env_file": ".env"
    }


settings = Settings()