from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.deps import get_current_active_user
from app.core.database import get_db
from app.core.security import create_access_token, create_refresh_token, verify_refresh_token
from app.core.config import settings
from app.crud.user import user as user_crud
from app.schemas.token import Token, RefreshTokenRequest
from app.schemas.user import User, UserCreate, UserUpdate
from app.models.user import User as UserModel


router = APIRouter()


@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def register(
    *,
    db: AsyncSession = Depends(get_db),
    user_in: UserCreate,
) -> Any:
    """
    새 사용자 회원가입
    """
    # 이메일 중복 확인
    user = await user_crud.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 등록된 이메일입니다",
        )
    
    # 사용자명 중복 확인
    user = await user_crud.get_by_username(db, username=user_in.username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 사용 중인 사용자명입니다",
        )
    
    # 사용자 생성
    user = await user_crud.create(db, user_create=user_in)
    return user


@router.post("/login", response_model=Token)
async def login(
    db: AsyncSession = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    사용자 로그인 (OAuth2 호환)
    """
    user = await user_crud.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이메일 또는 비밀번호가 올바르지 않습니다",
            headers={"WWW-Authenticate": "Bearer"},
        )
    elif not user_crud.is_active(user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="비활성화된 사용자입니다"
        )
    
    # Access token 생성
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.email, expires_delta=access_token_expires
    )
    
    # Refresh token 생성
    refresh_token_expires = timedelta(days=7)
    refresh_token = create_refresh_token(
        subject=user.email, expires_delta=refresh_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token,
    }


@router.get("/me", response_model=User)
async def read_user_me(
    current_user: UserModel = Depends(get_current_active_user),
) -> Any:
    """
    현재 로그인된 사용자 정보 조회
    """
    return current_user


@router.put("/me", response_model=User)
async def update_user_me(
    *,
    db: AsyncSession = Depends(get_db),
    user_in: UserUpdate,
    current_user: UserModel = Depends(get_current_active_user),
) -> Any:
    """
    현재 로그인된 사용자 정보 수정
    """
    # 이메일 변경 시 중복 확인
    if user_in.email and user_in.email != current_user.email:
        existing_user = await user_crud.get_by_email(db, email=user_in.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="이미 등록된 이메일입니다",
            )
    
    # 사용자명 변경 시 중복 확인
    if user_in.username and user_in.username != current_user.username:
        existing_user = await user_crud.get_by_username(db, username=user_in.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="이미 사용 중인 사용자명입니다",
            )
    
    user = await user_crud.update(db, user_id=current_user.id, user_update=user_in)
    return user


@router.post("/refresh", response_model=Token)
async def refresh_token(
    *,
    db: AsyncSession = Depends(get_db),
    token_request: RefreshTokenRequest,
) -> Any:
    """
    리프레시 토큰으로 새로운 액세스 토큰 발급
    """
    # 리프레시 토큰 검증
    email = verify_refresh_token(token_request.refresh_token)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유효하지 않은 리프레시 토큰입니다",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 사용자 확인
    user = await user_crud.get_by_email(db, email=email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="사용자를 찾을 수 없습니다",
        )
    
    if not user_crud.is_active(user):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="비활성화된 사용자입니다"
        )
    
    # 새로운 액세스 토큰 생성
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.email, expires_delta=access_token_expires
    )
    
    # 새로운 리프레시 토큰도 함께 발급 (선택사항)
    refresh_token_expires = timedelta(days=7)
    new_refresh_token = create_refresh_token(
        subject=user.email, expires_delta=refresh_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": new_refresh_token,
    }


@router.get("/test")
async def test_auth(
    current_user: UserModel = Depends(get_current_active_user),
) -> Any:
    """
    인증 테스트용 엔드포인트
    """
    return {
        "message": "인증 성공!",
        "user": {
            "id": current_user.id,
            "email": current_user.email,
            "username": current_user.username,
            "display_name": current_user.display_name
        }
    }