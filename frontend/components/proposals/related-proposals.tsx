import { Card, CardContent, CardHeader } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Heart, MessageCircle, TrendingUp } from "lucide-react"

interface RelatedProposalsProps {
  proposalId: string
}

export function RelatedProposals({ proposalId }: RelatedProposalsProps) {
  const relatedProposals = [
    {
      id: "2",
      title: "서초구 반포동 테니스장 확충 제안",
      author: "테니스매니아",
      likes: 189,
      comments: 23,
      category: "체육시설",
      region: "서초구",
      trend: "상승",
    },
    {
      id: "3",
      title: "송파구 잠실 수영장 운영시간 연장 건의",
      author: "수영사랑",
      likes: 156,
      comments: 18,
      category: "운영개선",
      region: "송파구",
      trend: "상승",
    },
    {
      id: "4",
      title: "마포구 생활체육 프로그램 다양화 제안",
      author: "건강지킴이",
      likes: 134,
      comments: 15,
      category: "프로그램",
      region: "마포구",
      trend: "보통",
    },
  ]

  return (
    <div className="space-y-6">
      {/* 관련 제안 */}
      <Card>
        <CardHeader>
          <h3 className="font-heading font-semibold">관련 제안</h3>
        </CardHeader>
        <CardContent className="space-y-4">
          {relatedProposals.map((proposal) => (
            <div key={proposal.id} className="p-3 rounded-lg border hover:bg-muted/50 cursor-pointer transition-colors">
              <div className="space-y-2">
                <div className="flex items-start gap-2">
                  <h4 className="font-medium text-sm leading-tight flex-1">{proposal.title}</h4>
                  {proposal.trend === "상승" && <TrendingUp className="h-4 w-4 text-green-500 flex-shrink-0" />}
                </div>

                <div className="flex items-center gap-2">
                  <Badge variant="secondary" className="text-xs">
                    {proposal.category}
                  </Badge>
                  <Badge variant="outline" className="text-xs">
                    {proposal.region}
                  </Badge>
                </div>

                <div className="flex items-center justify-between text-xs text-muted-foreground">
                  <span>by {proposal.author}</span>
                  <div className="flex items-center gap-3">
                    <div className="flex items-center gap-1">
                      <Heart className="h-3 w-3" />
                      {proposal.likes}
                    </div>
                    <div className="flex items-center gap-1">
                      <MessageCircle className="h-3 w-3" />
                      {proposal.comments}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </CardContent>
      </Card>

      {/* 제안 통계 */}
      <Card>
        <CardHeader>
          <h3 className="font-heading font-semibold">이 제안의 영향력</h3>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-3">
            <div className="flex justify-between items-center">
              <span className="text-sm">공감도</span>
              <span className="font-medium">상위 15%</span>
            </div>
            <div className="w-full bg-muted rounded-full h-2">
              <div className="bg-primary h-2 rounded-full" style={{ width: "85%" }}></div>
            </div>
          </div>

          <div className="space-y-3">
            <div className="flex justify-between items-center">
              <span className="text-sm">토론 활성도</span>
              <span className="font-medium">상위 25%</span>
            </div>
            <div className="w-full bg-muted rounded-full h-2">
              <div className="bg-secondary h-2 rounded-full" style={{ width: "75%" }}></div>
            </div>
          </div>

          <div className="pt-2 text-xs text-muted-foreground">
            이 제안은 높은 관심을 받고 있으며, 정책 반영 가능성이 높습니다.
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
