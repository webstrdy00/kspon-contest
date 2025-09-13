from typing import Optional
from pydantic import BaseModel


class Token(BaseModel):
    """액세스 토큰 응답"""
    access_token: str
    token_type: str = "bearer"
    refresh_token: Optional[str] = None


class TokenData(BaseModel):
    """토큰 데이터"""
    username: Optional[str] = None


class RefreshTokenRequest(BaseModel):
    """리프레시 토큰 요청"""
    refresh_token: str