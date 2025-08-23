"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { MapPin, Filter, Eye, EyeOff, TrendingUp, AlertTriangle, BarChart3 } from "lucide-react"

const facilityTypes = [
  { value: "all", label: "전체 시설", apiCode: "" },
  { value: "swimming", label: "수영장", apiCode: "수영장" },
  { value: "gym", label: "체육관", apiCode: "체육관" },
  { value: "tennis", label: "테니스장", apiCode: "테니스장" },
  { value: "football", label: "축구장", apiCode: "축구장" },
  { value: "baseball", label: "야구장", apiCode: "야구장" },
  { value: "basketball", label: "농구장", apiCode: "농구장" },
  { value: "badminton", label: "배드민턴장", apiCode: "배드민턴장" },
  { value: "golf", label: "골프장", apiCode: "골프장" },
  { value: "park_golf", label: "파크골프장", apiCode: "파크골프장" },
]

const regionsAnalysis = [
  {
    name: "서울특별시",
    facilities: 2847,
    population: 9720846,
    facilityPerCapita: 0.29,
    demand: "high",
    demandScore: 85,
    mismatch: true,
    mismatchType: "supply_shortage",
    topNeeds: ["수영장", "헬스장", "테니스장"],
    budgetEfficiency: 72,
  },
  {
    name: "부산광역시",
    facilities: 1234,
    population: 3349016,
    facilityPerCapita: 0.37,
    demand: "medium",
    demandScore: 68,
    mismatch: false,
    mismatchType: null,
    topNeeds: ["축구장", "농구장", "수영장"],
    budgetEfficiency: 84,
  },
  {
    name: "대구광역시",
    facilities: 987,
    population: 2410700,
    facilityPerCapita: 0.41,
    demand: "high",
    demandScore: 78,
    mismatch: true,
    mismatchType: "demand_excess",
    topNeeds: ["체육관", "배드민턴장", "헬스장"],
    budgetEfficiency: 69,
  },
  {
    name: "인천광역시",
    facilities: 1456,
    population: 2954955,
    facilityPerCapita: 0.49,
    demand: "medium",
    demandScore: 61,
    mismatch: false,
    mismatchType: null,
    topNeeds: ["파크골프장", "테니스장", "수영장"],
    budgetEfficiency: 91,
  },
  {
    name: "광주광역시",
    facilities: 678,
    population: 1441970,
    facilityPerCapita: 0.47,
    demand: "low",
    demandScore: 45,
    mismatch: false,
    mismatchType: null,
    topNeeds: ["체육관", "축구장", "농구장"],
    budgetEfficiency: 88,
  },
  {
    name: "대전광역시",
    facilities: 789,
    population: 1454679,
    facilityPerCapita: 0.54,
    demand: "high",
    demandScore: 82,
    mismatch: true,
    mismatchType: "supply_shortage",
    topNeeds: ["수영장", "헬스장", "골프장"],
    budgetEfficiency: 76,
  },
]

