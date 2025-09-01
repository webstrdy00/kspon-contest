# KSPON Contest Platform - Backend API

KSPON (Korean Sports Policy Opinion Network) 콘테스트 플랫폼의 FastAPI 백엔드 시스템입니다.

## 🏗️ 시스템 아키텍처

### 기술 스택

- **Framework**: FastAPI (Python)
- **Authentication**: JWT-based authentication with OAuth2 compatibility
- **Database**: PostgreSQL with PostGIS extension
- **ORM**: SQLAlchemy with Alembic migrations
- **Caching**: Redis
- **Security**: bcrypt password hashing, python-jose JWT
- **HTTP Client**: httpx with tenacity for retry logic
- **Scheduler**: APScheduler for automated data collection
- **Data Processing**: Pandas, NumPy for ETL pipeline
- **Testing**: pytest
- **Documentation**: Auto-generated OpenAPI/Swagger docs

### 프로젝트 구조

```
backend/
├── app/
│   ├── api/v1/
│   │   ├── endpoints/
│   │   │   ├── auth.py          # 인증 API
│   │   │   ├── dashboard.py     # 대시보드 API
│   │   │   ├── facilities.py    # 체육시설 API
│   │   │   ├── proposals.py     # 정책 제안 API
│   │   │   ├── reports.py       # 리포트 API
│   │   │   ├── data_import.py   # 공공데이터 수집 API (NEW)
│   │   │   ├── csv_upload.py    # CSV 업로드 API (NEW)
│   │   │   └── scheduler.py     # 스케줄러 관리 API (NEW)
│   │   └── api.py              # API 라우터 통합
│   ├── services/               # 외부 API 클라이언트 (2025-08-31 업데이트)
│   │   ├── base_api_client.py
│   │   ├── facilities_api_client.py
│   │   ├── fund_api_client.py                      # 기금지원 API
│   │   ├── fund_evaluation_api_client.py           # 기금평가 API (NEW)
│   │   ├── fund_comprehensive_api_client.py        # 종합실적 API (NEW)
│   │   └── performance_api_client.py               # 성과포상금 API
│   ├── etl/                    # ETL 파이프라인 (NEW)
│   │   └── csv_processor.py
│   ├── tasks/                  # 백그라운드 태스크 (NEW)
│   │   └── scheduler.py
│   ├── core/
│   │   ├── config.py           # 설정 관리
│   │   ├── deps.py             # FastAPI 의존성
│   │   └── security.py         # JWT/보안 기능
│   ├── crud/
│   │   └── user.py             # 사용자 CRUD 작업
│   ├── db/
│   │   └── database.py         # 데이터베이스 연결
│   ├── models/
│   │   ├── user.py             # 사용자 모델
│   │   ├── facility.py         # 시설 모델
│   │   ├── proposal.py         # 제안 모델
│   │   ├── budget.py           # 예산 모델
│   │   └── ...                 # 기타 모델들
│   └── schemas/
│       ├── user.py             # 사용자 스키마
│       └── token.py            # JWT 토큰 스키마
├── tests/
│   ├── test_auth.py            # 인증 시스템 테스트
│   └── test_api_clients.py    # API 클라이언트 테스트 (NEW)
├── alembic/                    # 데이터베이스 마이그레이션
├── main.py                     # FastAPI 애플리케이션 진입점
└── requirements.txt            # Python 의존성
```

## 🚀 빠른 시작

### 1. 환경 설정

#### 필수 요구사항

- Python 3.12+ (numpy 1.26.4 호환성)
- PostgreSQL (Docker 권장)
- Redis (선택사항, 캐싱용)

#### 가상환경 생성 및 활성화

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

#### 의존성 설치

```bash
pip install -r requirements.txt

# Windows Python 3.12에서 numpy 설치 오류 시
pip install numpy==1.26.4
```

### 2. 데이터베이스 설정

#### Docker를 사용한 데이터베이스 실행 (권장)

```bash
# 프로젝트 루트에서
cd ../infra
docker-compose up -d
```

#### 환경변수 설정 (.env 파일 생성)

```bash
# .env.sample을 복사하여 .env 파일 생성
cp .env.sample .env

# 필수 환경변수 (반드시 설정 필요)
SECRET_KEY=your-very-secure-secret-key-here  # 보안상 중요!
POSTGRES_PASSWORD=your-secure-password       # 보안상 중요!

# Database
POSTGRES_SERVER=localhost
POSTGRES_USER=postgres
POSTGRES_DB=kspon

# JWT Settings
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# 공공데이터포털 API (https://www.data.go.kr에서 발급)
DATA_GO_KR_API_KEY=your-api-key-here

# Redis (선택사항)
REDIS_URL=redis://:sports_data_lab@localhost:6379
```

#### 데이터베이스 마이그레이션

```bash
# 마이그레이션 실행
alembic upgrade head
```

### 3. 서버 실행

#### 개발 서버 시작

