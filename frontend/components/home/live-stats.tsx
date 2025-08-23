"use client"

import { Card, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { TrendingUp, Users, FileText, MessageSquare, Database, Zap } from "lucide-react"

const stats = [
  {
    icon: Database,
    label: "연동된 공공데이터",
    value: "15+",
    unit: "개 API",
    trend: "+3",
    color: "text-primary",
    bgColor: "bg-primary/10",
  },
  {
    icon: Users,
    label: "활성 사용자",
    value: "1,247",
    unit: "명",
    trend: "+89",
    color: "text-chart-2",
    bgColor: "bg-chart-2/10",
  },
  {
    icon: FileText,
    label: "생성된 리포트",
    value: "342",
    unit: "건",
    trend: "+23",
    color: "text-chart-3",
    bgColor: "bg-chart-3/10",
  },
  {
    icon: MessageSquare,
    label: "시민 제안",
    value: "156",
    unit: "건",
    trend: "+12",
    color: "text-chart-4",
    bgColor: "bg-chart-4/10",
  },
  {
    icon: Zap,
    label: "정책 반영",
    value: "28",
    unit: "건",
    trend: "+5",
    color: "text-green-600",
    bgColor: "bg-green-100",
  },
  {
    icon: TrendingUp,
    label: "데이터 정확도",
    value: "94.2",
    unit: "%",
    trend: "+2.1%",
    color: "text-orange-600",
    bgColor: "bg-orange-100",
  },
]

export function LiveStats() {
  return (
    <section className="max-w-6xl mx-auto">
      <div className="text-center mb-8">
        <Badge variant="secondary" className="mb-2 animate-pulse">
          실시간 현황
        </Badge>
        <h2 className="text-2xl font-heading font-bold">플랫폼 활동 현황</h2>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
        {stats.map((stat) => (
          <Card key={stat.label} className="hover:shadow-md transition-shadow">
            <CardContent className="p-4">
              <div className="flex items-center justify-between mb-3">
                <div className={`p-2 rounded-lg ${stat.bgColor}`}>
                  <stat.icon className={`h-4 w-4 ${stat.color}`} />
                </div>
                <Badge variant="outline" className="text-xs">
                  <TrendingUp className="h-3 w-3 mr-1" />
                  {stat.trend}
                </Badge>
              </div>
              <div className="space-y-1">
                <div className="flex items-baseline gap-1">
                  <span className={`text-2xl font-bold ${stat.color}`}>{stat.value}</span>
                  <span className="text-xs text-muted-foreground">{stat.unit}</span>
                </div>
                <div className="text-xs text-muted-foreground leading-tight">{stat.label}</div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </section>
  )
}
