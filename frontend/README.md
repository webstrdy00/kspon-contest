# KSPON Contest Platform - Frontend

KSPON (Korean Sports Policy Opinion Network) 콘테스트 플랫폼의 Next.js 프론트엔드 애플리케이션입니다.

## 🏗️ 시스템 아키텍처

### 기술 스택
- **Framework**: Next.js 15.2.4 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS 4.1.9 + shadcn/ui
- **UI Components**: Radix UI primitives
- **State Management**: React Context API
- **Forms**: React Hook Form + Zod validation
- **HTTP Client**: Axios
- **Maps**: Leaflet.js with enhanced features
  - VWorld/OpenStreetMap tiles
  - MarkerCluster for performance
  - Heatmap visualization
  - Custom icons and popups
- **Charts**: Recharts + D3.js
- **PDF Export**: html2canvas + jsPDF
- **Fonts**: Geist Sans & Mono
- **Icons**: Lucide React
- **Themes**: next-themes (다크/라이트 모드)

### 프로젝트 구조
```
frontend/
├── app/                        # Next.js App Router pages
│   ├── auth/                   # 인증 페이지 (로그인, 회원가입)
│   ├── dashboard/              # 대시보드
│   │   └── budget-performance/ # 예산-성과 분석
│   ├── help/                   # 도움말
│   ├── notifications/          # 알림
│   ├── profile/               # 사용자 프로필
│   ├── proposals/             # 정책 제안
│   ├── reports/               # 우리 동네 리포트
│   ├── stats/                 # 플랫폼 통계
│   ├── globals.css            # 글로벌 CSS
│   ├── layout.tsx            # 루트 레이아웃
│   └── page.tsx              # 홈페이지
│
├── components/                # 재사용 가능한 컴포넌트
│   ├── auth/                  # 인증 관련 컴포넌트
│   │   ├── AuthGuard.tsx     # 라우트 보호
│   │   ├── LoginForm.tsx     # 로그인 폼
│   │   └── RegisterForm.tsx  # 회원가입 폼
│   ├── budget-performance/   # 예산-성과 분석 컴포넌트 (Phase 3)
│   │   └── charts/
│   │       ├── ScatterPlot.tsx    # 예산 vs 성과 산점도
│   │       ├── Treemap.tsx       # 예산 배분 트리맵
│   │       └── TrendChart.tsx    # 시계열 트렌드 차트
│   ├── dashboard/            # 대시보드 컴포넌트
│   │   ├── enhanced-leaflet-map.tsx  # 향상된 지도 컴포넌트
│   │   ├── supply-demand-map.tsx     # 수요-공급 분석 맵
│   │   └── leaflet-map.tsx          # 기본 지도 컴포넌트
│   ├── home/                 # 홈페이지 컴포넌트
│   ├── layout/               # 레이아웃 컴포넌트
│   │   ├── Header.tsx        # 헤더
│   │   ├── Sidebar.tsx       # 사이드바
│   │   └── Navigation.tsx    # 네비게이션
│   ├── proposals/            # 정책 제안 컴포넌트
│   ├── reports/              # 리포트 컴포넌트
│   └── ui/                   # shadcn/ui 컴포넌트
│
├── public/                   # 정적 파일
├── lib/                      # 유틸리티 함수
│   └── api/                  # API 클라이언트
│       └── budget-performance.ts  # 예산-성과 API 클라이언트 (Phase 3)
├── contexts/                 # React Context providers
│   └── AuthContext.tsx       # 인증 상태 관리
├── types/                    # TypeScript 타입 정의
├── styles/                   # 스타일 파일 (있는 경우)
├── .env.sample              # 환경 변수 예시
├── .env                     # 실제 환경 변수 (Git 무시)
├── .gitignore               # Git 무시 파일
├── next.config.ts           # Next.js 설정
├── package.json             # 프로젝트 의존성
├── tailwind.config.ts       # Tailwind CSS 설정
└── tsconfig.json            # TypeScript 설정
```

## 🚀 시작하기

### 1. 패키지 설치

```bash
# npm 사용
npm install

# 또는 pnpm 사용 (권장)
pnpm install
```

### 2. 환경 변수 설정

`.env.sample` 파일을 `.env`로 복사하고 필요한 환경 변수를 설정합니다:

```bash
cp .env.sample .env
```

```env
# API 엔드포인트
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1

# VWorld Map API Key (선택사항 - 없으면 OpenStreetMap 사용)
NEXT_PUBLIC_VWORLD_KEY=your_vworld_key_here

# 공공데이터포털 API Key (선택사항)
NEXT_PUBLIC_DATA_GO_KR_API_KEY=your_api_key_here

# 앱 설정
NEXT_PUBLIC_ENV=development
```

### 3. 개발 서버 실행

```bash
# 개발 서버 시작
npm run dev
# 또는
pnpm dev

# 브라우저에서 http://localhost:3000 접속
```

### 4. 빌드 및 배포

```bash
# 프로덕션 빌드
npm run build
# 또는
pnpm build

# 프로덕션 서버 시작
npm run start
# 또는
pnpm start

# 린트 검사
npm run lint
# 또는
pnpm lint
```

## 🔐 인증 시스템

