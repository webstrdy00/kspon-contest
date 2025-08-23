import { BarChart3, TrendingUp, Users, FileText } from "lucide-react"

export function StatsHeader() {
  return (
    <div className="bg-white border-b">
      <div className="max-w-7xl mx-auto p-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">플랫폼 통계</h1>
            <p className="text-gray-600 mt-2">스포츠 데이터랩의 활동 현황과 트렌드를 확인하세요</p>
          </div>
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2 text-cyan-600">
              <BarChart3 className="h-5 w-5" />
              <span className="font-medium">실시간 업데이트</span>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mt-8">
          <div className="bg-gradient-to-r from-cyan-500 to-cyan-600 rounded-lg p-6 text-white">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-cyan-100">총 사용자</p>
                <p className="text-3xl font-bold">12,847</p>
              </div>
              <Users className="h-8 w-8 text-cyan-200" />
            </div>
            <p className="text-cyan-100 text-sm mt-2">+234 (이번 주)</p>
          </div>

          <div className="bg-gradient-to-r from-orange-500 to-orange-600 rounded-lg p-6 text-white">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-orange-100">총 제안</p>
                <p className="text-3xl font-bold">3,421</p>
              </div>
              <FileText className="h-8 w-8 text-orange-200" />
            </div>
            <p className="text-orange-100 text-sm mt-2">+89 (이번 주)</p>
          </div>

          <div className="bg-gradient-to-r from-green-500 to-green-600 rounded-lg p-6 text-white">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-green-100">생성된 리포트</p>
                <p className="text-3xl font-bold">8,756</p>
              </div>
              <BarChart3 className="h-8 w-8 text-green-200" />
            </div>
            <p className="text-green-100 text-sm mt-2">+156 (이번 주)</p>
          </div>

          <div className="bg-gradient-to-r from-purple-500 to-purple-600 rounded-lg p-6 text-white">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-purple-100">정책 반영</p>
                <p className="text-3xl font-bold">47</p>
              </div>
              <TrendingUp className="h-8 w-8 text-purple-200" />
            </div>
            <p className="text-purple-100 text-sm mt-2">+3 (이번 달)</p>
          </div>
        </div>
      </div>
    </div>
  )
}
