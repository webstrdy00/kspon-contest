# 백엔드 인증 시스템 설치 및 설정 가이드

## 📦 의존성 설치

### 1. 새로운 패키지 설치
```bash
cd backend
pip install python-jose[cryptography]==3.3.0 passlib[bcrypt]==1.7.4 bcrypt==4.0.1 email-validator==2.0.0
```

### 2. 전체 의존성 재설치 (권장)
```bash
cd backend
pip install -r requirements.txt
```

## 🗄️ 데이터베이스 마이그레이션

사용자 테이블이 이미 존재하므로 추가 마이그레이션은 필요하지 않습니다.

## 🚀 서버 실행 및 테스트

### 1. 서버 실행
```bash
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 2. API 문서 확인
브라우저에서 `http://localhost:8000/docs`에 접속하여 새로운 인증 API 확인

### 3. 헬스 체크
```bash
curl http://localhost:8000/api/v1/health
```

## 🧪 인증 API 테스트

### 1. 회원가입
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "username": "testuser", 
    "password": "password123",
    "display_name": "Test User"
  }'
```

### 2. 로그인
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=password123"
```

응답에서 `access_token` 값을 복사합니다.

### 3. 인증이 필요한 API 테스트
```bash
curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

### 4. 인증 테스트 엔드포인트
```bash
curl -X GET "http://localhost:8000/api/v1/auth/test" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

## 🏃‍♂️ 단위 테스트 실행

```bash
cd backend
python -m pytest tests/test_auth.py -v
```

## 🔧 프론트엔드 연동 가이드

프론트엔드에서 다음 엔드포인트들을 사용할 수 있습니다:

- `POST /api/v1/auth/register` - 회원가입
- `POST /api/v1/auth/login` - 로그인 (OAuth2 호환)
- `GET /api/v1/auth/me` - 현재 사용자 정보
- `PUT /api/v1/auth/me` - 사용자 정보 수정
- `GET /api/v1/auth/test` - 인증 테스트

### JWT 토큰 사용법
1. 로그인 성공 시 `access_token` 저장
2. API 요청 시 헤더에 `Authorization: Bearer <token>` 추가
3. 토큰 만료 시 재로그인 필요 (기본 30분)

## 🛠️ 설정값

`app/core/config.py`에서 다음 값들을 환경변수로 설정 가능:

- `SECRET_KEY`: JWT 서명용 비밀키
- `ALGORITHM`: JWT 알고리즘 (기본: HS256)  
- `ACCESS_TOKEN_EXPIRE_MINUTES`: 토큰 만료 시간 (기본: 30분)

## 🔍 문제 해결

### 1. 패키지 설치 오류
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### 2. 데이터베이스 연결 오류
PostgreSQL이 실행 중인지 확인하고 `app/core/config.py`의 데이터베이스 설정을 확인하세요.

### 3. 테스트 실패
SQLite 드라이버가 필요할 수 있습니다:
```bash
pip install sqlite3
```