import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Play, BarChart3, FileText, MessageSquare } from "lucide-react"

export function QuickStart() {
  const steps = [
    {
      icon: <Play className="h-6 w-6" />,
      title: "1. 회원가입 및 지역 설정",
      description: "계정을 만들고 관심 지역을 설정하여 맞춤형 정보를 받아보세요.",
      action: "가입하기",
    },
    {
      icon: <BarChart3 className="h-6 w-6" />,
      title: "2. 대시보드 둘러보기",
      description: "인터랙티브 지도와 차트로 체육시설 현황을 한눈에 파악하세요.",
      action: "대시보드 보기",
    },
    {
      icon: <FileText className="h-6 w-6" />,
      title: "3. 우리 동네 리포트 생성",
      description: "내 지역의 체육 환경을 상세히 분석한 맞춤형 리포트를 만들어보세요.",
      action: "리포트 생성",
    },
    {
      icon: <MessageSquare className="h-6 w-6" />,
      title: "4. 정책 제안하기",
      description: "데이터를 근거로 한 정책 제안을 작성하고 다른 시민들과 소통하세요.",
      action: "제안하기",
    },
  ]

  return (
    <Card>
      <CardHeader>
        <CardTitle>빠른 시작 가이드</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {steps.map((step, index) => (
            <div key={index} className="flex items-start space-x-4 p-4 border rounded-lg">
              <div className="flex-shrink-0 w-12 h-12 bg-cyan-100 rounded-lg flex items-center justify-center text-cyan-600">
                {step.icon}
              </div>
              <div className="flex-1">
                <h3 className="font-semibold mb-2">{step.title}</h3>
                <p className="text-gray-600 text-sm mb-3">{step.description}</p>
                <Button variant="outline" size="sm">
                  {step.action}
                </Button>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}
