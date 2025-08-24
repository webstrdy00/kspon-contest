"use client"

import { useState } from "react"
import { Header } from "@/components/layout/header"
import { Sidebar } from "@/components/layout/sidebar"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Badge } from "@/components/ui/badge"
import { SupplyDemandMap } from "@/components/dashboard/supply-demand-map"
import { MapPin, TrendingUp, Users, Building2 } from "lucide-react"

export default function DashboardPage() {
  const [selectedRegion, setSelectedRegion] = useState<string>("전체")
  const [selectedFacilityType, setSelectedFacilityType] = useState<string>("전체")

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
                <h1 className="text-3xl font-bold tracking-tight">인터랙티브 대시보드</h1>
                <p className="text-muted-foreground">
                  전국 체육시설 현황과 수요-공급 분석을 한눈에 확인하세요
                </p>
              </div>
              <div className="flex gap-3">
                <Select value={selectedRegion} onValueChange={setSelectedRegion}>
                  <SelectTrigger className="w-[180px]">
                    <SelectValue placeholder="지역 선택" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="전체">전체 지역</SelectItem>
                    <SelectItem value="11">서울특별시</SelectItem>
                    <SelectItem value="26">부산광역시</SelectItem>
                    <SelectItem value="27">대구광역시</SelectItem>
                  </SelectContent>
                </Select>
                <Select value={selectedFacilityType} onValueChange={setSelectedFacilityType}>
                  <SelectTrigger className="w-[180px]">
                    <SelectValue placeholder="시설 유형" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="전체">전체 시설</SelectItem>
                    <SelectItem value="수영장">수영장</SelectItem>
                    <SelectItem value="체육관">체육관</SelectItem>
                    <SelectItem value="테니스장">테니스장</SelectItem>
                    <SelectItem value="축구장">축구장</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>

            {/* 주요 통계 카드 */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">전체 체육시설</CardTitle>
                  <Building2 className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">12,543</div>
                  <p className="text-xs text-muted-foreground">
                    전월 대비 <span className="text-green-600">+2.1%</span>
                  </p>
                </CardContent>
              </Card>
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">수요-공급 불균형 지역</CardTitle>
                  <TrendingUp className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">47</div>
                  <p className="text-xs text-muted-foreground">
                    <Badge variant="destructive" className="text-xs">주의 필요</Badge>
                  </p>
                </CardContent>
              </Card>
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">이용자 만족도</CardTitle>
                  <Users className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">84.2%</div>
                  <p className="text-xs text-muted-foreground">
                    전년 대비 <span className="text-green-600">+1.8%p</span>
                  </p>
                </CardContent>
              </Card>
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">신규 제안</CardTitle>
                  <MapPin className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">156</div>
                  <p className="text-xs text-muted-foreground">
                    이번 주 등록된 정책 제안
                  </p>
                </CardContent>
              </Card>
            </div>

            {/* 메인 대시보드 탭 */}
            <Tabs defaultValue="supply-demand" className="space-y-4">
              <TabsList className="grid w-full grid-cols-2">
                <TabsTrigger value="supply-demand">수요-공급 분석</TabsTrigger>
                <TabsTrigger value="regional-comparison">지역별 비교</TabsTrigger>
              </TabsList>
              
              <TabsContent value="supply-demand" className="space-y-4">
                <SupplyDemandMap />
              </TabsContent>

              <TabsContent value="regional-comparison" className="space-y-4">
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  <Card>
                    <CardHeader>
                      <CardTitle>지역별 시설 현황</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="h-[300px] bg-muted rounded-lg flex items-center justify-center">
                        <p className="text-muted-foreground">지역별 시설 현황 차트</p>
                      </div>
                    </CardContent>
                  </Card>
                  <Card>
                    <CardHeader>
                      <CardTitle>수요 분석</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="h-[300px] bg-muted rounded-lg flex items-center justify-center">
                        <p className="text-muted-foreground">수요 분석 차트</p>
                      </div>
                    </CardContent>
                  </Card>
                </div>
              </TabsContent>
            </Tabs>
          </div>
        </main>
      </div>
    </div>
  )
}
