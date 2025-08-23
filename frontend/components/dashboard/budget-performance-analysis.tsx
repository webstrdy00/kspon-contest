"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { TrendingUp, TrendingDown, DollarSign, Trophy, Target, AlertTriangle, Database, Users } from "lucide-react"

const sportsData = [
  {
    sport: "양궁",
    budget: 120,
    performance: 95,
    efficiency: "excellent",
    medals: 8,
    supportInstitutions: ["대한양궁협회", "서울시체육회"],
    budgetDetails: { equipment: 40, training: 50, competition: 30 },
    performanceMetrics: { worldRanking: 1, domesticParticipation: 2500 },
  },
  {
    sport: "태권도",
    budget: 180,
    performance: 87,
    efficiency: "good",
    medals: 6,
    supportInstitutions: ["대한태권도협회", "부산시체육회"],
    budgetDetails: { equipment: 60, training: 80, competition: 40 },
    performanceMetrics: { worldRanking: 2, domesticParticipation: 4200 },
  },
  {
    sport: "수영",
    budget: 250,
    performance: 72,
    efficiency: "average",
    medals: 4,
    supportInstitutions: ["대한수영연맹", "인천시체육회"],
    budgetDetails: { equipment: 100, training: 90, competition: 60 },
    performanceMetrics: { worldRanking: 8, domesticParticipation: 3800 },
  },
  {
    sport: "축구",
    budget: 320,
    performance: 65,
    efficiency: "below",
    medals: 2,
    supportInstitutions: ["대한축구협회", "경기도체육회"],
    budgetDetails: { equipment: 80, training: 140, competition: 100 },
    performanceMetrics: { worldRanking: 23, domesticParticipation: 15000 },
  },
  {
    sport: "농구",
    budget: 150,
    performance: 78,
    efficiency: "good",
    medals: 3,
    supportInstitutions: ["대한농구협회", "대구시체육회"],
    budgetDetails: { equipment: 50, training: 70, competition: 30 },
    performanceMetrics: { worldRanking: 12, domesticParticipation: 5600 },
  },
  {
    sport: "배구",
    budget: 140,
    performance: 82,
    efficiency: "good",
    medals: 5,
    supportInstitutions: ["대한배구협회", "광주시체육회"],
    budgetDetails: { equipment: 45, training: 65, competition: 30 },
    performanceMetrics: { worldRanking: 6, domesticParticipation: 3200 },
  },
]

const institutionRegionMapping = [
  { institution: "대한양궁협회", estimatedRegion: "서울", confidence: "high" },
  { institution: "대한태권도협회", estimatedRegion: "부산", confidence: "medium" },
  { institution: "대한수영연맹", estimatedRegion: "인천", confidence: "high" },
  { institution: "대한축구협회", estimatedRegion: "경기", confidence: "high" },
  { institution: "대한농구협회", estimatedRegion: "대구", confidence: "medium" },
  { institution: "대한배구협회", estimatedRegion: "광주", confidence: "medium" },
]

const regionData = [
  {
    region: "서울",
    budget: 450,
    performance: 88,
    trend: "up",
    institutions: 12,
    dataCompleteness: 85,
    citizenContributions: 23,
  },
  {
    region: "부산",
    budget: 280,
    performance: 76,
    trend: "up",
    institutions: 8,
    dataCompleteness: 72,
    citizenContributions: 15,
  },
  {
    region: "대구",
    budget: 220,
    performance: 82,
    trend: "down",
    institutions: 6,
    dataCompleteness: 68,
    citizenContributions: 11,
  },
  {
    region: "인천",
    budget: 190,
    performance: 74,
    trend: "up",
    institutions: 5,
    dataCompleteness: 79,
    citizenContributions: 18,
  },
  {
    region: "광주",
    budget: 160,
    performance: 79,
    trend: "stable",
    institutions: 4,
    dataCompleteness: 63,
    citizenContributions: 9,
  },
  {
    region: "대전",
    budget: 180,
    performance: 85,
    trend: "up",
    institutions: 5,
    dataCompleteness: 74,
    citizenContributions: 12,
  },
]

