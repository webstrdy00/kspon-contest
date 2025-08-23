import { LoginForm } from "@/components/auth/login-form"

export default function LoginPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-muted/50">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <div className="flex items-center justify-center gap-2 mb-4">
            <div className="h-10 w-10 rounded-lg bg-primary flex items-center justify-center">
              <span className="text-primary-foreground font-heading font-bold">스</span>
            </div>
            <h1 className="font-heading font-bold text-2xl">스포츠 데이터랩</h1>
          </div>
          <p className="text-muted-foreground">시민 참여형 체육 정책 플랫폼에 오신 것을 환영합니다</p>
        </div>
        <LoginForm />
      </div>
    </div>
  )
}
