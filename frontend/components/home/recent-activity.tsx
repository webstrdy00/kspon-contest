"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Heart, MessageCircle, FileText, TrendingUp, Clock } from "lucide-react"

const recentProposals = [
  {
    title: "부산 해운대구 해변 운동기구 설치 제안",
    author: "박시민",
    likes: 89,
    comments: 12,
    timeAgo: "2시간 전",
    category: "시설 확충",
    trending: true,
  },
  {
    title: "마포구 홍대 인근 클라이밍짐 신설 제안",
    author: "김체육",
    likes: 67,
    comments: 8,
    timeAgo: "5시간 전",
    category: "시설 확충",
    trending: false,
  },
  {
    title: "강남구 테니스장 이용시간 확대 요청",
    author: "이정책",
    likes: 45,
    comments: 15,
    timeAgo: "1일 전",
    category: "운영 개선",
    trending: false,
  },
]

const recentReports = [
  {
    title: "서울 강남구 체육 환경 종합 리포트",
    downloads: 234,
    timeAgo: "1시간 전",
    type: "지역 분석",
  },
  {
    title: "부산광역시 수영장 수요-공급 분석",
    downloads: 156,
    timeAgo: "3시간 전",
    type: "시설 분석",
  },
  {
    title: "전국 파크골프장 현황 및 개선 방안",
    downloads: 89,
    timeAgo: "6시간 전",
    type: "정책 제안",
  },
]

export function RecentActivity() {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Clock className="h-5 w-5" />
          최근 활동
        </CardTitle>
        <CardDescription>실시간으로 업데이트되는 시민 제안과 리포트 현황</CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        <div>
          <h4 className="font-medium mb-3 flex items-center gap-2">
            <MessageCircle className="h-4 w-4" />
            인기 제안
          </h4>
          <div className="space-y-3">
            {recentProposals.map((proposal, index) => (
              <div
                key={index}
                className="flex items-start gap-3 p-3 border rounded-lg hover:bg-muted/50 transition-colors"
              >
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-1">
                    <Badge variant="outline" className="text-xs">
                      {proposal.category}
                    </Badge>
                    {proposal.trending && (
                      <Badge variant="secondary" className="text-xs">
                        <TrendingUp className="h-3 w-3 mr-1" />
                        인기
                      </Badge>
                    )}
                  </div>
                  <h5 className="font-medium text-sm leading-tight mb-1 truncate">{proposal.title}</h5>
                  <div className="flex items-center gap-4 text-xs text-muted-foreground">
                    <span>by {proposal.author}</span>
                    <span>{proposal.timeAgo}</span>
                  </div>
                </div>
                <div className="flex items-center gap-3 text-xs">
                  <div className="flex items-center gap-1">
                    <Heart className="h-3 w-3 text-red-500" />
                    {proposal.likes}
                  </div>
                  <div className="flex items-center gap-1">
                    <MessageCircle className="h-3 w-3 text-blue-500" />
                    {proposal.comments}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div>
          <h4 className="font-medium mb-3 flex items-center gap-2">
            <FileText className="h-4 w-4" />
            인기 리포트
          </h4>
          <div className="space-y-3">
            {recentReports.map((report, index) => (
              <div
                key={index}
                className="flex items-center justify-between p-3 border rounded-lg hover:bg-muted/50 transition-colors"
              >
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-1">
                    <Badge variant="outline" className="text-xs">
                      {report.type}
                    </Badge>
                  </div>
                  <h5 className="font-medium text-sm leading-tight mb-1 truncate">{report.title}</h5>
                  <div className="text-xs text-muted-foreground">
                    {report.downloads}회 다운로드 • {report.timeAgo}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        <Button variant="outline" className="w-full bg-transparent">
          모든 활동 보기
        </Button>
      </CardContent>
    </Card>
  )
}
