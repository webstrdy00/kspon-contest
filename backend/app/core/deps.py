from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.db.database import SessionLocal
from app.core.security import verify_token
from app.crud.user import user as user_crud
from app.models.user import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"api/v1/auth/login")


def get_db() -> Generator:
    """데이터베이스 세션 의존성"""
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    """현재 사용자 가져오기"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="인증 정보를 확인할 수 없습니다",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # 토큰 검증
    token_data = verify_token(token)
    if token_data is None:
        raise credentials_exception
    
    # 사용자 조회
    user = user_crud.get_by_email(db, email=token_data)
    if user is None:
        raise credentials_exception
    
    return user


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """현재 활성 사용자 가져오기"""
    if not user_crud.is_active(current_user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="비활성화된 사용자입니다"
        )
    return current_user