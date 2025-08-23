"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { MapPin, FileText, MessageSquare, BarChart3, ArrowRight, Sparkles } from "lucide-react"

const features = [
  {
    icon: BarChart3,
    title: "인터랙티브 대시보드",
    description: "전국공공체육시설 API와 수요 데이터를 결합한 수요-공급 불일치 분석",
    highlights: ["실시간 지도 시각화", "히트맵 & 클러스터링", "예산-성과 효율성 분석"],
    status: "실시간 업데이트",
    link: "/dashboard",
  },
  {
    icon: FileText,
    title: "우리 동네 리포트",
    description: "지역별 체육 환경을 종합 분석한 맞춤형 리포트 자동 생성",
    highlights: ["AI 기반 분석", "전국 평균 비교", "PDF 다운로드"],
    status: "AI 분석 포함",
    link: "/reports",
  },
  {
    icon: MessageSquare,
    title: "시민 정책 제안",
    description: "데이터 근거와 함께 정책을 제안하고 시민들의 공감을 얻는 소통 플랫폼",
    highlights: ["데이터 기반 제안", "공감 랭킹 시스템", "배지 & 레벨 시스템"],
    status: "게이미피케이션",
    link: "/proposals",
  },
  {
    icon: MapPin,
    title: "지역별 비교 분석",
    description: "유사 지역, 인접 지역, 벤치마크 지역과의 다차원 비교 분석",
    highlights: ["벤치마크 분석", "개선 잠재력 측정", "성공 사례 학습"],
    status: "심층 분석",
    link: "/reports",
  },
]

export function FeaturesOverview() {
  return (
    <section className="max-w-6xl mx-auto">
      <div className="text-center mb-12">
        <Badge variant="secondary" className="mb-4">
          핵심 기능
        </Badge>
        <h2 className="text-3xl font-heading font-bold mb-4">
          데이터 기반 정책 결정을 위한 <span className="text-primary">통합 플랫폼</span>
        </h2>
        <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
          복잡한 공공데이터를 시민이 쉽게 이해할 수 있도록 시각화하고, 집단지성을 통해 더 나은 정책을 만들어갑니다.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {features.map((feature, index) => (
          <Card key={feature.title} className="group hover:shadow-lg transition-all duration-300 hover:-translate-y-1">
            <CardHeader>
              <div className="flex items-start justify-between">
                <div className="flex items-center gap-3">
                  <div className="p-2 bg-primary/10 rounded-lg group-hover:bg-primary/20 transition-colors">
                    <feature.icon className="h-6 w-6 text-primary" />
                  </div>
                  <div>
                    <CardTitle className="text-lg">{feature.title}</CardTitle>
                    <Badge variant="outline" className="mt-1 text-xs">
                      <Sparkles className="h-3 w-3 mr-1" />
                      {feature.status}
                    </Badge>
                  </div>
                </div>
              </div>
              <CardDescription className="text-base leading-relaxed">{feature.description}</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div>
                  <h4 className="font-medium text-sm mb-2">주요 특징</h4>
                  <div className="space-y-1">
                    {feature.highlights.map((highlight) => (
                      <div key={highlight} className="flex items-center gap-2 text-sm text-muted-foreground">
                        <div className="w-1.5 h-1.5 bg-primary rounded-full"></div>
                        {highlight}
                      </div>
                    ))}
                  </div>
                </div>
                <Button variant="ghost" className="w-full group/btn" asChild>
                  <a href={feature.link}>
                    자세히 보기
                    <ArrowRight className="ml-2 h-4 w-4 group-hover/btn:translate-x-1 transition-transform" />
                  </a>
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </section>
  )
}
