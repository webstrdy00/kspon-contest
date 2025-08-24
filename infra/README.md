# Infrastructure Setup

KSPON Contest Platform의 인프라 설정 파일들입니다.

## 🐳 Docker Compose 사용법

### 1. 데이터베이스 서비스 시작
```bash
cd infra
docker-compose up -d
```

### 2. 서비스 확인
```bash
# 모든 서비스 상태 확인
docker-compose ps

# 로그 확인
docker-compose logs -f postgres
docker-compose logs -f redis
```

### 3. 서비스 중지
```bash
# 서비스만 중지 (데이터는 보존)
docker-compose stop

# 서비스와 컨테이너 완전 삭제
docker-compose down

# 볼륨까지 완전 삭제 (주의: 데이터 손실)
docker-compose down -v
```

## 📊 서비스 구성

### PostgreSQL + PostGIS
- **포트**: 5432
- **데이터베이스**: sports_data_lab
- **사용자**: sports_data_lab
- **비밀번호**: sports_data_lab
- **기능**: PostGIS 확장으로 지리공간 데이터 지원

### Redis
- **포트**: 6379
- **비밀번호**: sports_data_lab
- **기능**: 캐싱, 세션 저장소

### pgAdmin (개발용)
- **포트**: 5050
- **이메일**: admin@kspon.com
- **비밀번호**: admin123
- **기능**: PostgreSQL 데이터베이스 관리 웹 인터페이스

## 🔧 백엔드 연결 설정

백엔드에서 다음과 같이 연결하세요:

### PostgreSQL 연결 URL
```
postgresql://sports_data_lab:sports_data_lab@localhost:5432/sports_data_lab
```

### Redis 연결 URL
```
redis://:sports_data_lab@localhost:6379
```

### 환경변수 설정 (.env)
```bash
# Database
POSTGRES_SERVER=localhost
POSTGRES_USER=sports_data_lab
POSTGRES_PASSWORD=sports_data_lab
POSTGRES_DB=sports_data_lab

# Redis
REDIS_URL=redis://:sports_data_lab@localhost:6379
```

## 🗄️ 데이터베이스 초기화

### 1. Alembic 마이그레이션 실행
```bash
cd backend
alembic upgrade head
```

### 2. 샘플 데이터 생성 (선택사항)
```bash
cd backend
python scripts/create_sample_data.py
```

## 🧪 연결 테스트

### PostgreSQL 연결 테스트
```bash
# psql 클라이언트로 연결
psql -h localhost -U sports_data_lab -d sports_data_lab

# 또는 Docker 컨테이너 내에서
docker exec -it kspon-postgres psql -U sports_data_lab -d sports_data_lab
```

### Redis 연결 테스트
```bash
# redis-cli로 연결
redis-cli -h localhost -p 6379 -a sports_data_lab ping

# 또는 Docker 컨테이너 내에서
docker exec -it kspon-redis redis-cli -a sports_data_lab ping
```

## 🔍 문제 해결

### 포트 충돌 해결
기존에 PostgreSQL이나 Redis가 실행 중이라면:
```bash
# 기존 서비스 중지
sudo systemctl stop postgresql
sudo systemctl stop redis-server

# 또는 docker-compose.yml에서 포트 변경
# postgres: "5433:5432"
# redis: "6380:6379"
```

### 데이터 초기화
```bash
# 모든 데이터 삭제 후 재시작
docker-compose down -v
docker-compose up -d
```

### 로그 확인
```bash
# 특정 서비스 로그
docker-compose logs -f postgres
docker-compose logs -f redis
docker-compose logs -f pgadmin
```

## 🚀 프로덕션 배포

프로덕션 환경에서는:
1. 비밀번호 변경 (강력한 비밀번호 사용)
2. pgAdmin 서비스 제거 또는 보안 설정
3. 볼륨 백업 설정
4. SSL/TLS 연결 활성화