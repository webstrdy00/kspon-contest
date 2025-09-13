"""
pytest 설정 파일
테스트용 데이터베이스 세션 및 공통 fixture 정의
"""
import asyncio
import pytest
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool
import os
from pathlib import Path
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env.sample")
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///:memory:")

# 테스트 환경 설정
os.environ["TESTING"] = "1"

from app.core.config import settings
from app.models.base import Base
from app.core.database import get_db


# 테스트용 데이터베이스 URL
TEST_DATABASE_URL = str(settings.DATABASE_URL).replace("/kspon", "/kspon_test") if settings.DATABASE_URL else "sqlite+aiosqlite:///:memory:"


@pytest.fixture(scope="session")
def event_loop():
    """이벤트 루프 fixture"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def test_engine():
    """테스트용 데이터베이스 엔진"""
    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
        poolclass=NullPool,
    )
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    await engine.dispose()


@pytest.fixture(scope="function")
async def db_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """테스트용 데이터베이스 세션"""
    async_session = async_sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    
    async with async_session() as session:
        yield session
        await session.rollback()


@pytest.fixture(scope="function")
async def client(db_session):
    """FastAPI 테스트 클라이언트"""
    from httpx import AsyncClient
    from main import app
    
    async def override_get_db():
        yield db_session
    
    app.dependency_overrides[get_db] = override_get_db
    
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    
    app.dependency_overrides.clear()


@pytest.fixture
def mock_facility_data():
    """시설 테스트 데이터"""
    return {
        'faci_nm': '테스트 수영장',
        'fcob_nm': '수영장',
        'ftype_nm': '실내수영장',
        'fmng_cp_nm': '서울특별시',
        'faci_road_addr1': '서울특별시 강남구 테헤란로 123',
        'faci_point_x': '127.0276',
        'faci_point_y': '37.4979',
        'tel_no': '02-555-1234',
        'homepage_url': 'http://test-pool.com',
        'ar_totl_ar': '2000',
        'faciStat_nm': '운영중'
    }


@pytest.fixture
def mock_performance_data():
    """성과금 테스트 데이터"""
    return {
        'pmt_yymm': '202501',
        'spm_nm': '수영',
        'mmamt': '10000000',
        'rcptn_nm': '홍길동',
        'row_num': '1'
    }


@pytest.fixture
def mock_fund_data():
    """기금 테스트 데이터"""
    return {
        'year': '2025',
        'bsnsyear': '2025',
        'sbsidy_se': '보조금',
        'bsns_nm': '생활체육 활성화 사업',
        'excn_amt': '5000000000',
        'intrlck_nm': '서울특별시',
        'remark': '생활체육 지원'
    }


@pytest.fixture
def auth_headers():
    """인증 헤더"""
    # 테스트용 JWT 토큰 생성
    from app.core.security import create_access_token
    
    access_token = create_access_token(
        data={"sub": "test@example.com"}
    )
    
    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture
async def test_user(db_session):
    """테스트 사용자"""
    from app.models.user import User
    from app.core.security import get_password_hash
    
    user = User(
        email="test@example.com",
        hashed_password=get_password_hash("testpassword"),
        username="testuser",
        is_active=True,
        is_verified=True
    )
    
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    
    return user


@pytest.fixture
async def admin_user(db_session):
    """관리자 사용자"""
    from app.models.user import User
    from app.core.security import get_password_hash
    
    admin = User(
        email="admin@example.com",
        hashed_password=get_password_hash("adminpassword"),
        username="admin",
        is_active=True,
        is_verified=True,
        role="admin"
    )
    
    db_session.add(admin)
    await db_session.commit()
    await db_session.refresh(admin)
    
    return admin