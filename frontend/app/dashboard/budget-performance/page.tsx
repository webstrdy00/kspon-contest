"use client"

import { useState } from "react"
import { Header } from "@/components/layout/header"
import { Sidebar } from "@/components/layout/sidebar"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Badge } from "@/components/ui/badge"
import { BudgetPerformanceChart } from "@/components/dashboard/budget-performance-chart"
import { TrendingUp, DollarSign, Trophy, Target } from "lucide-react"

export default function BudgetPerformancePage() {
  const [selectedYear, setSelectedYear] = useState<string>("2023")
  const [selectedSportType, setSelectedSportType] = useState<string>("전체")

  return (
    <div className="min-h-screen bg-background">
      <Header />
      <div className="flex">
        <Sidebar />
        <main className="flex-1 p-6">
          <div className="space-y-6">
            {/* 페이지 헤더 */}
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-3xl font-bold tracking-tight">예산-성과 분석</h1>
                <p className="text-muted-foreground">
                  체육 예산 투입과 경기력 성과의 상관관계를 분석합니다
                </p>
              </div>
              <div className="flex gap-3">
                <Select value={selectedYear} onValueChange={setSelectedYear}>
                  <SelectTrigger className="w-[120px]">
                    <SelectValue placeholder="연도" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="2023">2023년</SelectItem>
                    <SelectItem value="2022">2022년</SelectItem>
                    <SelectItem value="2021">2021년</SelectItem>
                  </SelectContent>
                </Select>
                <Select value={selectedSportType} onValueChange={setSelectedSportType}>
                  <SelectTrigger className="w-[160px]">
                    <SelectValue placeholder="종목 선택" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="전체">전체 종목</SelectItem>
                    <SelectItem value="양궁">양궁</SelectItem>
                    <SelectItem value="태권도">태권도</SelectItem>
                    <SelectItem value="수영">수영</SelectItem>
                    <SelectItem value="골프">골프</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>

            {/* 주요 지표 카드 */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">총 예산 투입액</CardTitle>
                  <DollarSign className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">2,847억원</div>
                  <p className="text-xs text-muted-foreground">
                    전년 대비 <span className="text-green-600">+8.3%</span>
                  </p>
                </CardContent>
              </Card>
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">총 메달 수</CardTitle>
                  <Trophy className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">312개</div>
                  <p className="text-xs text-muted-foreground">
                    전년 대비 <span className="text-green-600">+12.5%</span>
                  </p>
                </CardContent>
              </Card>
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">예산 효율성 지수</CardTitle>
                  <TrendingUp className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">1.24</div>
                  <p className="text-xs text-muted-foreground">
                    <Badge variant="secondary" className="text-xs">우수</Badge>
                  </p>
                </CardContent>
              </Card>
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">최고 효율성 종목</CardTitle>
                  <Target className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">양궁</div>
                  <p className="text-xs text-muted-foreground">
                    효율성 지수 <span className="text-green-600">2.18</span>
                  </p>
                </CardContent>
              </Card>
            </div>

            {/* 예산-성과 분석 차트 */}
            <BudgetPerformanceChart />
          </div>
        </main>
      </div>
    </div>
  )
}