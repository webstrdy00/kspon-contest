from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.deps import get_db, get_current_active_user
from app.core.security import create_access_token
from app.core.config import settings
from app.crud.user import user as user_crud
from app.schemas.token import Token
from app.schemas.user import User, UserCreate, UserUpdate
from app.models.user import User as UserModel


router = APIRouter()


@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
def register(
    *,
    db: Session = Depends(get_db),
    user_in: UserCreate,
) -> Any:
    """
    새 사용자 회원가입
    """
    # 이메일 중복 확인
    user = user_crud.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 등록된 이메일입니다",
        )
    
    # 사용자명 중복 확인
    user = user_crud.get_by_username(db, username=user_in.username)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 사용 중인 사용자명입니다",
        )
    
    # 사용자 생성
    user = user_crud.create(db, user_create=user_in)
    return user


@router.post("/login", response_model=Token)
def login(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    사용자 로그인 (OAuth2 호환)
    """
    user = user_crud.authenticate(
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
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.email, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.get("/me", response_model=User)
def read_user_me(
    current_user: UserModel = Depends(get_current_active_user),
) -> Any:
    """
    현재 로그인된 사용자 정보 조회
    """
    return current_user


@router.put("/me", response_model=User)
def update_user_me(
    *,
    db: Session = Depends(get_db),
    user_in: UserUpdate,
    current_user: UserModel = Depends(get_current_active_user),
) -> Any:
    """
    현재 로그인된 사용자 정보 수정
    """
    # 이메일 변경 시 중복 확인
    if user_in.email and user_in.email != current_user.email:
        existing_user = user_crud.get_by_email(db, email=user_in.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="이미 등록된 이메일입니다",
            )
    
    # 사용자명 변경 시 중복 확인
    if user_in.username and user_in.username != current_user.username:
        existing_user = user_crud.get_by_username(db, username=user_in.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="이미 사용 중인 사용자명입니다",
            )
    
    user = user_crud.update(db, user_id=current_user.id, user_update=user_in)
    return user


@router.get("/test")
def test_auth(
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