import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.deps import get_db
from app.db.database import Base
from app.models.user import User
from main import app

# 테스트용 인메모리 데이터베이스 설정
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_register_user():
    """사용자 회원가입 테스트"""
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "password": "testpassword123",
            "display_name": "Test User"
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"
    assert "id" in data


def test_register_duplicate_email():
    """중복 이메일 회원가입 테스트"""
    # 첫 번째 사용자 등록
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "duplicate@example.com",
            "username": "user1",
            "password": "password123",
            "display_name": "User One"
        },
    )
    
    # 같은 이메일로 두 번째 사용자 등록 시도
    response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "duplicate@example.com",
            "username": "user2",
            "password": "password123",
            "display_name": "User Two"
        },
    )
    assert response.status_code == 400
    assert "이미 등록된 이메일입니다" in response.json()["detail"]


def test_login_success():
    """정상 로그인 테스트"""
    # 사용자 등록
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "login@example.com",
            "username": "loginuser",
            "password": "loginpassword",
            "display_name": "Login User"
        },
    )
    
    # 로그인
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "login@example.com",
            "password": "loginpassword"
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials():
    """잘못된 인증정보로 로그인 테스트"""
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "nonexistent@example.com",
            "password": "wrongpassword"
        },
    )
    assert response.status_code == 401
    assert "이메일 또는 비밀번호가 올바르지 않습니다" in response.json()["detail"]


def test_get_current_user():
    """현재 사용자 정보 조회 테스트"""
    # 사용자 등록
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "current@example.com",
            "username": "currentuser",
            "password": "currentpassword",
            "display_name": "Current User"
        },
    )
    
    # 로그인
    login_response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "current@example.com",
            "password": "currentpassword"
        },
    )
    token = login_response.json()["access_token"]
    
    # 현재 사용자 정보 조회
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "current@example.com"
    assert data["username"] == "currentuser"


def test_auth_test_endpoint():
    """인증 테스트 엔드포인트 테스트"""
    # 사용자 등록
    client.post(
        "/api/v1/auth/register",
        json={
            "email": "authtest@example.com",
            "username": "authtestuser",
            "password": "authtestpassword",
            "display_name": "Auth Test User"
        },
    )
    
    # 로그인
    login_response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "authtest@example.com",
            "password": "authtestpassword"
        },
    )
    token = login_response.json()["access_token"]
    
    # 인증 테스트
    response = client.get(
        "/api/v1/auth/test",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "인증 성공!"
    assert data["user"]["email"] == "authtest@example.com"


def test_unauthorized_access():
    """인증되지 않은 접근 테스트"""
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401


def test_invalid_token():
    """잘못된 토큰으로 접근 테스트"""
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": "Bearer invalid_token"}
    )
    assert response.status_code == 401