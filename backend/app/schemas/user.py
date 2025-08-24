from typing import Optional, List
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """사용자 기본 스키마"""
    email: EmailStr
    username: str
    display_name: str
    is_active: bool = True
    is_verified: bool = False


class UserCreate(BaseModel):
    """사용자 생성 스키마"""
    email: EmailStr
    username: str
    password: str
    display_name: str
    bio: Optional[str] = None
    region_code: Optional[str] = None
    interested_regions: Optional[List[str]] = None
    interested_sports: Optional[List[str]] = None
    interested_facility_types: Optional[List[str]] = None


class UserUpdate(BaseModel):
    """사용자 수정 스키마"""
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None
    display_name: Optional[str] = None
    bio: Optional[str] = None
    region_code: Optional[str] = None
    interested_regions: Optional[List[str]] = None
    interested_sports: Optional[List[str]] = None
    interested_facility_types: Optional[List[str]] = None
    is_active: Optional[bool] = None


class User(UserBase):
    """사용자 조회 스키마"""
    id: int
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    region_code: Optional[str] = None
    interested_regions: Optional[List[str]] = None
    interested_sports: Optional[List[str]] = None
    interested_facility_types: Optional[List[str]] = None
    proposal_count: int = 0
    vote_count: int = 0
    like_received: int = 0
    report_count: int = 0
    
    class Config:
        from_attributes = True


class UserInDB(User):
    """데이터베이스용 사용자 스키마"""
    hashed_password: str