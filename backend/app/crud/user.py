from typing import Optional
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password


class CRUDUser:
    """사용자 CRUD 작업"""
    
    def get_by_id(self, db: Session, user_id: int) -> Optional[User]:
        """ID로 사용자 조회"""
        return db.query(User).filter(User.id == user_id).first()
    
    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        """이메일로 사용자 조회"""
        return db.query(User).filter(User.email == email).first()
    
    def get_by_username(self, db: Session, username: str) -> Optional[User]:
        """사용자명으로 사용자 조회"""
        return db.query(User).filter(User.username == username).first()
    
    def create(self, db: Session, user_create: UserCreate) -> User:
        """새 사용자 생성"""
        hashed_password = get_password_hash(user_create.password)
        
        db_user = User(
            email=user_create.email,
            username=user_create.username,
            hashed_password=hashed_password,
            display_name=user_create.display_name,
            bio=user_create.bio,
            region_code=user_create.region_code,
            interested_regions=user_create.interested_regions,
            interested_sports=user_create.interested_sports,
            interested_facility_types=user_create.interested_facility_types,
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    def update(self, db: Session, user_id: int, user_update: UserUpdate) -> Optional[User]:
        """사용자 정보 수정"""
        db_user = self.get_by_id(db, user_id)
        if not db_user:
            return None
        
        update_data = user_update.dict(exclude_unset=True)
        
        # 비밀번호가 포함된 경우 해싱
        if "password" in update_data:
            hashed_password = get_password_hash(update_data.pop("password"))
            update_data["hashed_password"] = hashed_password
        
        for field, value in update_data.items():
            setattr(db_user, field, value)
        
        db.commit()
        db.refresh(db_user)
        return db_user
    
    def authenticate(self, db: Session, email: str, password: str) -> Optional[User]:
        """사용자 인증"""
        user = self.get_by_email(db, email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
    
    def is_active(self, user: User) -> bool:
        """사용자 활성 상태 확인"""
        return user.is_active
    
    def is_verified(self, user: User) -> bool:
        """사용자 인증 상태 확인"""
        return user.is_verified


user = CRUDUser()