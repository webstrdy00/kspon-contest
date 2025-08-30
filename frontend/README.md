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
- **Maps**: Leaflet.js + react-leaflet
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
│   ├── dashboard/            # 대시보드 컴포넌트
│   ├── home/                 # 홈페이지 컴포넌트
│   ├── layout/               # 레이아웃 컴포넌트
│   │   ├── Header.tsx        # 헤더
│   │   ├── Sidebar.tsx       # 사이드바
│   │   └── Navigation.tsx    # 네비게이션
│   ├── proposals/            # 정책 제안 컴포넌트
│   ├── reports/              # 리포트 컴포넌트
│   ├── stats/                # 통계 컴포넌트
│   ├── ui/                   # shadcn/ui 기본 컴포넌트
│   └── theme-provider.tsx    # 테마 프로바이더
│
├── contexts/                 # React Context
│   └── AuthContext.tsx      # 인증 상태 관리
│
├── hooks/                   # 커스텀 훅
├── lib/                    # 유틸리티 함수
├── public/                 # 정적 파일
├── styles/                 # 추가 스타일시트
├── components.json         # shadcn/ui 설정
├── next.config.mjs        # Next.js 설정
├── package.json           # 의존성 및 스크립트
├── tailwind.config.js     # Tailwind CSS 설정
└── tsconfig.json          # TypeScript 설정
```

## 🚀 빠른 시작

### 1. 환경 설정

#### 필수 요구사항
- Node.js 18+
- npm 또는 pnpm

#### 의존성 설치
```bash
cd frontend

# npm 사용
npm install

# 또는 pnpm 사용 (권장)
pnpm install
```

### 2. 환경변수 설정

`.env.local` 파일을 생성하고 다음 변수를 설정하세요:
```bash
# API 서버 URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# 기타 설정
NEXT_PUBLIC_APP_NAME=KSPON Contest Platform
NEXT_PUBLIC_APP_VERSION=1.0.0
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

### 백엔드 API 연동

```tsx
// contexts/AuthContext.tsx에서 실제 API 호출
const login = async (email: string, password: string) => {
  const response = await axios.post('/api/v1/auth/login', {
    username: email, // OAuth2 형식
    password
  })
  
  const { access_token } = response.data
  localStorage.setItem('access_token', access_token)
  
  // 사용자 정보 조회
  const userResponse = await axios.get('/api/v1/auth/me', {
    headers: { Authorization: `Bearer ${access_token}` }
  })
  
  setUser(userResponse.data)
}
```

## 📄 주요 페이지 및 기능

### 1. 홈페이지 (`/`)
- 플랫폼 소개 및 주요 기능 안내
- 빠른 접근 버튼 (대시보드, 리포트, 제안서)
- 최신 통계 및 공지사항

### 2. 대시보드 (`/dashboard`)
- **수요-공급 분석 맵**: Leaflet.js를 사용한 인터랙티브 지도
- **예산-성과 분석**: Recharts로 시각화된 차트
- **지역별 체육시설 현황**: 실시간 데이터 표시
- **필터링 및 검색 기능**: 지역, 시설 유형별 필터

### 3. 우리 동네 리포트 (`/reports`)
- **AI 기반 리포트 생성**: 단계별 리포트 작성 인터페이스
- **리포트 템플릿**: 기본형, 고급형, 만족도형
- **PDF 내보내기**: html2canvas + jsPDF 사용
- **리포트 관리**: 저장, 수정, 공유 기능

### 4. 시민 정책 제안 (`/proposals`)
- **제안서 작성**: 다단계 폼 검증 (React Hook Form + Zod)
- **제안서 목록**: 카드/리스트 뷰 지원
- **투표 및 댓글**: 커뮤니티 참여 기능
- **고급 검색**: 카테고리, 지역, 상태별 필터링

### 5. 사용자 프로필 (`/profile`)
- **프로필 관리**: 개인정보 수정, 아바타 업로드
- **활동 내역**: 작성한 제안, 투표 기록
- **관심사 설정**: 스포츠 종목, 지역, 시설 유형
- **배지 시스템**: 활동에 따른 배지 획득

