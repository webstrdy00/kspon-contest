import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Settings, Share2, Calendar, MapPin } from "lucide-react"

export function ProfileHeader() {
  const user = {
    name: "김체육",
    email: "kim@example.com",
    avatar: "",
    joinDate: "2023년 3월",
    location: "서울특별시 마포구",
    badges: ["데이터 전문가", "정책 제안왕", "시민 참여상"],
    stats: {
      proposals: 12,
      likes: 247,
      reports: 5,
      comments: 89,
    },
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="font-heading font-bold text-3xl">내 프로필</h1>
        <div className="flex items-center gap-2">
          <Button variant="outline" size="sm">
            <Share2 className="h-4 w-4 mr-2" />
            프로필 공유
          </Button>
          <Button variant="outline" size="sm">
            <Settings className="h-4 w-4 mr-2" />
            설정
          </Button>
        </div>
      </div>

      <Card>
        <CardContent className="p-6">
          <div className="flex items-start gap-6">
            <Avatar className="h-24 w-24">
              <AvatarImage src={user.avatar || "/placeholder.svg"} alt={user.name} />
              <AvatarFallback className="text-2xl">{user.name.charAt(0)}</AvatarFallback>
            </Avatar>

            <div className="flex-1 space-y-4">
              <div>
                <h2 className="font-heading font-bold text-2xl">{user.name}</h2>
                <p className="text-muted-foreground">{user.email}</p>
                <div className="flex items-center gap-4 mt-2 text-sm text-muted-foreground">
                  <div className="flex items-center gap-1">
                    <Calendar className="h-4 w-4" />
                    {user.joinDate} 가입
                  </div>
                  <div className="flex items-center gap-1">
                    <MapPin className="h-4 w-4" />
                    {user.location}
                  </div>
                </div>
              </div>

              <div className="flex flex-wrap gap-2">
                {user.badges.map((badge) => (
                  <Badge key={badge} variant="secondary">
                    {badge}
                  </Badge>
                ))}
              </div>

              <div className="grid grid-cols-4 gap-4">
                <div className="text-center">
                  <div className="text-2xl font-bold text-primary">{user.stats.proposals}</div>
                  <div className="text-sm text-muted-foreground">작성한 제안</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-chart-2">{user.stats.likes}</div>
                  <div className="text-sm text-muted-foreground">받은 공감</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-chart-4">{user.stats.reports}</div>
                  <div className="text-sm text-muted-foreground">생성한 리포트</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-chart-5">{user.stats.comments}</div>
                  <div className="text-sm text-muted-foreground">작성한 댓글</div>
                </div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
