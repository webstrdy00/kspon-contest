from typing import Optional
from pydantic import BaseModel


class Token(BaseModel):
    """액세스 토큰 응답"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """토큰 데이터"""
    username: Optional[str] = None