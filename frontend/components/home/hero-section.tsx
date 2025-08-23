"use client"

import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { ArrowRight, BarChart3, Users, Target, Zap } from "lucide-react"

export function HeroSection() {
  return (
    <section className="relative bg-gradient-to-br from-primary/10 via-background to-accent/10 px-6 py-16">
      <div className="max-w-6xl mx-auto">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          <div className="space-y-6">
            <div className="space-y-2">
              <h1 className="text-4xl lg:text-5xl font-heading font-bold leading-tight">
                <span className="text-primary">스포츠 데이터랩</span>
                <br />
                시민을 위한 체육 정책 대시보드
              </h1>
              <p className="text-xl text-muted-foreground leading-relaxed">
                복잡한 체육 데이터를 쉽게 이해하고, 데이터 기반으로 지역 체육 정책에 대한 의견을 제시할 수 있는 시민
                참여형 플랫폼입니다.
              </p>
            </div>

            <div className="flex flex-wrap gap-4">
              <Button size="lg" className="group">
                대시보드 둘러보기
                <ArrowRight className="ml-2 h-4 w-4 group-hover:translate-x-1 transition-transform" />
              </Button>
              <Button variant="outline" size="lg">
                정책 제안하기
              </Button>
            </div>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 pt-8">
              <div className="text-center">
                <div className="text-2xl font-bold text-primary">15+</div>
                <div className="text-sm text-muted-foreground">공공데이터 API</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-chart-2">247</div>
                <div className="text-sm text-muted-foreground">시민 제안</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-chart-3">89%</div>
                <div className="text-sm text-muted-foreground">데이터 정확도</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-chart-4">12</div>
                <div className="text-sm text-muted-foreground">정책 반영</div>
              </div>
            </div>
          </div>

          <div className="relative">
            <div className="bg-card border rounded-2xl p-6 shadow-2xl">
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <h3 className="font-heading font-semibold">실시간 분석 현황</h3>
                  <Badge variant="outline" className="animate-pulse">
                    LIVE
                  </Badge>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="p-4 bg-primary/10 rounded-lg">
                    <BarChart3 className="h-8 w-8 text-primary mb-2" />
                    <div className="text-sm text-muted-foreground">수요-공급 분석</div>
                    <div className="font-semibold">실시간 업데이트</div>
                  </div>
                  <div className="p-4 bg-chart-2/10 rounded-lg">
                    <Users className="h-8 w-8 text-chart-2 mb-2" />
                    <div className="text-sm text-muted-foreground">시민 참여</div>
                    <div className="font-semibold">활발한 소통</div>
                  </div>
                  <div className="p-4 bg-chart-3/10 rounded-lg">
                    <Target className="h-8 w-8 text-chart-3 mb-2" />
                    <div className="text-sm text-muted-foreground">정책 효과</div>
                    <div className="font-semibold">데이터 기반</div>
                  </div>
                  <div className="p-4 bg-chart-4/10 rounded-lg">
                    <Zap className="h-8 w-8 text-chart-4 mb-2" />
                    <div className="text-sm text-muted-foreground">AI 분석</div>
                    <div className="font-semibold">인사이트 도출</div>
                  </div>
                </div>
              </div>
            </div>

            {/* Floating elements for visual appeal */}
            <div className="absolute -top-4 -right-4 w-20 h-20 bg-primary/20 rounded-full blur-xl"></div>
            <div className="absolute -bottom-4 -left-4 w-16 h-16 bg-accent/20 rounded-full blur-xl"></div>
          </div>
        </div>
      </div>
    </section>
  )
}