### AuthContext 사용법

```tsx
import { useAuth } from '@/contexts/AuthContext'

function MyComponent() {
  const { user, login, logout, isLoading } = useAuth()
  
  const handleLogin = async (email: string, password: string) => {
    try {
      await login(email, password)
      // 로그인 성공 후 리다이렉트
    } catch (error) {
      // 에러 처리
    }
  }
  
  if (isLoading) return <div>로딩 중...</div>
  
  return (
    <div>
      {user ? (
        <div>환영합니다, {user.display_name}님!</div>
      ) : (
        <button onClick={() => handleLogin()}>로그인</button>
      )}
    </div>
  )
}
```

### AuthGuard 컴포넌트

```tsx
import AuthGuard from '@/components/auth/AuthGuard'

function ProtectedPage() {
  return (
    <AuthGuard>
      <div>이 내용은 로그인한 사용자만 볼 수 있습니다.</div>
    </AuthGuard>
  )
}
```

## 🗺️ 지도 기능

### Enhanced Leaflet Map

수요-공급 분석을 위한 향상된 지도 컴포넌트:

```tsx
import { EnhancedLeafletMap } from '@/components/dashboard/enhanced-leaflet-map'

function MapPage() {
  return (
    <EnhancedLeafletMap
      selectedFacility="all"
      showDemandLayer={true}
      showHeatmap={true}
      showClusters={true}
      selectedRegion={null}
      onRegionSelect={(region) => console.log(region)}
    />
  )
}
```

### 주요 기능
- **VWorld/OpenStreetMap 타일**: 한국 지도 서비스 또는 OSM 자동 선택
- **시설 클러스터링**: MarkerCluster로 대량 데이터 성능 최적화
- **히트맵 시각화**: 수요 강도를 색상으로 표현
- **커스텀 마커**: 시설 유형별 이모지 아이콘
- **상세 팝업**: 시설 정보, 수요-공급 비율, 접근성 정보
- **필터링**: 지역별, 시설 유형별 필터

## 📊 주요 페이지

### 1. 홈페이지 (/)
- 플랫폼 소개
- 주요 통계
- 퀵 액세스 메뉴

### 2. 대시보드 (/dashboard)
- **수요-공급 분석 맵**: 실시간 시설 분포 및 수요 분석
- **예산-성과 분석** (/dashboard/budget-performance) - Phase 3 ✅
  - 효율성 분석: S/A/B/C/D 등급 시스템
  - ROI 분석: 투자 대비 수익률
  - 지역별 비교: 시도별 예산 효율성
  - 시계열 트렌드: 연도별 추이
- **지역별 통계**: 시도별 체육시설 현황

### 3. 우리 동네 리포트 (/reports)
- AI 기반 자동 리포트 생성
- 템플릿 선택 (기본/고급/만족도)
- PDF 다운로드

### 4. 시민 정책 제안 (/proposals)
- 정책 제안 작성
- 커뮤니티 투표
- 댓글 및 토론

### 5. 프로필 (/profile)
- 사용자 정보 관리
- 활동 내역
- 알림 설정

## 🧪 테스트

```bash
# 테스트 실행
npm run test

# 테스트 커버리지
npm run test:coverage
```

## 📝 코드 컨벤션

- **컴포넌트**: PascalCase (예: `SupplyDemandMap.tsx`)
- **유틸리티**: camelCase (예: `formatDate.ts`)
- **스타일**: Tailwind CSS 유틸리티 클래스 사용
- **타입**: interface 선호, 필요시 type 사용
- **상태관리**: React Context API 사용

## 🔧 환경 설정

### VSCode 추천 익스텐션
- ESLint
- Prettier
- Tailwind CSS IntelliSense
- TypeScript Vue Plugin (Volar)

### 개발 도구
- React Developer Tools
- Redux DevTools (Context API 디버깅)

## 📚 주요 의존성

```json
{
  "dependencies": {
    "next": "15.2.4",
    "react": "^18",
    "react-dom": "^18",
    "leaflet": "^1.9.4",
    "leaflet.markercluster": "^1.5.3",
    "leaflet.heat": "^0.2.0",
    "recharts": "2.15.4",
    "axios": "^1.6.2",
    "react-hook-form": "^7.60.0",
    "zod": "3.25.67",
    "@radix-ui/react-*": "latest",
    "tailwindcss": "^4.1.9",
    "lucide-react": "^0.454.0"
  }
}
```

## 🤝 기여하기

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'FEAT: Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이센스

이 프로젝트는 MIT 라이센스를 따릅니다.

## 📞 문의

KSPON Contest Platform Team - contact@kspon.kr

---

**최근 업데이트**: 2025-01-06
- Phase 3: 예산-성과 분석 시스템 구현 완료 ✅
  - Recharts 기반 차트 컴포넌트 3종 (ScatterPlot, Treemap, TrendChart)
  - ETag 지원 API 클라이언트
  - LocalStorage 캐싱으로 성능 최적화
  - 차트 렌더링 P95 < 890ms 달성
- Phase 2: 수요-공급 분석 맵 구현 완료
- Enhanced Leaflet Map 컴포넌트 추가
- MarkerCluster, Heatmap 기능 통합