export function BudgetPerformanceAnalysis() {
  const [analysisType, setAnalysisType] = useState("efficiency")
  const [selectedSport, setSelectedSport] = useState<string | null>(null)
  const [showDataLimitations, setShowDataLimitations] = useState(true)

  return (
    <div className="space-y-6">
      {showDataLimitations && (
        <Alert>
          <AlertTriangle className="h-4 w-4" />
          <AlertDescription>
            <strong>데이터 한계 안내:</strong> 현재 지역별 성과 분석은 기관명 기반 추정 데이터를 사용합니다. 더 정확한
            분석을 위해{" "}
            <Button variant="link" className="p-0 h-auto text-primary">
              시민 데이터 기여
            </Button>
            에 참여해주세요.
            <Button variant="ghost" size="sm" className="ml-2" onClick={() => setShowDataLimitations(false)}>
              닫기
            </Button>
          </AlertDescription>
        </Alert>
      )}

      {/* Enhanced Analysis Controls */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-base">분석 기준</CardTitle>
          </CardHeader>
          <CardContent>
            <Select value={analysisType} onValueChange={setAnalysisType}>
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="efficiency">예산 효율성</SelectItem>
                <SelectItem value="performance">성과 지표</SelectItem>
                <SelectItem value="roi">투자 수익률</SelectItem>
                <SelectItem value="participation">참여도 대비 성과</SelectItem>
              </SelectContent>
            </Select>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-base">기간 설정</CardTitle>
          </CardHeader>
          <CardContent>
            <Select defaultValue="2024">
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="2024">2024년</SelectItem>
                <SelectItem value="2023">2023년</SelectItem>
                <SelectItem value="2022">2022년</SelectItem>
                <SelectItem value="multi">다년도 비교</SelectItem>
              </SelectContent>
            </Select>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-base">비교 대상</CardTitle>
          </CardHeader>
          <CardContent>
            <Select defaultValue="sports">
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="sports">종목별 비교</SelectItem>
                <SelectItem value="regions">지역별 비교</SelectItem>
                <SelectItem value="institutions">기관별 비교</SelectItem>
                <SelectItem value="budget_categories">예산 항목별</SelectItem>
              </SelectContent>
            </Select>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="pb-3">
            <CardTitle className="text-base flex items-center gap-2">
              <Database className="h-4 w-4" />
              데이터 품질
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-1">
              <div className="flex justify-between text-sm">
                <span>완성도</span>
                <span className="font-medium">74%</span>
              </div>
              <div className="w-full bg-muted rounded-full h-2">
                <div className="bg-primary h-2 rounded-full" style={{ width: "74%" }}></div>
              </div>
              <div className="text-xs text-muted-foreground">시민 기여: 88건</div>
            </div>
          </CardContent>
        </Card>
      </div>

      <Tabs defaultValue="analysis" className="w-full">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="analysis">효율성 분석</TabsTrigger>
          <TabsTrigger value="mapping">매핑 테이블</TabsTrigger>
          <TabsTrigger value="crowdsource">집단지성 보완</TabsTrigger>
          <TabsTrigger value="insights">인사이트</TabsTrigger>
        </TabsList>

        <TabsContent value="analysis" className="space-y-6">
          {/* Enhanced Performance Scatter Plot */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Target className="h-5 w-5" />
                투입 대비 산출 효율성 분석
              </CardTitle>
              <CardDescription>
                국민체육진흥기금 지원실적 vs 경기력향상성과금 데이터 기반 - 좌상단이 가장 효율적인 영역
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="h-80 bg-muted rounded-lg flex items-center justify-center relative overflow-hidden">
                <div className="absolute inset-0 bg-gradient-to-tr from-primary/10 to-accent/10"></div>

                {/* Enhanced Scatter Plot with detailed tooltips */}
                <div className="relative w-full h-full p-8">
                  {sportsData.map((item, index) => (
                    <div
                      key={item.sport}
                      className={`absolute w-4 h-4 rounded-full cursor-pointer hover:scale-150 transition-all duration-200 ${
                        selectedSport === item.sport ? "ring-2 ring-primary ring-offset-2" : ""
                      }`}
                      style={{
                        left: `${(item.budget / 400) * 80 + 10}%`,
                        bottom: `${(item.performance / 100) * 70 + 15}%`,
                        backgroundColor:
                          item.efficiency === "excellent"
                            ? "#0891b2"
                            : item.efficiency === "good"
                              ? "#f97316"
                              : item.efficiency === "average"
                                ? "#4b5563"
                                : "#dc2626",
                      }}
                      onClick={() => setSelectedSport(selectedSport === item.sport ? null : item.sport)}
                      title={`${item.sport}: ${item.budget}억원, ${item.performance}점, 메달 ${item.medals}개`}
                    />
                  ))}

                  {/* Efficiency zones overlay */}
                  <div className="absolute inset-8 pointer-events-none">
                    <div className="absolute top-0 left-0 w-1/2 h-1/2 bg-green-500/10 rounded border-2 border-green-500/20"></div>
                    <div className="absolute top-0 right-0 w-1/2 h-1/2 bg-yellow-500/10 rounded border-2 border-yellow-500/20"></div>
                    <div className="absolute bottom-0 left-0 w-1/2 h-1/2 bg-orange-500/10 rounded border-2 border-orange-500/20"></div>
                    <div className="absolute bottom-0 right-0 w-1/2 h-1/2 bg-red-500/10 rounded border-2 border-red-500/20"></div>
                  </div>

                  {/* Axes Labels */}
                  <div className="absolute bottom-2 left-1/2 transform -translate-x-1/2 text-xs text-muted-foreground">
                    투입 예산 (억원)
                  </div>
                  <div className="absolute left-2 top-1/2 transform -translate-y-1/2 -rotate-90 text-xs text-muted-foreground">
                    성과 지표 (점수)
                  </div>
                </div>

                {/* Enhanced Legend with efficiency zones */}
                <div className="absolute top-4 right-4 bg-background/95 p-4 rounded-lg border shadow-lg">
                  <div className="text-xs font-medium mb-3">효율성 구간</div>
                  <div className="space-y-2">
                    <div className="flex items-center gap-2">
                      <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                      <span className="text-xs">우수 (저비용-고성과)</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
                      <span className="text-xs">양호 (고비용-고성과)</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="w-3 h-3 bg-orange-500 rounded-full"></div>
                      <span className="text-xs">보통 (저비용-저성과)</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="w-3 h-3 bg-red-500 rounded-full"></div>
                      <span className="text-xs">개선필요 (고비용-저성과)</span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Selected Sport Details */}
              {selectedSport && (
                <div className="mt-4 p-4 bg-muted/50 rounded-lg">
                  {(() => {
                    const sport = sportsData.find((s) => s.sport === selectedSport)
                    return sport ? (
                      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                        <div>
                          <h4 className="font-medium mb-2">{sport.sport} 상세 정보</h4>
                          <div className="space-y-1 text-sm">
                            <div>총 예산: {sport.budget}억원</div>
                            <div>성과 점수: {sport.performance}점</div>
                            <div>메달 수: {sport.medals}개</div>
                            <div>세계 랭킹: {sport.performanceMetrics.worldRanking}위</div>
                          </div>
                        </div>
                        <div>
                          <h4 className="font-medium mb-2">예산 배분</h4>
                          <div className="space-y-1 text-sm">
                            <div>장비: {sport.budgetDetails.equipment}억원</div>
                            <div>훈련: {sport.budgetDetails.training}억원</div>
                            <div>대회: {sport.budgetDetails.competition}억원</div>
                          </div>
                        </div>
                        <div>
                          <h4 className="font-medium mb-2">지원 기관</h4>
                          <div className="space-y-1">
                            {sport.supportInstitutions.map((inst) => (
                              <Badge key={inst} variant="secondary" className="text-xs mr-1">
                                {inst}
                              </Badge>
                            ))}
                          </div>
                        </div>
                      </div>
                    ) : null
                  })()}
                </div>
              )}
            </CardContent>
          </Card>

          {/* Detailed Analysis Tables */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Sports Performance */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Trophy className="h-4 w-4" />
                  종목별 성과 분석
                </CardTitle>
                <CardDescription>투입 예산 대비 성과 효율성 순위</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {sportsData
                    .sort((a, b) => b.performance / b.budget - a.performance / a.budget)
                    .map((item, index) => (
                      <div key={item.sport} className="flex items-center justify-between p-3 border rounded-lg">
                        <div className="flex items-center gap-3">
                          <div className="w-6 h-6 rounded-full bg-primary/10 flex items-center justify-center text-xs font-bold">
                            {index + 1}
                          </div>
                          <div>
                            <div className="font-medium">{item.sport}</div>
                            <div className="text-sm text-muted-foreground">
                              예산 {item.budget}억원 • 메달 {item.medals}개
                            </div>
                          </div>
                        </div>
                        <div className="flex items-center gap-2">
                          <div className="text-right">
                            <div className="text-sm font-medium">{item.performance}점</div>
                            <div className="text-xs text-muted-foreground">
                              효율성: {(item.performance / item.budget).toFixed(2)}
                            </div>
                          </div>
                          <Badge
                            variant={
                              item.efficiency === "excellent"
                                ? "default"
                                : item.efficiency === "good"
                                  ? "secondary"
                                  : item.efficiency === "average"
                                    ? "outline"
                                    : "destructive"
                            }
                            className="text-xs"
                          >
                            {item.efficiency === "excellent"
                              ? "우수"
                              : item.efficiency === "good"
                                ? "양호"
                                : item.efficiency === "average"
                                  ? "보통"
                                  : "개선필요"}
                          </Badge>
                        </div>
                      </div>
                    ))}
                </div>
              </CardContent>
            </Card>

            {/* Regional Performance with Data Completeness */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <DollarSign className="h-4 w-4" />
                  지역별 예산 효율성
                </CardTitle>
                <CardDescription>추정 데이터 기반 분석 (데이터 완성도 표시)</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {regionData.map((item) => (
                    <div key={item.region} className="p-3 border rounded-lg">
                      <div className="flex items-center justify-between mb-2">
                        <div className="flex items-center gap-2">
                          <div className="font-medium">{item.region}</div>
                          <Badge variant="outline" className="text-xs">
                            완성도 {item.dataCompleteness}%
                          </Badge>
                        </div>
                        <div className="flex items-center gap-2">
                          <div className="text-right">
                            <div className="text-sm font-medium">{item.performance}점</div>
                          </div>
                          {item.trend === "up" && <TrendingUp className="h-4 w-4 text-green-600" />}
                          {item.trend === "down" && <TrendingDown className="h-4 w-4 text-red-600" />}
                          {item.trend === "stable" && <div className="h-4 w-4 bg-gray-400 rounded-full" />}
                        </div>
                      </div>
                      <div className="flex justify-between text-sm text-muted-foreground">
                        <span>
                          예산 {item.budget}억원 • 기관 {item.institutions}개
                        </span>
                        <span>시민 기여 {item.citizenContributions}건</span>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="mapping" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Database className="h-5 w-5" />
                기관-지역 매핑 테이블
              </CardTitle>
              <CardDescription>
                API 데이터의 기관명을 분석하여 지역을 추정한 매핑 테이블입니다. 정확도 향상을 위해 시민 검증에
                참여해주세요.
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {institutionRegionMapping.map((mapping, index) => (
                  <div key={index} className="flex items-center justify-between p-3 border rounded-lg">
                    <div>
                      <div className="font-medium">{mapping.institution}</div>
                      <div className="text-sm text-muted-foreground">추정 지역: {mapping.estimatedRegion}</div>
                    </div>
                    <div className="flex items-center gap-2">
                      <Badge
                        variant={
                          mapping.confidence === "high"
                            ? "default"
                            : mapping.confidence === "medium"
                              ? "secondary"
                              : "outline"
                        }
                      >
                        {mapping.confidence === "high" ? "높음" : mapping.confidence === "medium" ? "보통" : "낮음"}
                      </Badge>
                      <Button variant="outline" size="sm">
                        검증하기
                      </Button>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="crowdsource" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Users className="h-5 w-5" />
                집단지성 데이터 보완
              </CardTitle>
              <CardDescription>공공데이터의 한계를 시민 참여로 보완하여 더 정확한 분석을 만들어갑니다.</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-4">
                  <h4 className="font-medium">데이터 보완이 필요한 영역</h4>
                  <div className="space-y-3">
                    <div className="p-3 border rounded-lg">
                      <div className="font-medium text-sm">지역별 성과 데이터</div>
                      <div className="text-sm text-muted-foreground mt-1">선수 소속 지역 정보 부족 (완성도: 45%)</div>
                      <Button variant="outline" size="sm" className="mt-2 bg-transparent">
                        기여하기
                      </Button>
                    </div>
                    <div className="p-3 border rounded-lg">
                      <div className="font-medium text-sm">시설 이용률 데이터</div>
                      <div className="text-sm text-muted-foreground mt-1">실제 이용 현황 정보 부족 (완성도: 32%)</div>
                      <Button variant="outline" size="sm" className="mt-2 bg-transparent">
                        기여하기
                      </Button>
                    </div>
                  </div>
                </div>
                <div className="space-y-4">
                  <h4 className="font-medium">최근 시민 기여 현황</h4>
                  <div className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span>이번 주 기여</span>
                      <span className="font-medium">23건</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span>검증 완료</span>
                      <span className="font-medium">18건</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span>데이터 품질 향상</span>
                      <span className="font-medium text-green-600">+3.2%</span>
                    </div>
                  </div>
                  <Button className="w-full">데이터 기여 참여하기</Button>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="insights" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>주요 인사이트</CardTitle>
              <CardDescription>데이터 분석을 통해 도출된 핵심 발견사항</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
                  <h4 className="font-medium text-green-800 mb-2">효율성 우수 종목</h4>
                  <p className="text-sm text-green-700">
                    양궁과 배구가 가장 높은 예산 효율성을 보이며, 상대적으로 적은 투자로 우수한 성과를 달성하고
                    있습니다.
                  </p>
                </div>
                <div className="p-4 bg-orange-50 border border-orange-200 rounded-lg">
                  <h4 className="font-medium text-orange-800 mb-2">개선 필요 영역</h4>
                  <p className="text-sm text-orange-700">
                    축구는 높은 예산 투입에 비해 상대적으로 낮은 성과를 보이고 있어, 예산 배분 및 운영 방식의 개선이
                    필요합니다.
                  </p>
                </div>
                <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
                  <h4 className="font-medium text-blue-800 mb-2">데이터 거버넌스</h4>
                  <p className="text-sm text-blue-700">
                    시민 참여를 통한 데이터 보완으로 분석 정확도가 지속적으로 향상되고 있으며, 투명한 정책 결정을
                    지원하고 있습니다.
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
