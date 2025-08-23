"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Play, BarChart3, FileText, MessageSquare, ArrowRight } from "lucide-react"

const quickActions = [
  {
    icon: BarChart3,
    title: "대시보드 둘러보기",
    description: "전국 체육시설 현황과 수요-공급 분석을 확인해보세요",
    action: "시작하기",
    link: "/dashboard",
    color: "bg-primary/10 text-primary",
  },
  {
    icon: FileText,
    title: "우리 동네 리포트 생성",
    description: "거주 지역의 체육 환경을 종합 분석한 리포트를 받아보세요",
    action: "리포트 생성",
    link: "/reports",
    color: "bg-chart-2/10 text-chart-2",
  },
  {
    icon: MessageSquare,
    title: "정책 제안하기",
    description: "데이터 근거와 함께 체육 정책 개선 아이디어를 제안해보세요",
    action: "제안하기",
    link: "/proposals",
    color: "bg-chart-3/10 text-chart-3",
  },
]

const userGuide = [
  "지역을 선택하여 체육시설 현황을 확인하세요",
  "수요-공급 분석을 통해 부족한 시설을 파악하세요",
  "데이터 근거와 함께 정책 제안을 작성하세요",
  "다른 시민들의 공감을 받아 정책 반영을 이끌어내세요",
]

export function QuickStart() {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Play className="h-5 w-5" />
          빠른 시작
        </CardTitle>
        <CardDescription>스포츠 데이터랩을 처음 사용하시나요? 주요 기능을 바로 체험해보세요</CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        <div className="space-y-3">
          {quickActions.map((action, index) => (
            <div
              key={index}
              className="flex items-center gap-3 p-3 border rounded-lg hover:shadow-sm transition-shadow"
            >
              <div className={`p-2 rounded-lg ${action.color}`}>
                <action.icon className="h-4 w-4" />
              </div>
              <div className="flex-1 min-w-0">
                <h5 className="font-medium text-sm mb-1">{action.title}</h5>
                <p className="text-xs text-muted-foreground leading-tight">{action.description}</p>
              </div>
              <Button variant="ghost" size="sm" asChild>
                <a href={action.link}>
                  {action.action}
                  <ArrowRight className="ml-1 h-3 w-3" />
                </a>
              </Button>
            </div>
          ))}
        </div>

        <div>
          <h4 className="font-medium mb-3">사용 가이드</h4>
          <div className="space-y-2">
            {userGuide.map((step, index) => (
              <div key={index} className="flex items-start gap-3 text-sm">
                <Badge variant="outline" className="text-xs min-w-fit">
                  {index + 1}
                </Badge>
                <span className="text-muted-foreground leading-relaxed">{step}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="pt-4 border-t">
          <Button className="w-full">전체 가이드 보기</Button>
        </div>
      </CardContent>
    </Card>
  )
}
