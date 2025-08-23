import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Heart, MessageCircle, FileText, Award, Calendar } from "lucide-react"

const activities = [
  {
    id: 1,
    type: "like",
    title: "부산 해운대구 해변 운동기구 설치 제안",
    author: "박시민",
    timestamp: "2시간 전",
  },
  {
    id: 2,
    type: "comment",
    title: "강남구 테니스장 이용 시간 확대 요청",
    author: "이정책",
    timestamp: "5시간 전",
  },
  {
    id: 3,
    type: "report",
    title: "서울특별시 마포구 체육 환경 종합 리포트",
    timestamp: "1일 전",
  },
  {
    id: 4,
    type: "badge",
    title: "데이터 전문가 배지 획득",
    timestamp: "3일 전",
  },
]

export function MyActivity() {
  const getActivityIcon = (type: string) => {
    switch (type) {
      case "like":
        return <Heart className="h-4 w-4 text-red-500" />
      case "comment":
        return <MessageCircle className="h-4 w-4 text-blue-500" />
      case "report":
        return <FileText className="h-4 w-4 text-green-500" />
      case "badge":
        return <Award className="h-4 w-4 text-yellow-500" />
      default:
        return <Calendar className="h-4 w-4" />
    }
  }

  const getActivityText = (type: string) => {
    switch (type) {
      case "like":
        return "공감을 표시했습니다"
      case "comment":
        return "댓글을 작성했습니다"
      case "report":
        return "리포트를 생성했습니다"
      case "badge":
        return "배지를 획득했습니다"
      default:
        return "활동했습니다"
    }
  }

  return (
    <div className="space-y-4">
      <h3 className="font-heading font-semibold text-lg">최근 활동</h3>

      <div className="space-y-3">
        {activities.map((activity) => (
          <Card key={activity.id}>
            <CardContent className="p-4">
              <div className="flex items-start gap-3">
                <div className="mt-1">{getActivityIcon(activity.type)}</div>
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-sm font-medium">{getActivityText(activity.type)}</span>
                    <Badge variant="outline" className="text-xs">
                      {activity.timestamp}
                    </Badge>
                  </div>
                  <p className="text-sm text-muted-foreground">{activity.title}</p>
                  {activity.author && <p className="text-xs text-muted-foreground mt-1">by {activity.author}</p>}
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}