```bash
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### API 문서 확인

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/api/v1/health

## 🔐 인증 시스템

### JWT 인증 API

#### 회원가입

```bash
POST /api/v1/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "username": "testuser",
  "password": "securepassword",
  "display_name": "Test User",
  "bio": "스포츠를 사랑하는 시민입니다"
}
```

#### 로그인 (OAuth2 호환)

```bash
POST /api/v1/auth/login
Content-Type: application/x-www-form-urlencoded

username=user@example.com&password=securepassword
```

**응답 예시:**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### 현재 사용자 정보 조회

```bash
GET /api/v1/auth/me
Authorization: Bearer <access_token>
```

#### 사용자 정보 수정

```bash
PUT /api/v1/auth/me
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "display_name": "Updated Name",
  "bio": "업데이트된 자기소개"
}
```

### 인증 의존성 사용법

```python
from fastapi import Depends
from app.core.deps import get_current_active_user
from app.models.user import User

@router.get("/protected-endpoint")
def protected_route(
    current_user: User = Depends(get_current_active_user)
):
    return {"user_id": current_user.id, "message": "인증 성공!"}
```

## 🧪 테스트

### 전체 테스트 실행

```bash
python -m pytest tests/ -v
```

### 특정 테스트 실행

```bash
# 인증 테스트만 실행
python -m pytest tests/test_auth.py -v

# 커버리지 포함
python -m pytest tests/ --cov=app --cov-report=html
```

### API 테스트 (cURL)

```bash
# 회원가입
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","username":"testuser","password":"password123","display_name":"Test User"}'

# 로그인
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=password123"

# 인증된 요청
curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer <your_token_here>"
```

## 🗄️ 데이터베이스

### 모델 구조

#### User 모델

```python
class User(Base):
    # 기본 정보
    email: str                    # 이메일 (로그인 ID)
    username: str                 # 사용자명
    hashed_password: str          # 해시된 비밀번호
    display_name: str             # 표시명

    # 프로필 정보
    bio: str                      # 자기소개
    avatar_url: str               # 아바타 이미지
    region_code: str              # 거주지역

    # 활동 통계
    proposal_count: int           # 작성한 제안 수
    vote_count: int               # 투표 참여 수
    like_received: int            # 받은 공감 수

    # 관심사
    interested_sports: JSON       # 관심 종목
    interested_regions: JSON      # 관심 지역
```

### 마이그레이션 관리

#### 새로운 마이그레이션 생성

```bash
alembic revision --autogenerate -m "Add new feature"
```

#### 마이그레이션 적용

```bash
# 최신 버전으로 업그레이드
alembic upgrade head

