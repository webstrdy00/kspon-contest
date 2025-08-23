import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Heart, MessageCircle, Eye, Calendar } from "lucide-react"

const myProposals = [
  {
    id: 1,
    title: "마포구 홍대 인근 실내 클라이밍짐 신설 제안",
    status: "검토중",
    category: "시설 확충",
    likes: 127,
    comments: 23,
    views: 456,
    createdAt: "2024-01-15",
  },
  {
    id: 2,
    title: "서대문구 체육시설 접근성 개선 방안",
    status: "진행중",
    category: "접근성",
    likes: 89,
    comments: 15,
    views: 234,
    createdAt: "2024-01-10",
  },
  {
    id: 3,
    title: "마포구 공원 운동기구 확충 제안",
    status: "완료",
    category: "시설 확충",
    likes: 156,
    comments: 31,
    views: 678,
    createdAt: "2024-01-05",
  },
]

export function MyProposals() {
  const getStatusColor = (status: string) => {
    switch (status) {
      case "완료":
        return "default"
      case "진행중":
        return "secondary"
      case "검토중":
        return "outline"
      default:
        return "outline"
    }
  }

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h3 className="font-heading font-semibold text-lg">내가 작성한 제안</h3>
        <Button>새 제안 작성</Button>
      </div>

      {myProposals.map((proposal) => (
        <Card key={proposal.id} className="hover:shadow-md transition-shadow">
          <CardHeader>
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-2">
                  <Badge variant="outline">{proposal.category}</Badge>
                  <Badge variant={getStatusColor(proposal.status)}>{proposal.status}</Badge>
                </div>
                <CardTitle className="text-lg hover:text-primary transition-colors cursor-pointer">
                  {proposal.title}
                </CardTitle>
                <CardDescription className="flex items-center gap-1 mt-2">
                  <Calendar className="h-4 w-4" />
                  {proposal.createdAt}
                </CardDescription>
              </div>
            </div>
          </CardHeader>
          <CardContent>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-4">
                <div className="flex items-center gap-1 text-sm">
                  <Heart className="h-4 w-4 text-red-500" />
                  {proposal.likes}
                </div>
                <div className="flex items-center gap-1 text-sm">
                  <MessageCircle className="h-4 w-4 text-blue-500" />
                  {proposal.comments}
                </div>
                <div className="flex items-center gap-1 text-sm">
                  <Eye className="h-4 w-4 text-gray-500" />
                  {proposal.views}
                </div>
              </div>
              <div className="flex items-center gap-2">
                <Button variant="outline" size="sm">
                  수정
                </Button>
                <Button variant="ghost" size="sm">
                  삭제
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  )
}