export function SupplyDemandMap() {
  const [selectedFacility, setSelectedFacility] = useState("all")
  const [showDemandLayer, setShowDemandLayer] = useState(true)
  const [showHeatmap, setShowHeatmap] = useState(false)
  const [analysisMode, setAnalysisMode] = useState("mismatch")
  const [selectedRegion, setSelectedRegion] = useState<string | null>(null)

  useEffect(() => {
    // Simulate API call to fetch facility data
    console.log("[v0] Loading facility data for:", selectedFacility)
    // In real implementation, this would call the actual API:
    // https://www.data.go.kr/data/15113986/openapi.do
  }, [selectedFacility])

  const getMismatchColor = (region: any) => {
    if (!region.mismatch) return "bg-green-500"
    return region.mismatchType === "supply_shortage" ? "bg-red-500" : "bg-orange-500"
  }

  const getMismatchLabel = (region: any) => {
    if (!region.mismatch) return "균형"
    return region.mismatchType === "supply_shortage" ? "공급 부족" : "수요 초과"
  }

  return (
    <div className="space-y-6">
      {/* Analysis Mode Tabs */}
      <Tabs value={analysisMode} onValueChange={setAnalysisMode} className="w-full">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="mismatch">수요-공급 분석</TabsTrigger>
          <TabsTrigger value="efficiency">예산 효율성</TabsTrigger>
          <TabsTrigger value="demand">수요 패턴</TabsTrigger>
        </TabsList>

        <TabsContent value="mismatch" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Map Area */}
            <div className="lg:col-span-2">
              <Card>
                <CardHeader>
                  <div className="flex items-center justify-between">
                    <div>
                      <CardTitle className="flex items-center gap-2">
                        <MapPin className="h-5 w-5" />
                        수요-공급 불일치 분석 지도
                      </CardTitle>
                      <CardDescription>
                        전국공공체육시설 API와 한국스포츠과학원 실태조사 데이터를 결합한 분석
                      </CardDescription>
                    </div>
                    <div className="flex gap-2">
                      <Button variant="outline" size="sm" onClick={() => setShowHeatmap(!showHeatmap)}>
                        {showHeatmap ? <EyeOff className="h-4 w-4 mr-2" /> : <Eye className="h-4 w-4 mr-2" />}
                        히트맵
                      </Button>
                      <Button variant="outline" size="sm" onClick={() => setShowDemandLayer(!showDemandLayer)}>
                        {showDemandLayer ? <EyeOff className="h-4 w-4 mr-2" /> : <Eye className="h-4 w-4 mr-2" />}
                        수요 레이어
                      </Button>
                    </div>
                  </div>
                </CardHeader>
                <CardContent>
                  {/* Enhanced Map Placeholder with Leaflet.js integration ready */}
                  <div className="h-96 bg-muted rounded-lg flex items-center justify-center relative overflow-hidden">
                    <div className="absolute inset-0 bg-gradient-to-br from-primary/20 to-accent/20"></div>
                    <div className="relative z-10 text-center">
                      <MapPin className="h-12 w-12 text-primary mx-auto mb-4" />
                      <h3 className="font-heading font-semibold text-lg mb-2">Leaflet.js + VWorld 지도</h3>
                      <p className="text-muted-foreground text-sm">
                        실제 구현: Leaflet.js + 국토교통부 VWorld 타일
                        <br />• 전국공공체육시설 API (좌표 기반 시각화)
                        <br />• 히트맵, 클러스터링, 필터링 지원
                        <br />• 실시간 수요-공급 불일치 분석
                      </p>
                    </div>

                    {/* Enhanced Sample Data Points with clustering simulation */}
                    <div className="absolute top-16 left-16 flex items-center justify-center">
                      <div className="w-8 h-8 bg-red-500/80 rounded-full flex items-center justify-center text-white text-xs font-bold">
                        5
                      </div>
                    </div>
                    <div className="absolute top-24 right-20 flex items-center justify-center">
                      <div className="w-6 h-6 bg-orange-500/80 rounded-full flex items-center justify-center text-white text-xs font-bold">
                        3
                      </div>
                    </div>
                    <div className="absolute bottom-20 left-24 flex items-center justify-center">
                      <div className="w-10 h-10 bg-green-500/80 rounded-full flex items-center justify-center text-white text-xs font-bold">
                        8
                      </div>
                    </div>
                    <div className="absolute bottom-16 right-16 flex items-center justify-center">
                      <div className="w-4 h-4 bg-primary/80 rounded-full"></div>
                    </div>

                    {/* Heatmap overlay simulation */}
                    {showHeatmap && (
                      <div className="absolute inset-4 bg-gradient-radial from-red-500/30 via-orange-500/20 to-transparent rounded-lg"></div>
                    )}
                  </div>

                  {/* Enhanced Legend */}
                  <div className="grid grid-cols-2 gap-4 mt-4 p-4 bg-muted/50 rounded-lg">
                    <div className="space-y-2">
                      <h4 className="font-medium text-sm">시설 분포</h4>
                      <div className="flex items-center gap-2">
                        <div className="w-3 h-3 bg-primary rounded-full"></div>
                        <span className="text-sm">체육시설 위치</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <div className="w-6 h-6 bg-primary/80 rounded-full flex items-center justify-center text-white text-xs">
                          N
                        </div>
                        <span className="text-sm">시설 클러스터</span>
                      </div>
                    </div>
                    <div className="space-y-2">
                      <h4 className="font-medium text-sm">수요-공급 분석</h4>
                      <div className="flex items-center gap-2">
                        <div className="w-3 h-3 bg-red-500 rounded-full"></div>
                        <span className="text-sm">공급 부족 지역</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <div className="w-3 h-3 bg-orange-500 rounded-full"></div>
                        <span className="text-sm">수요 초과 지역</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                        <span className="text-sm">균형 지역</span>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Enhanced Controls and Analysis */}
            <div className="space-y-6">
              {/* Advanced Filters */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Filter className="h-4 w-4" />
                    고급 필터
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <label className="text-sm font-medium mb-2 block">시설 종류</label>
                    <Select value={selectedFacility} onValueChange={setSelectedFacility}>
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        {facilityTypes.map((type) => (
                          <SelectItem key={type.value} value={type.value}>
                            {type.label}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  <div>
                    <label className="text-sm font-medium mb-2 block">분석 레이어</label>
                    <div className="space-y-2">
                      <label className="flex items-center space-x-2">
                        <input
                          type="checkbox"
                          checked={showDemandLayer}
                          onChange={(e) => setShowDemandLayer(e.target.checked)}
                          className="rounded"
                        />
                        <span className="text-sm">수요 데이터 표시</span>
                      </label>
                      <label className="flex items-center space-x-2">
                        <input
                          type="checkbox"
                          checked={showHeatmap}
                          onChange={(e) => setShowHeatmap(e.target.checked)}
                          className="rounded"
                        />
                        <span className="text-sm">히트맵 표시</span>
                      </label>
                      <label className="flex items-center space-x-2">
                        <input type="checkbox" defaultChecked className="rounded" />
                        <span className="text-sm">인구밀도 고려</span>
                      </label>
                      <label className="flex items-center space-x-2">
                        <input type="checkbox" className="rounded" />
                        <span className="text-sm">교통접근성 고려</span>
                      </label>
                    </div>
                  </div>

                  <div>
                    <label className="text-sm font-medium mb-2 block">연령대별 수요</label>
                    <Select defaultValue="all">
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="all">전체 연령</SelectItem>
                        <SelectItem value="youth">청소년 (13-18세)</SelectItem>
                        <SelectItem value="adult">성인 (19-64세)</SelectItem>
                        <SelectItem value="senior">노인 (65세 이상)</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </CardContent>
              </Card>

              {/* Regional Analysis Results */}
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <TrendingUp className="h-4 w-4" />
                    지역별 분석 결과
                  </CardTitle>
                  <CardDescription>수요-공급 불일치 심각도 순으로 정렬</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {regionsAnalysis
                      .sort((a, b) => (b.mismatch ? 1 : 0) - (a.mismatch ? 1 : 0))
                      .map((region) => (
                        <div
                          key={region.name}
                          className={`p-3 border rounded-lg cursor-pointer transition-colors ${
                            selectedRegion === region.name ? "border-primary bg-primary/5" : "hover:bg-muted/50"
                          }`}
                          onClick={() => setSelectedRegion(selectedRegion === region.name ? null : region.name)}
                        >
                          <div className="flex items-center justify-between">
                            <div className="flex-1">
                              <div className="flex items-center gap-2">
                                <div className={`w-3 h-3 rounded-full ${getMismatchColor(region)}`}></div>
                                <span className="font-medium">{region.name}</span>
                                {region.mismatch && <AlertTriangle className="h-4 w-4 text-orange-500" />}
                              </div>
                              <div className="text-sm text-muted-foreground mt-1">
                                시설 {region.facilities.toLocaleString()}개 • 인구 1만명당{" "}
                                {region.facilityPerCapita.toFixed(1)}개
                              </div>
                            </div>
                            <div className="flex flex-col items-end gap-1">
                              <Badge
                                variant={
                                  region.demand === "high"
                                    ? "destructive"
                                    : region.demand === "medium"
                                      ? "default"
                                      : "secondary"
                                }
                              >
                                수요 {region.demandScore}점
                              </Badge>
                              <Badge
                                variant="outline"
                                className={
                                  region.mismatch
                                    ? "text-orange-600 border-orange-600"
                                    : "text-green-600 border-green-600"
                                }
                              >
                                {getMismatchLabel(region)}
                              </Badge>
                            </div>
                          </div>

                          {selectedRegion === region.name && (
                            <div className="mt-3 pt-3 border-t space-y-2">
                              <div>
                                <span className="text-sm font-medium">주요 부족 시설:</span>
                                <div className="flex gap-1 mt-1">
                                  {region.topNeeds.map((need) => (
                                    <Badge key={need} variant="secondary" className="text-xs">
                                      {need}
                                    </Badge>
                                  ))}
                                </div>
                              </div>
                              <div className="text-sm">
                                <span className="font-medium">예산 효율성:</span> {region.budgetEfficiency}점
                              </div>
                            </div>
                          )}
                        </div>
                      ))}
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </TabsContent>

        <TabsContent value="efficiency" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <BarChart3 className="h-5 w-5" />
                예산-성과 효율성 분석
              </CardTitle>
              <CardDescription>국민체육진흥기금 지원실적과 경기력향상성과금 데이터 기반 분석</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="h-64 bg-muted rounded-lg flex items-center justify-center">
                <div className="text-center">
                  <BarChart3 className="h-12 w-12 text-primary mx-auto mb-4" />
                  <h3 className="font-heading font-semibold text-lg mb-2">예산 효율성 차트</h3>
                  <p className="text-muted-foreground text-sm">
                    투입 예산 대비 성과 분석
                    <br />
                    종목별, 지역별 효율성 비교
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="demand" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <TrendingUp className="h-5 w-5" />
                수요 패턴 분석
              </CardTitle>
              <CardDescription>한국스포츠과학원 실태조사 - 필요 체육시설 및 여가시간 데이터 분석</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="h-64 bg-muted rounded-lg flex items-center justify-center">
                <div className="text-center">
                  <TrendingUp className="h-12 w-12 text-primary mx-auto mb-4" />
                  <h3 className="font-heading font-semibold text-lg mb-2">수요 패턴 시각화</h3>
                  <p className="text-muted-foreground text-sm">
                    연령대별, 지역별, 시간대별 수요 분석
                    <br />
                    다차원 교차 분석 결과
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}
