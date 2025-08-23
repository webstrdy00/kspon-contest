"use client"

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { BarChart3, Map, TrendingUp, Users } from "lucide-react"

export function DataPreview() {
  return (
    <section className="py-12">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-foreground mb-4">실시간 데이터로 보는 우리나라 체육 현황</h2>
        <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
          15개 공공데이터 API를 통해 수집된 최신 정보를 한눈에 확인하세요
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <Card className="border-l-4 border-l-cyan-500">
          <CardHeader className="pb-3">
            <div className="flex items-center justify-between">
              <CardTitle className="text-sm font-medium text-muted-foreground">전국 공공체육시설</CardTitle>
              <Map className="h-4 w-4 text-cyan-500" />
            </div>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-foreground">24,847개</div>
            <div className="flex items-center mt-2">
              <TrendingUp className="h-3 w-3 text-green-500 mr-1" />
              <span className="text-xs text-green-500">+3.2% 전년 대비</span>
            </div>
          </CardContent>
        </Card>

        <Card className="border-l-4 border-l-orange-500">
          <CardHeader className="pb-3">
            <div className="flex items-center justify-between">
              <CardTitle className="text-sm font-medium text-muted-foreground">체육진흥기금 지원</CardTitle>
              <BarChart3 className="h-4 w-4 text-orange-500" />
            </div>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-foreground">1,247억원</div>
            <div className="flex items-center mt-2">
              <span className="text-xs text-muted-foreground">2024년 총 지원액</span>
            </div>
          </CardContent>
        </Card>

        <Card className="border-l-4 border-l-green-500">
          <CardHeader className="pb-3">
            <div className="flex items-center justify-between">
              <CardTitle className="text-sm font-medium text-muted-foreground">시민 제안 수</CardTitle>
              <Users className="h-4 w-4 text-green-500" />
            </div>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-foreground">3,429개</div>
            <div className="flex items-center mt-2">
              <span className="text-xs text-muted-foreground">이번 달 신규 제안</span>
            </div>
          </CardContent>
        </Card>

        <Card className="border-l-4 border-l-purple-500">
          <CardHeader className="pb-3">
            <div className="flex items-center justify-between">
              <CardTitle className="text-sm font-medium text-muted-foreground">정책 반영률</CardTitle>
              <TrendingUp className="h-4 w-4 text-purple-500" />
            </div>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-foreground">23.7%</div>
            <div className="flex items-center mt-2">
              <Badge variant="secondary" className="text-xs">
                전국 평균 대비 +8.2%
              </Badge>
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="text-center">
        <Button size="lg" className="bg-cyan-600 hover:bg-cyan-700">
          전체 데이터 대시보드 보기
        </Button>
      </div>
    </section>
  )
}
