from datetime import datetime, timedelta, timezone
from typing import Optional, Union, Any
from jose import JWTError, jwt
from passlib.context import CryptContext

from .config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """평문 비밀번호와 해시된 비밀번호를 비교하여 검증"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """비밀번호를 해시화"""
    return pwd_context.hash(password)


def create_access_token(
    subject: Union[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """JWT 액세스 토큰 생성"""
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def create_refresh_token(
    subject: Union[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """JWT 리프레시 토큰 생성"""
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # 리프레시 토큰은 기본적으로 7일간 유효
        expire = datetime.now(timezone.utc) + timedelta(days=7)
    
    to_encode = {"exp": expire, "sub": str(subject), "type": "refresh"}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_token(token: str, token_type: str = "access") -> Optional[str]:
    """JWT 토큰을 검증하고 subject 반환"""
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_subject: str = payload.get("sub")
        token_type_in_payload: str = payload.get("type", "access")
        
        if token_subject is None:
            return None
        
        # 토큰 타입 확인 (refresh token인지 access token인지)
        if token_type == "refresh" and token_type_in_payload != "refresh":
            return None
            
        return token_subject
    except JWTError:
        return None


def verify_refresh_token(token: str) -> Optional[str]:
    """리프레시 토큰을 검증하고 subject 반환"""
    return verify_token(token, token_type="refresh")