# 특정 버전으로 업그레이드/다운그레이드
alembic upgrade <revision_id>
alembic downgrade <revision_id>
```

#### 마이그레이션 히스토리 확인

```bash
alembic history --verbose
alembic current
```

## 📊 API 엔드포인트

### 인증 관련

- `POST /api/v1/auth/register` - 사용자 회원가입
- `POST /api/v1/auth/login` - 사용자 로그인
- `GET /api/v1/auth/me` - 현재 사용자 정보
- `PUT /api/v1/auth/me` - 사용자 정보 수정
- `GET /api/v1/auth/test` - 인증 테스트

### 공공데이터 수집 (NEW - 2025-08-30)

- `POST /api/v1/data/import/facilities` - 체육시설 데이터 수집
- `POST /api/v1/data/import/fund` - 예산 데이터 수집
- `POST /api/v1/data/import/performance` - 성과금 데이터 수집
- `GET /api/v1/data/analysis/budget-performance/{year}` - 예산-성과 분석
- `GET /api/v1/data/statistics/facilities` - 시설 통계

### CSV 데이터 처리 (NEW - 2025-08-30)

- `POST /api/v1/csv/upload/facility-demand` - 수요 CSV 업로드
- `POST /api/v1/csv/upload/leisure-time` - 여가시간 CSV 업로드
- `POST /api/v1/csv/merge-analysis` - 수요-공급 병합 분석
- `GET /api/v1/csv/csv-templates` - CSV 템플릿 정보

### 스케줄러 관리 (NEW - 2025-08-30)

- `GET /api/v1/scheduler/status` - 스케줄러 상태 조회
- `POST /api/v1/scheduler/start` - 스케줄러 시작
- `POST /api/v1/scheduler/stop` - 스케줄러 중지
- `POST /api/v1/scheduler/trigger/{job_id}` - 작업 수동 실행

### 시스템

- `GET /api/v1/health` - 서버 상태 확인

### 기타 API (기존 구현)

- `GET /api/v1/dashboard/*` - 대시보드 관련 API
- `GET /api/v1/facilities/*` - 체육시설 관련 API
- `POST /api/v1/proposals/*` - 정책 제안 관련 API
- `GET /api/v1/reports/*` - 리포트 관련 API

## 🔧 개발 도구

### 코드 품질 검사

```bash
# 타입 체크 (mypy 설치 필요)
mypy app/

# 코드 포맷팅 (black 설치 필요)
black app/ tests/

# 임포트 정렬 (isort 설치 필요)
isort app/ tests/
```

### 개발 서버 옵션

```bash
# 기본 개발 서버
uvicorn main:app --reload

# 상세 로그 포함
uvicorn main:app --reload --log-level debug

# 특정 포트 지정
uvicorn main:app --reload --port 8080

# 외부 접속 허용
uvicorn main:app --reload --host 0.0.0.0
```

## 📝 설정 관리

### 환경변수 옵션

```bash
# JWT 설정
SECRET_KEY=your-very-secure-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# 데이터베이스 설정
POSTGRES_SERVER=localhost
POSTGRES_USER=postgres
POSTGRES_PASSWORD=12345
POSTGRES_DB=kspon

# CORS 설정
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:8000"]

# 외부 API 설정
DATA_GO_KR_API_KEY=your-data-go-kr-api-key
FACILITIES_API_URL=http://apis.data.go.kr/B554287/PublicSportsFacilitiesService
FUND_SUPPORT_API_URL=https://apis.data.go.kr/B551014/SRVC_OD_API_FUN_OBJ_ORG_API
PERFORMANCE_REWARD_API_URL=https://apis.data.go.kr/B551014/SRVC_TODZ_USFUN_PIRPEN_NON_DSPSN
FUND_EVALUATION_API_URL=https://apis.data.go.kr/B551014/SRVC_OD_API_FUN_FLDESTM_QSTN_API
FUND_COMPREHENSIVE_API_URL=https://apis.data.go.kr/B551014/SRVC_OD_API_FUN_INSTT_BSNS_RSLT_API

# 스케줄러 설정
AUTO_START_SCHEDULER=false  # 서버 시작 시 스케줄러 자동 시작

# 캐시 설정
REDIS_URL=redis://:sports_data_lab@localhost:6379
```

### 프로덕션 설정

```bash
# 프로덕션 환경에서는 반드시 변경해야 할 설정들
SECRET_KEY=<강력한-랜덤-키-생성>
POSTGRES_PASSWORD=<강력한-데이터베이스-패스워드>
```

## 🚨 문제 해결

### 최근 업데이트 (2025-08-31)

#### SQLAlchemy 2.0 마이그레이션

- `Column` → `mapped_column()` 변경
- `Mapped[]` 타입 어노테이션 추가
- `DeclarativeBase` 사용

#### Pydantic v2 마이그레이션

- `BaseSettings`를 `pydantic_settings`에서 import
- `@validator` → `@field_validator`로 변경

#### 공공데이터 API URL 업데이트

모든 API URL이 최신 버전으로 업데이트되었습니다:

- 체육인복지 경기력성과포상금: `TODZ_USFUN_PIRPEN_NON_DSPSN` 엔드포인트
- 국민체육진흥기금: 새로운 엔드포인트 구조
- 상세 내용은 `API_URL_GUIDE.md` 참조

### 일반적인 문제들

#### 1. 데이터베이스 연결 오류

```bash
# PostgreSQL 서비스 확인
docker-compose ps

# 데이터베이스 로그 확인
docker-compose logs postgres

# 연결 테스트
psql -h localhost -U postgres -d kspon
```

#### 2. 패키지 설치 오류

```bash
# pip 업그레이드
pip install --upgrade pip

# 캐시 클리어 후 재설치
pip cache purge
pip install -r requirements.txt --force-reinstall
```

#### 3. 마이그레이션 오류

```bash
# 마이그레이션 상태 확인
alembic current

# 수동으로 마이그레이션 재설정 (주의: 데이터 손실 가능)
alembic stamp head
```

#### 4. JWT 토큰 관련 오류

- SECRET_KEY가 제대로 설정되었는지 확인
- 토큰 만료 시간 확인 (기본 30분)
- 클라이언트에서 Authorization 헤더 형식 확인: `Bearer <token>`

## 📚 추가 리소스

### 개발 문서

- **FastAPI 공식 문서**: https://fastapi.tiangolo.com/
- **SQLAlchemy 문서**: https://docs.sqlalchemy.org/
- **Alembic 문서**: https://alembic.sqlalchemy.org/

### API 문서

- **로컬 Swagger UI**: http://localhost:8000/docs
- **로컬 ReDoc**: http://localhost:8000/redoc

### 관련 파일

- **인증 시스템 설치 가이드**: `README_AUTH.md`
- **인프라 설정 가이드**: `../infra/README.md`
- **API 오류 해결 가이드**: `API_URL_GUIDE.md`

---

## 🤝 기여하기

### 개발 워크플로우

1. 기능 브랜치 생성: `git checkout -b feature/새로운-기능`
2. 코드 작성 및 테스트
3. 커밋: `git commit -m "FEAT: 새로운 기능 추가"`
4. 푸시 및 Pull Request 생성

### 커밋 메시지 규칙

- `FEAT: 새로운 기능 추가`
- `FIX: 버그 수정`
- `DOCS: 문서 수정`
- `TEST: 테스트 코드 추가`
- `REFACTOR: 코드 리팩토링`

---

**이제 KSPON 콘테스트 플랫폼의 백엔드 시스템이 완전히 준비되었습니다!** 🚀

질문이나 문제가 있으시면 개발 로그나 관련 문서를 참조하시거나, 이슈를 생성해 주세요.
