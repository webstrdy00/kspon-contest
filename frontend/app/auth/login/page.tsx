"use client"

import { useState } from "react"
import Link from "next/link"
import { useRouter } from "next/navigation"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Separator } from "@/components/ui/separator"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { useAuth } from "@/contexts/AuthContext"
import { Eye, EyeOff, LogIn, AlertCircle, Loader2 } from "lucide-react"

export default function LoginPage() {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [showPassword, setShowPassword] = useState(false)
  const [rememberMe, setRememberMe] = useState(false)
  const [error, setError] = useState("")
  const [isSubmitting, setIsSubmitting] = useState(false)
  
  const { login } = useAuth()
  const router = useRouter()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError("")
    setIsSubmitting(true)

    try {
      const result = await login(email, password)
      
      if (result.success) {
        router.push("/dashboard")
        router.refresh()
      } else {
        setError(result.error || "로그인에 실패했습니다.")
      }
    } catch (error) {
      setError("로그인 중 오류가 발생했습니다.")
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div className="space-y-6">
      {/* 브랜드 헤더 */}
      <div className="text-center">
        <div className="flex items-center justify-center gap-2 mb-4">
          <div className="h-12 w-12 rounded-lg bg-primary flex items-center justify-center">
            <span className="text-primary-foreground font-bold text-lg">스</span>
          </div>
          <h1 className="font-bold text-2xl">스포츠 데이터랩</h1>
        </div>
        <p className="text-muted-foreground">시민 참여형 체육 정책 플랫폼에 오신 것을 환영합니다</p>
      </div>

      <Card className="shadow-lg">
        <CardHeader className="space-y-1 text-center">
          <CardTitle className="text-2xl font-bold">로그인</CardTitle>
          <CardDescription>
            계정으로 로그인하여 더 많은 기능을 이용하세요
          </CardDescription>
        </CardHeader>
        
        <form onSubmit={handleSubmit}>
          <CardContent className="space-y-4">
            {error && (
              <Alert variant="destructive">
                <AlertCircle className="h-4 w-4" />
                <AlertDescription>{error}</AlertDescription>
              </Alert>
            )}

            <div className="space-y-2">
              <Label htmlFor="email">이메일</Label>
              <Input
                id="email"
                type="email"
                placeholder="your@email.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                disabled={isSubmitting}
              />
            </div>
            
            <div className="space-y-2">
              <Label htmlFor="password">비밀번호</Label>
              <div className="relative">
                <Input
                  id="password"
                  type={showPassword ? "text" : "password"}
                  placeholder="비밀번호를 입력하세요"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  disabled={isSubmitting}
                  className="pr-10"
                />
                <Button
                  type="button"
                  variant="ghost"
                  size="sm"
                  className="absolute right-0 top-0 h-full px-3 py-2 hover:bg-transparent"
                  onClick={() => setShowPassword(!showPassword)}
                  disabled={isSubmitting}
                >
                  {showPassword ? (
                    <EyeOff className="h-4 w-4 text-muted-foreground" />
                  ) : (
                    <Eye className="h-4 w-4 text-muted-foreground" />
                  )}
                </Button>
              </div>
            </div>

            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-2">
                <input
                  id="remember"
                  type="checkbox"
                  checked={rememberMe}
                  onChange={(e) => setRememberMe(e.target.checked)}
                  className="rounded border-gray-300"
                  disabled={isSubmitting}
                />
                <Label htmlFor="remember" className="text-sm text-muted-foreground cursor-pointer">
                  로그인 상태 유지
                </Label>
              </div>
              <Link 
                href="/auth/forgot-password" 
                className="text-sm text-primary hover:underline"
              >
                비밀번호 찾기
              </Link>
            </div>
          </CardContent>

          <CardFooter className="flex flex-col space-y-4">
            <Button type="submit" className="w-full" disabled={isSubmitting}>
              {isSubmitting ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  로그인 중...
                </>
              ) : (
                <>
                  <LogIn className="mr-2 h-4 w-4" />
                  로그인
                </>
              )}
            </Button>
            
            <div className="text-center text-sm text-muted-foreground">
              계정이 없으신가요?{" "}
              <Link href="/auth/register" className="text-primary hover:underline">
                회원가입
              </Link>
            </div>

            <div className="relative">
              <div className="absolute inset-0 flex items-center">
                <Separator className="w-full" />
              </div>
              <div className="relative flex justify-center text-xs uppercase">
                <span className="bg-background px-2 text-muted-foreground">
                  데모 계정
                </span>
              </div>
            </div>

            <div className="space-y-2 text-xs text-muted-foreground">
              <div className="bg-muted p-3 rounded-md">
                <p className="font-medium mb-1">테스트 계정:</p>
                <p>이메일: test@example.com</p>
                <p>비밀번호: password123</p>
              </div>
              <div className="bg-muted p-3 rounded-md">
                <p className="font-medium mb-1">관리자 계정:</p>
                <p>이메일: admin@example.com</p>
                <p>비밀번호: admin123</p>
              </div>
            </div>
          </CardFooter>
        </form>
      </Card>
    </div>
  )
}
