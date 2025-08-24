from typing import List, Union, Optional
from pydantic import AnyHttpUrl, BaseSettings, validator
from pydantic_settings import BaseSettings
import secrets


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    PROJECT_NAME: str = "스포츠 데이터랩 API"
    PROJECT_VERSION: str = "1.0.0"

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

    # External APIs
    DATA_GO_KR_API_KEY: Optional[str] = None
    DATA_GO_KR_BASE_URL: str = "http://apis.data.go.kr/1192000"

    # Cache
    REDIS_URL: Optional[str] = None

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()