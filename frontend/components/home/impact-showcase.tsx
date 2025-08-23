"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { CheckCircle, MapPin, Users } from "lucide-react"

export function ImpactShowcase() {
  const successStories = [
    {
      title: "강남구 파크골프장 신설",
      description: "시민 제안을 통해 유휴부지에 파크골프장이 조성되어 월 평균 1,200명이 이용하고 있습니다.",
      impact: "257명 공감",
      status: "정책 반영 완료",
      location: "서울 강남구",
      date: "2024.11",
    },
    {
      title: "부산 해운대 야간 운동시설 확충",
      description: "데이터 분석 결과 야간 운동 수요가 높아 LED 조명과 안전시설을 확충했습니다.",
      impact: "189명 공감",
      status: "시행 중",
      location: "부산 해운대구",
      date: "2024.12",
    },
    {
      title: "대구 수성구 생활체육 프로그램 확대",
      description: "고령자 대상 생활체육 프로그램 부족 문제를 해결하여 참여율이 340% 증가했습니다.",
      impact: "312명 공감",
      status: "정책 반영 완료",
      location: "대구 수성구",
      date: "2024.10",
    },
  ]

  return (
    <section className="py-12 bg-slate-50 rounded-2xl">
      <div className="px-6">
        <div className="text-center mb-8">
          <h2 className="text-3xl font-bold text-foreground mb-4">데이터가 만든 변화</h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            시민들의 데이터 기반 제안이 실제 정책으로 반영된 성공 사례들을 확인해보세요
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          {successStories.map((story, index) => (
            <Card key={index} className="bg-white border-0 shadow-sm hover:shadow-md transition-shadow">
              <CardHeader className="pb-3">
                <div className="flex items-start justify-between mb-2">
                  <Badge variant={story.status === "정책 반영 완료" ? "default" : "secondary"} className="text-xs">
                    <CheckCircle className="h-3 w-3 mr-1" />
                    {story.status}
                  </Badge>
                  <span className="text-xs text-muted-foreground">{story.date}</span>
                </div>
                <CardTitle className="text-lg font-semibold text-foreground leading-tight">{story.title}</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <p className="text-sm text-muted-foreground leading-relaxed">{story.description}</p>
                <div className="flex items-center justify-between text-xs">
                  <div className="flex items-center text-muted-foreground">
                    <MapPin className="h-3 w-3 mr-1" />
                    {story.location}
                  </div>
                  <div className="flex items-center text-orange-600 font-medium">
                    <Users className="h-3 w-3 mr-1" />
                    {story.impact}
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        <div className="text-center">
          <Button variant="outline" size="lg">
            더 많은 성공 사례 보기
          </Button>
        </div>
      </div>
    </section>
  )
}
