"""
DATABASE_URL 유효성 검사 테스트
"""
import importlib
import types
import pytest


def test_missing_database_url_raises_runtime_error(monkeypatch):
    """DATABASE_URL이 없을 때 RuntimeError 발생 확인"""
    # 모듈을 임포트하기 전에 설정 준비
    import app.core.config as config
    import app.core.database as db
    
    # 원본 설정 백업
    original_settings = config.settings
    
    # DATABASE_URL이 None인 가짜 설정 객체 생성
    fake_settings = types.SimpleNamespace(DATABASE_URL=None)
    
    # 설정을 가짜 객체로 교체
    monkeypatch.setattr(config, 'settings', fake_settings)
    
    # database 모듈 리로드 시 RuntimeError 발생 확인
    with pytest.raises(RuntimeError) as exc_info:
        importlib.reload(db)
    
    # 에러 메시지 확인
    assert "DATABASE_URL is not configured" in str(exc_info.value)
    assert ".env file" in str(exc_info.value)
    
    # 원본 설정 복원
    monkeypatch.setattr(config, 'settings', original_settings)
    
    # 정상 상태로 모듈 리로드
    importlib.reload(db)


def test_valid_database_url_no_error(monkeypatch):
    """유효한 DATABASE_URL이 있을 때 정상 동작 확인"""
    import app.core.config as config
    import app.core.database as db
    
    # 원본 설정 백업
    original_settings = config.settings
    
    # 유효한 DATABASE_URL을 가진 가짜 설정 객체 생성
    fake_settings = types.SimpleNamespace(
        DATABASE_URL="postgresql://user:pass@localhost/testdb"
    )
    
    # 설정을 가짜 객체로 교체
    monkeypatch.setattr(config, 'settings', fake_settings)
    
    try:
        # database 모듈 리로드 - 에러 없이 실행되어야 함
        importlib.reload(db)
        
        # DATABASE_URL이 정상적으로 설정되었는지 확인
        assert db.DATABASE_URL is not None
        assert "postgresql+asyncpg://" in db.DATABASE_URL
        
    finally:
        # 원본 설정 복원
        monkeypatch.setattr(config, 'settings', original_settings)
        importlib.reload(db)


def test_database_url_postgresql_conversion():
    """PostgreSQL URL이 asyncpg 드라이버로 변환되는지 확인"""
    import app.core.config as config
    import app.core.database as db
    
    # 현재 설정에서 DATABASE_URL 확인
    if config.settings.DATABASE_URL and config.settings.DATABASE_URL.startswith("postgresql://"):
        # asyncpg 드라이버로 변환되었는지 확인
        assert "postgresql+asyncpg://" in db.DATABASE_URL or "sqlite" in db.DATABASE_URL
    
    # SQLite 메모리 DB 사용 시
    elif config.settings.DATABASE_URL and "sqlite" in config.settings.DATABASE_URL:
        assert "sqlite" in db.DATABASE_URL