### 6. 인증 페이지 (`/auth`)
- **로그인 페이지**: 이메일/비밀번호 로그인
- **회원가입 페이지**: 상세 프로필 정보 입력
- **소셜 로그인**: Google, Naver 연동 (향후 계획)

## 🎨 UI/UX 디자인 시스템

### shadcn/ui 컴포넌트

```tsx
// 기본 UI 컴포넌트 사용 예시
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Dialog, DialogContent, DialogTrigger } from '@/components/ui/dialog'

function ExampleComponent() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>제목</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          <Input placeholder="입력하세요" />
          <Dialog>
            <DialogTrigger asChild>
              <Button>모달 열기</Button>
            </DialogTrigger>
            <DialogContent>
              <p>모달 내용</p>
            </DialogContent>
          </Dialog>
        </div>
      </CardContent>
    </Card>
  )
}
```

### 테마 시스템

```tsx
// 다크/라이트 모드 토글
import { useTheme } from 'next-themes'

function ThemeToggle() {
  const { theme, setTheme } = useTheme()
  
  return (
    <button onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}>
      테마 변경
    </button>
  )
}
```

### 반응형 디자인

```tsx
// Tailwind CSS를 사용한 반응형 스타일
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
  <Card className="p-4 hover:shadow-lg transition-shadow">
    모바일: 1열, 태블릿: 2열, 데스크톱: 3열
  </Card>
</div>
```

## 📊 데이터 시각화

### 지도 컴포넌트 (Leaflet.js)

```tsx
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet'

function FacilityMap() {
  return (
    <MapContainer center={[37.5665, 126.9780]} zoom={13}>
      <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />
      <Marker position={[37.5665, 126.9780]}>
        <Popup>서울시청 체육시설</Popup>
      </Marker>
    </MapContainer>
  )
}
```

### 차트 컴포넌트 (Recharts)

```tsx
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts'

function BudgetChart({ data }: { data: any[] }) {
  return (
    <LineChart width={600} height={300} data={data}>
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="year" />
      <YAxis />
      <Tooltip />
      <Legend />
      <Line type="monotone" dataKey="budget" stroke="#8884d8" />
      <Line type="monotone" dataKey="performance" stroke="#82ca9d" />
    </LineChart>
  )
}
```

## 📱 폼 관리 및 검증

### React Hook Form + Zod 사용법

```tsx
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'

const proposalSchema = z.object({
  title: z.string().min(5, '제목은 5자 이상이어야 합니다'),
  content: z.string().min(10, '내용은 10자 이상이어야 합니다'),
  category: z.string().min(1, '카테고리를 선택해주세요'),
})

type ProposalFormData = z.infer<typeof proposalSchema>

function ProposalForm() {
  const {
    register,
    handleSubmit,
    formState: { errors }
  } = useForm<ProposalFormData>({
    resolver: zodResolver(proposalSchema)
  })

  const onSubmit = (data: ProposalFormData) => {
    // 서버로 데이터 전송
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <Input
        {...register('title')}
        placeholder="제안서 제목"
      />
      {errors.title && <p className="text-red-500">{errors.title.message}</p>}
      
      <Button type="submit">제출</Button>
    </form>
  )
}
```

## 🔧 개발 도구 및 설정

### Next.js 설정 (`next.config.mjs`)
```javascript
const nextConfig = {
  eslint: {
    ignoreDuringBuilds: true,  // 빌드 시 ESLint 무시
  },
  typescript: {
    ignoreBuildErrors: true,   // 빌드 시 TypeScript 오류 무시
  },
  images: {
    unoptimized: true,         // 이미지 최적화 비활성화
  },
}
```

### Tailwind CSS 설정
```javascript
// tailwind.config.js
module.exports = {
  content: [
    './pages/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}',
    './app/**/*.{ts,tsx}',
    './src/**/*.{ts,tsx}',
  ],
  theme: {
    extend: {
      colors: {
        // 커스텀 색상 팔레트
      },
      fontFamily: {
        sans: ['Geist Sans', 'sans-serif'],
        mono: ['Geist Mono', 'monospace'],
      },
    },
  },
  plugins: [require('tailwindcss-animate')],
}
```

