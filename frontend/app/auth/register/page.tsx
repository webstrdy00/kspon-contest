import { RegisterForm } from "@/components/auth/register-form"

export default function RegisterPage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-cyan-50 to-orange-50 p-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">스포츠 데이터랩 가입</h1>
          <p className="text-gray-600">데이터 기반 체육 정책에 참여하세요</p>
        </div>
        <RegisterForm />
      </div>
    </div>
  )
}
