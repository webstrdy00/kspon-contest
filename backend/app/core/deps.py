from collections.abc import AsyncGenerator
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import verify_token
from app.crud.user import user as user_crud
from app.models.user import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")
oauth2_scheme_optional = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login", auto_error=False)


async def get_current_user(
    db: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme),
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
    user = await user_crud.get_by_email(db, email=token_data)
    if user is None:
        raise credentials_exception
    
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """현재 활성 사용자 가져오기"""
    if not user_crud.is_active(current_user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="비활성화된 사용자입니다",
        )
    return current_user


async def get_current_user_optional(
    db: AsyncSession = Depends(get_db),
    token: Optional[str] = Depends(oauth2_scheme_optional),
) -> Optional[User]:
    """현재 사용자 가져오기 (선택적 - 인증 없어도 됨)"""
    if not token:
        return None
    
    try:
        # 토큰 검증
        token_data = verify_token(token)
        if token_data is None:
            return None
        
        # 사용자 조회
        user = await user_crud.get_by_email(db, email=token_data)
        return user
    except Exception:
        return None