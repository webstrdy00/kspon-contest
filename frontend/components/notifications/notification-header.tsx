import { Bell, Settings } from "lucide-react"
import { Button } from "@/components/ui/button"

export function NotificationHeader() {
  return (
    <div className="bg-white border-b">
      <div className="max-w-4xl mx-auto p-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <Bell className="h-8 w-8 text-cyan-600" />
            <div>
              <h1 className="text-3xl font-bold text-gray-900">알림</h1>
              <p className="text-gray-600">중요한 업데이트와 활동 소식을 확인하세요</p>
            </div>
          </div>
          <Button variant="outline" size="sm">
            <Settings className="h-4 w-4 mr-2" />
            알림 설정
          </Button>
        </div>
      </div>
    </div>
  )
}
