import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Heart, MessageSquare, FileText, Bell, TrendingUp } from "lucide-react"

export function NotificationList() {
  const notifications = [
    {
      id: 1,
      type: "proposal",
      icon: <Heart className="h-5 w-5" />,
      title: "내 제안이 100개의 공감을 받았습니다!",
      description: '"강남구 파크골프장 확충 제안"이 많은 관심을 받고 있습니다.',
      time: "2시간 전",
      isNew: true,
      color: "text-red-500",
    },
    {
      id: 2,
      type: "comment",
      icon: <MessageSquare className="h-5 w-5" />,
      title: "새로운 댓글이 달렸습니다",
      description: '김민수님이 "서초구 체육시설 현황 분석" 제안에 댓글을 남겼습니다.',
      time: "4시간 전",
      isNew: true,
      color: "text-blue-500",
    },
    {
      id: 3,
      type: "report",
      icon: <FileText className="h-5 w-5" />,
      title: "관심 지역 리포트가 업데이트되었습니다",
      description: "강남구의 새로운 체육시설 데이터가 추가되었습니다.",
      time: "6시간 전",
      isNew: false,
      color: "text-green-500",
    },
    {
      id: 4,
      type: "system",
      icon: <Bell className="h-5 w-5" />,
      title: "정책 반영 소식",
      description: '회원님이 제안한 "청소년 체육시설 개선안"이 서울시에서 검토 중입니다.',
      time: "1일 전",
      isNew: false,
      color: "text-purple-500",
    },
    {
      id: 5,
      type: "trending",
      icon: <TrendingUp className="h-5 w-5" />,
      title: "이번 주 인기 제안",
      description: '"생활체육관 운영시간 연장" 제안이 이번 주 가장 많은 공감을 받았습니다.',
      time: "2일 전",
      isNew: false,
      color: "text-orange-500",
    },
  ]

  return (
    <div className="space-y-4">
      {notifications.map((notification) => (
        <Card key={notification.id} className={`${notification.isNew ? "border-cyan-200 bg-cyan-50" : ""}`}>
          <CardContent className="p-4">
            <div className="flex items-start space-x-4">
              <div className={`flex-shrink-0 ${notification.color}`}>{notification.icon}</div>
              <div className="flex-1 min-w-0">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <h3 className="font-semibold text-gray-900 mb-1">
                      {notification.title}
                      {notification.isNew && (
                        <Badge variant="default" className="ml-2 text-xs">
                          새로움
                        </Badge>
                      )}
                    </h3>
                    <p className="text-gray-600 text-sm mb-2">{notification.description}</p>
                    <span className="text-gray-400 text-xs">{notification.time}</span>
                  </div>
                  <Button variant="ghost" size="sm">
                    확인
                  </Button>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      ))}

      <div className="text-center py-8">
        <p className="text-gray-500 mb-4">모든 알림을 확인했습니다</p>
        <Button variant="outline">이전 알림 더보기</Button>
      </div>
    </div>
  )
}
