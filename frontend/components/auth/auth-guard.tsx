"use client"

import { useEffect } from "react"
import { useRouter } from "next/navigation"
import { useAuth } from "@/contexts/AuthContext"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { AlertCircle, Lock, LogIn } from "lucide-react"

interface AuthGuardProps {
  children: React.ReactNode
  requireAuth?: boolean
  requireAdmin?: boolean
  fallback?: React.ReactNode
  redirectTo?: string
}

export function AuthGuard({ 
  children, 
  requireAuth = true, 
  requireAdmin = false, 
  fallback,
  redirectTo 
}: AuthGuardProps) {
  const { user, isAuthenticated, isLoading } = useAuth()
  const router = useRouter()

  useEffect(() => {
    if (!isLoading && requireAuth && !isAuthenticated && redirectTo) {
      router.push(redirectTo)
    }
  }, [isLoading, requireAuth, isAuthenticated, redirectTo, router])

  // 로딩 중
  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <div className="text-center">
          <div className="w-8 h-8 border-4 border-primary border-t-transparent rounded-full animate-spin mx-auto mb-4" />
          <p className="text-muted-foreground">로딩 중...</p>
        </div>
      </div>
    )
  }

  // 인증이 필요하지만 로그인하지 않은 경우
  if (requireAuth && !isAuthenticated) {
    if (fallback) {
      return <>{fallback}</>
    }

    return (
      <div className="flex items-center justify-center min-h-[400px] p-4">
        <Card className="w-full max-w-md">
          <CardHeader className="text-center">
            <div className="w-12 h-12 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-4">
              <Lock className="h-6 w-6 text-primary" />
            </div>
            <CardTitle>로그인이 필요합니다</CardTitle>
          </CardHeader>
          <CardContent className="text-center space-y-4">
            <Alert>
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>
                이 페이지에 접근하려면 로그인이 필요합니다.
              </AlertDescription>
            </Alert>
            <div className="flex gap-2 justify-center">
              <Button asChild>
                <a href="/auth/login">
                  <LogIn className="mr-2 h-4 w-4" />
                  로그인
                </a>
              </Button>
              <Button variant="outline" asChild>
                <a href="/auth/register">회원가입</a>
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    )
  }

  // 관리자 권한이 필요하지만 일반 사용자인 경우
  if (requireAdmin && user?.role !== 'admin') {
    if (fallback) {
      return <>{fallback}</>
    }

    return (
      <div className="flex items-center justify-center min-h-[400px] p-4">
        <Card className="w-full max-w-md">
          <CardHeader className="text-center">
            <div className="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <AlertCircle className="h-6 w-6 text-red-600" />
            </div>
            <CardTitle>접근 권한이 없습니다</CardTitle>
          </CardHeader>
          <CardContent className="text-center space-y-4">
            <Alert variant="destructive">
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>
                이 페이지는 관리자만 접근할 수 있습니다.
              </AlertDescription>
            </Alert>
            <Button variant="outline" onClick={() => router.back()}>
              이전 페이지로 돌아가기
            </Button>
          </CardContent>
        </Card>
      </div>
    )
  }

  // 모든 조건을 만족하는 경우 자식 컴포넌트 렌더링
  return <>{children}</>
}