### TypeScript 설정 (`tsconfig.json`)
```json
{
  "compilerOptions": {
    "target": "es5",
    "lib": ["dom", "dom.iterable", "es6"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "forceConsistentCasingInFileNames": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [
      {
        "name": "next"
      }
    ],
    "baseUrl": ".",
    "paths": {
      "@/*": ["./*"]
    }
  }
}
```

## 🚨 문제 해결

### 일반적인 문제들

#### 1. 빌드 오류
```bash
# 의존성 재설치
rm -rf node_modules package-lock.json pnpm-lock.yaml
pnpm install

# TypeScript 오류 무시 (임시)
# next.config.mjs에서 ignoreBuildErrors: true 설정
```

#### 2. Leaflet.js SSR 오류
```tsx
// 동적 임포트로 해결
import dynamic from 'next/dynamic'

const Map = dynamic(() => import('@/components/Map'), {
  ssr: false,
  loading: () => <div>지도 로딩 중...</div>
})
```

#### 3. 이미지 최적화 오류
```javascript
// next.config.mjs
const nextConfig = {
  images: {
    unoptimized: true, // 이미지 최적화 비활성화
  },
}
```

#### 4. API 연결 오류
```tsx
// axios 기본 설정
axios.defaults.baseURL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

// 요청 인터셉터
axios.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})
```

## 📚 추가 리소스

### 개발 문서
- **Next.js 문서**: https://nextjs.org/docs
- **shadcn/ui 문서**: https://ui.shadcn.com/
- **Tailwind CSS 문서**: https://tailwindcss.com/docs
- **React Hook Form 문서**: https://react-hook-form.com/

### 컴포넌트 라이브러리
- **Radix UI**: https://www.radix-ui.com/
- **Lucide Icons**: https://lucide.dev/
- **Recharts**: https://recharts.org/
- **Leaflet.js**: https://leafletjs.com/

### 스타일링 도구
- **Tailwind CSS IntelliSense**: VS Code 확장
- **Headless UI**: https://headlessui.com/
- **Class Variance Authority**: https://cva.style/

## 🎯 성능 최적화

### 1. 이미지 최적화
```tsx
import Image from 'next/image'

function OptimizedImage() {
  return (
    <Image
      src="/sports-facility.jpg"
      alt="체육시설"
      width={600}
      height={400}
      placeholder="blur"
      blurDataURL="data:image/jpeg;base64,..."
    />
  )
}
```

### 2. 코드 분할
```tsx
// 동적 임포트로 번들 크기 최적화
const HeavyComponent = dynamic(() => import('@/components/HeavyComponent'), {
  loading: () => <div>로딩 중...</div>
})
```

### 3. 메모이제이션
```tsx
import { memo, useMemo } from 'react'

const ExpensiveComponent = memo(({ data }: { data: any[] }) => {
  const processedData = useMemo(() => {
    return data.filter(item => item.active)
  }, [data])

  return <div>{/* 렌더링 로직 */}</div>
})
```

---

## 🤝 기여하기

### 개발 워크플로우
1. 기능 브랜치 생성: `git checkout -b feature/새로운-기능`
2. 컴포넌트 개발 및 테스트
3. 커밋: `git commit -m "FEAT: 새로운 컴포넌트 추가"`
4. 푸시 및 Pull Request 생성

### 코딩 규칙
- **컴포넌트**: PascalCase (예: `UserProfile.tsx`)
- **파일/폴더**: kebab-case (예: `user-profile/`)
- **함수/변수**: camelCase (예: `handleSubmit`)
- **상수**: UPPER_SNAKE_CASE (예: `API_BASE_URL`)

### 컴포넌트 작성 가이드
```tsx
// 컴포넌트 템플릿
interface ComponentProps {
  title: string
  onAction?: () => void
}

export default function Component({ title, onAction }: ComponentProps) {
  return (
    <div className="p-4">
      <h2 className="text-xl font-semibold">{title}</h2>
      {onAction && (
        <Button onClick={onAction}>액션 실행</Button>
      )}
    </div>
  )
}
```

---

**이제 KSPON 콘테스트 플랫폼의 프론트엔드가 완전히 준비되었습니다!** ⚡

백엔드 API와 연동하여 완전한 풀스택 애플리케이션을 구축할 수 있습니다. 질문이나 문제가 있으시면 언제든 문의해 주세요! 🚀