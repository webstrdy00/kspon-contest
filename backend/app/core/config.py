from typing import List, Union, Optional
from pydantic import field_validator
from pydantic_settings import BaseSettings
import secrets


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str  
    PROJECT_NAME: str = "스포츠 데이터랩 API"
    PROJECT_VERSION: str = "1.0.0"
    
    # JWT Authentication
    ALGORITHM: str 
    ACCESS_TOKEN_EXPIRE_MINUTES: int  

    # CORS 
    BACKEND_CORS_ORIGINS: List[str]

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # Database
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DATABASE_URL: Optional[str] = None

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], values: dict) -> str:
        if isinstance(v, str):
            return v
        return f"postgresql://{values.data.get('POSTGRES_USER')}:{values.data.get('POSTGRES_PASSWORD')}@{values.data.get('POSTGRES_SERVER')}/{values.data.get('POSTGRES_DB')}"

    # External APIs - 공공데이터포털
    DATA_GO_KR_API_KEY: Optional[str] = None
    
    # API Base URLs -
    DATA_GO_KR_BASE_URL: Optional[str] = None
    
    # 전국공공체육시설 API
    FACILITIES_API_URL: str
    
    # 국민체육진흥기금 API URLs
    FUND_SUPPORT_API_URL: str
    FUND_BUSINESS_API_URL: Optional[str] = None
    
    # 체육인복지 경기력향상성과금 API
    PERFORMANCE_REWARD_API_URL: str
    
    # API 설정
    API_TIMEOUT: int
    API_MAX_RETRIES: int
    API_PAGE_SIZE: int

    # Cache
    REDIS_URL: Optional[str] = None
    
    # Scheduler
    AUTO_START_SCHEDULER: bool  

    model_config = {
        "case_sensitive": True,
        "env_file": ".env"
    }


settings = Settings()