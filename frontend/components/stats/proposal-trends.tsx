import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"

export function ProposalTrends() {
  const trendingTopics = [
    { topic: "파크골프장 확충", proposals: 89, trend: "up" },
    { topic: "생활체육관 운영시간 연장", proposals: 67, trend: "up" },
    { topic: "청소년 체육시설 개선", proposals: 54, trend: "stable" },
    { topic: "장애인 체육시설 접근성", proposals: 43, trend: "up" },
    { topic: "체육예산 투명성", proposals: 38, trend: "down" },
  ]

  return (
    <Card>
      <CardHeader>
        <CardTitle>제안 트렌드</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {trendingTopics.map((item, index) => (
            <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div className="flex items-center space-x-3">
                <span className="text-lg font-bold text-gray-400">#{index + 1}</span>
                <div>
                  <p className="font-medium">{item.topic}</p>
                  <p className="text-sm text-gray-600">{item.proposals}개 제안</p>
                </div>
              </div>
              <Badge variant={item.trend === "up" ? "default" : item.trend === "down" ? "destructive" : "secondary"}>
                {item.trend === "up" ? "↗️ 상승" : item.trend === "down" ? "↘️ 하락" : "→ 유지"}
              </Badge>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}
