import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"

export function PlatformOverview() {
  const metrics = [
    { label: "일일 활성 사용자", value: "2,847", change: "+12%", progress: 78 },
    { label: "월간 활성 사용자", value: "8,234", change: "+8%", progress: 65 },
    { label: "평균 세션 시간", value: "14분 32초", change: "+5%", progress: 82 },
    { label: "사용자 만족도", value: "4.7/5.0", change: "+0.2", progress: 94 },
  ]

  return (
    <Card>
      <CardHeader>
        <CardTitle>플랫폼 개요</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {metrics.map((metric, index) => (
            <div key={index} className="space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">{metric.label}</span>
                <span className="text-sm font-medium text-green-600">{metric.change}</span>
              </div>
              <div className="text-2xl font-bold">{metric.value}</div>
              <Progress value={metric.progress} className="h-2" />
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}
