"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import {
  Download,
  Share2,
  BarChart3,
  Users,
  MapPin,
  TrendingUp,
  TrendingDown,
  AlertTriangle,
  Target,
  Zap,
} from "lucide-react"

interface RegionData {
  value: string
  label: string
  city: string
  district: string
}

interface RegionalReportProps {
  regionData: RegionData
}

// Enhanced mock data with comparison features
const mockReportData = {
  demographics: {
    population: 385847,
    ageGroups: {
      "20s": 28.5,
      "30s": 22.1,
      "40s": 18.7,
      "50s": 16.2,
      "60s+": 14.5,
    },
    leisureTime: {
      weekday: 2.3,
      weekend: 4.7,
    },
  },
  facilities: {
    total: 47,
    types: {
      체육관: 12,
      수영장: 8,
      테니스장: 6,
      축구장: 9,
      농구장: 7,
      기타: 5,
    },
    utilization: 78.5,
    accessibilityScore: 82.3,
  },
  demand: {
    mostWanted: ["클라이밍짐", "풋살장", "배드민턴장"],
    satisfaction: 72.3,
    unmetDemand: 23.7,
    demandByAge: {
      "20s": ["클라이밍짐", "풋살장", "헬스장"],
      "30s": ["수영장", "테니스장", "요가스튜디오"],
      "40s": ["배드민턴장", "탁구장", "골프연습장"],
      "50s+": ["게이트볼장", "파크골프장", "산책로"],
    },
  },
  budget: {
    total: 45.2,
    perCapita: 117000,
    efficiency: 85.4,
    breakdown: {
      시설운영: 18.5,
      신규건설: 15.2,
      프로그램운영: 8.3,
      유지보수: 3.2,
    },
  },
  comparison: {
    nationalAverage: {
      facilitiesPerCapita: 0.89,
      current: 1.22,
      status: "above",
      budgetPerCapita: 95000,
      satisfaction: 68.5,
      utilization: 71.2,
    },
    neighboringRegions: [
      { name: "서대문구", score: 78.2, trend: "up", population: 312000, facilities: 38 },
      { name: "용산구", score: 82.1, trend: "stable", population: 229000, facilities: 35 },
      { name: "영등포구", score: 75.8, trend: "down", population: 408000, facilities: 52 },
    ],
    similarRegions: [
      { name: "성남시 분당구", score: 84.2, similarity: 92, reason: "인구구성 유사" },
      { name: "부산시 해운대구", score: 79.8, similarity: 88, reason: "여가수요 패턴 유사" },
      { name: "대전시 유성구", score: 81.5, similarity: 85, reason: "예산규모 유사" },
    ],
    benchmarkAnalysis: {
      bestPractice: {
        region: "성남시 분당구",
        score: 94.2,
        keyFactors: ["디지털 예약시스템", "민관협력 프로그램", "맞춤형 시설배치"],
      },
      improvementPotential: 18.8,
    },
  },
}

export function RegionalReport({ regionData }: RegionalReportProps) {
  const [comparisonType, setComparisonType] = useState("national")
  const [selectedMetric, setSelectedMetric] = useState("overall")
  const data = mockReportData

  const handleDownloadPDF = () => {
    console.log("Downloading PDF report...")
  }

  const getComparisonColor = (current: number, comparison: number, higherIsBetter = true) => {
    const diff = current - comparison
    if (higherIsBetter) {
      return diff > 0 ? "text-green-600" : "text-red-600"
    } else {
      return diff < 0 ? "text-green-600" : "text-red-600"
    }
  }

  const getComparisonIcon = (current: number, comparison: number, higherIsBetter = true) => {
    const diff = current - comparison
    if (higherIsBetter) {
      return diff > 0 ? (
        <TrendingUp className="h-4 w-4 text-green-600" />
      ) : (
        <TrendingDown className="h-4 w-4 text-red-600" />
      )
    } else {
      return diff < 0 ? (
        <TrendingUp className="h-4 w-4 text-green-600" />
      ) : (
        <TrendingDown className="h-4 w-4 text-red-600" />
      )
    }
  }

  return (
    <div className="space-y-6">
      {/* Enhanced Report Header */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle className="text-2xl font-heading">{regionData.label} 체육 환경 종합 리포트</CardTitle>
              <CardDescription className="mt-2">
                생성일: {new Date().toLocaleDateString("ko-KR")} | 데이터 기준: 2024년 3분기 | AI 분석 포함
              </CardDescription>
            </div>
            <div className="flex gap-2">
              <Button variant="outline" size="sm">
                <Share2 className="h-4 w-4 mr-2" />
                공유
              </Button>
              <Button onClick={handleDownloadPDF} size="sm">
                <Download className="h-4 w-4 mr-2" />
                PDF 다운로드
              </Button>
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <div className="bg-gradient-to-r from-primary/10 to-accent/10 p-6 rounded-lg">
            <h3 className="font-heading font-semibold text-lg mb-3">AI 분석 요약</h3>
            <p className="text-muted-foreground leading-relaxed mb-4">
              <strong>{regionData.district}</strong>는 20대 인구 비율이 전국 평균보다 15% 높지만, 20대가 선호하는
              클라이밍짐, 풋살장 등의 시설은 상대적으로 부족한 상황입니다. 전체적인 체육시설 수는 전국 평균을 상회하나,
              수요-공급 불일치 문제가 존재합니다.
            </p>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="text-center p-3 bg-background/50 rounded-lg">
                <div className="text-lg font-bold text-primary">85.4점</div>
                <div className="text-sm text-muted-foreground">종합 점수</div>
              </div>
              <div className="text-center p-3 bg-background/50 rounded-lg">
                <div className="text-lg font-bold text-green-600">+18.8점</div>
                <div className="text-sm text-muted-foreground">개선 잠재력</div>
              </div>
              <div className="text-center p-3 bg-background/50 rounded-lg">
                <div className="text-lg font-bold text-chart-2">전국 상위 23%</div>
                <div className="text-sm text-muted-foreground">순위</div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      <Tabs defaultValue="overview" className="w-full">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="overview">종합 현황</TabsTrigger>
          <TabsTrigger value="comparison">비교 분석</TabsTrigger>
          <TabsTrigger value="insights">심층 분석</TabsTrigger>
          <TabsTrigger value="recommendations">개선 방안</TabsTrigger>
        </TabsList>

        <TabsContent value="overview" className="space-y-6">
          {/* Demographics Analysis */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Users className="h-5 w-5" />
                인구 및 여가 현황
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div>
                  <h4 className="font-medium mb-3">인구 구성</h4>
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-sm">총 인구</span>
                      <span className="font-medium">{data.demographics.population.toLocaleString()}명</span>
                    </div>
                    {Object.entries(data.demographics.ageGroups).map(([age, percentage]) => (
                      <div key={age} className="flex justify-between">
                        <span className="text-sm">{age}</span>
                        <span className="text-sm">{percentage}%</span>
                      </div>
                    ))}
                  </div>
                </div>

                <div>
                  <h4 className="font-medium mb-3">여가 시간</h4>
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-sm">평일 평균</span>
                      <span className="font-medium">{data.demographics.leisureTime.weekday}시간</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm">주말 평균</span>
                      <span className="font-medium">{data.demographics.leisureTime.weekend}시간</span>
                    </div>
                  </div>
                </div>

                <div>
                  <h4 className="font-medium mb-3">특성 분석</h4>
                  <div className="space-y-2">
                    <Badge variant="secondary">젊은 인구 집중</Badge>
                    <Badge variant="outline">높은 여가 수요</Badge>
                    <Badge variant="outline">도심 접근성 우수</Badge>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Enhanced Facilities Analysis */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <MapPin className="h-5 w-5" />
                체육시설 현황
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h4 className="font-medium mb-3">시설 분포</h4>
                  <div className="space-y-3">
                    {Object.entries(data.facilities.types).map(([type, count]) => (
                      <div key={type} className="flex items-center justify-between">
                        <span className="text-sm">{type}</span>
                        <div className="flex items-center gap-2">
                          <div className="w-20 h-2 bg-muted rounded-full overflow-hidden">
                            <div
                              className="h-full bg-primary rounded-full"
                              style={{ width: `${(count / Math.max(...Object.values(data.facilities.types))) * 100}%` }}
                            />
                          </div>
                          <span className="text-sm font-medium w-8">{count}개</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                <div>
                  <h4 className="font-medium mb-3">연령대별 수요</h4>
                  <div className="space-y-3">
                    {Object.entries(data.demand.demandByAge).map(([age, facilities]) => (
                      <div key={age}>
                        <span className="text-sm font-medium">{age}</span>
                        <div className="flex gap-1 mt-1">
                          {facilities.slice(0, 2).map((facility) => (
                            <Badge key={facility} variant="secondary" className="text-xs">
                              {facility}
                            </Badge>
                          ))}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Enhanced Budget Analysis */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <BarChart3 className="h-5 w-5" />
                예산 및 성과
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
                <div className="text-center">
                  <div className="text-2xl font-bold text-primary">{data.budget.total}억원</div>
                  <div className="text-sm text-muted-foreground">총 투입 예산</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-chart-2">{data.budget.perCapita.toLocaleString()}원</div>
                  <div className="text-sm text-muted-foreground">1인당 예산</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-chart-4">{data.budget.efficiency}점</div>
                  <div className="text-sm text-muted-foreground">예산 효율성</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-chart-3">{data.facilities.accessibilityScore}점</div>
                  <div className="text-sm text-muted-foreground">접근성 점수</div>
                </div>
              </div>

              <div>
                <h4 className="font-medium mb-3">예산 배분</h4>
                <div className="space-y-2">
                  {Object.entries(data.budget.breakdown).map(([category, amount]) => (
                    <div key={category} className="flex items-center justify-between">
                      <span className="text-sm">{category}</span>
                      <div className="flex items-center gap-2">
                        <div className="w-24 h-2 bg-muted rounded-full overflow-hidden">
                          <div
                            className="h-full bg-primary rounded-full"
                            style={{ width: `${(amount / data.budget.total) * 100}%` }}
                          />
                        </div>
                        <span className="text-sm font-medium w-12">{amount}억원</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="comparison" className="space-y-6">
          <div className="flex items-center gap-4 mb-6">
            <Select value={comparisonType} onValueChange={setComparisonType}>
              <SelectTrigger className="w-48">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="national">전국 평균과 비교</SelectItem>
                <SelectItem value="neighboring">인접 지역과 비교</SelectItem>
                <SelectItem value="similar">유사 지역과 비교</SelectItem>
                <SelectItem value="benchmark">벤치마크 분석</SelectItem>
              </SelectContent>
            </Select>

            <Select value={selectedMetric} onValueChange={setSelectedMetric}>
              <SelectTrigger className="w-48">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="overall">종합 지표</SelectItem>
                <SelectItem value="facilities">시설 현황</SelectItem>
                <SelectItem value="budget">예산 효율성</SelectItem>
                <SelectItem value="satisfaction">주민 만족도</SelectItem>
              </SelectContent>
            </Select>
          </div>

          {comparisonType === "national" && (
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Target className="h-5 w-5" />
                  전국 평균과 비교
                </CardTitle>
                <CardDescription>우리 지역이 전국 평균 대비 어느 수준에 있는지 확인하세요</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="space-y-4">
                    <div className="flex items-center justify-between p-4 border rounded-lg">
                      <div>
                        <div className="font-medium">1인당 체육시설 수</div>
                        <div className="text-sm text-muted-foreground">
                          전국 평균: {data.comparison.nationalAverage.facilitiesPerCapita}
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
                        <span
                          className={`font-bold ${getComparisonColor(data.comparison.nationalAverage.current, data.comparison.nationalAverage.facilitiesPerCapita)}`}
                        >
                          {data.comparison.nationalAverage.current}
                        </span>
                        {getComparisonIcon(
                          data.comparison.nationalAverage.current,
                          data.comparison.nationalAverage.facilitiesPerCapita,
                        )}
                      </div>
                    </div>

                    <div className="flex items-center justify-between p-4 border rounded-lg">
                      <div>
                        <div className="font-medium">1인당 예산</div>
                        <div className="text-sm text-muted-foreground">
                          전국 평균: {data.comparison.nationalAverage.budgetPerCapita.toLocaleString()}원
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
                        <span
                          className={`font-bold ${getComparisonColor(data.budget.perCapita, data.comparison.nationalAverage.budgetPerCapita)}`}
                        >
                          {data.budget.perCapita.toLocaleString()}원
                        </span>
                        {getComparisonIcon(data.budget.perCapita, data.comparison.nationalAverage.budgetPerCapita)}
                      </div>
                    </div>
                  </div>

                  <div className="space-y-4">
                    <div className="flex items-center justify-between p-4 border rounded-lg">
                      <div>
                        <div className="font-medium">주민 만족도</div>
                        <div className="text-sm text-muted-foreground">
                          전국 평균: {data.comparison.nationalAverage.satisfaction}%
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
                        <span
                          className={`font-bold ${getComparisonColor(data.demand.satisfaction, data.comparison.nationalAverage.satisfaction)}`}
                        >
                          {data.demand.satisfaction}%
                        </span>
                        {getComparisonIcon(data.demand.satisfaction, data.comparison.nationalAverage.satisfaction)}
                      </div>
                    </div>

                    <div className="flex items-center justify-between p-4 border rounded-lg">
                      <div>
                        <div className="font-medium">시설 이용률</div>
                        <div className="text-sm text-muted-foreground">
                          전국 평균: {data.comparison.nationalAverage.utilization}%
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
                        <span
                          className={`font-bold ${getComparisonColor(data.facilities.utilization, data.comparison.nationalAverage.utilization)}`}
                        >
                          {data.facilities.utilization}%
                        </span>
                        {getComparisonIcon(data.facilities.utilization, data.comparison.nationalAverage.utilization)}
                      </div>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}

          {comparisonType === "similar" && (
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Users className="h-5 w-5" />
                  유사 지역과 비교
                </CardTitle>
                <CardDescription>인구구성, 예산규모 등이 유사한 지역과의 비교 분석</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {data.comparison.similarRegions.map((region) => (
                    <div key={region.name} className="flex items-center justify-between p-4 border rounded-lg">
                      <div>
                        <div className="font-medium">{region.name}</div>
                        <div className="text-sm text-muted-foreground">
                          유사도 {region.similarity}% • {region.reason}
                        </div>
                      </div>
                      <div className="flex items-center gap-2">
                        <span className="font-medium">{region.score}점</span>
                        <Badge variant={region.score > 85.4 ? "destructive" : "default"}>
                          {region.score > 85.4 ? "우수" : "유사"}
                        </Badge>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}

          {comparisonType === "benchmark" && (
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Zap className="h-5 w-5" />
                  벤치마크 분석
                </CardTitle>
                <CardDescription>최우수 지역의 성공 사례와 개선 잠재력 분석</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-6">
                  <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
                    <h4 className="font-medium text-green-800 mb-2">
                      벤치마크 지역: {data.comparison.benchmarkAnalysis.bestPractice.region}
                    </h4>
                    <div className="text-sm text-green-700 mb-3">
                      종합 점수: {data.comparison.benchmarkAnalysis.bestPractice.score}점
                    </div>
                    <div>
                      <span className="text-sm font-medium text-green-800">핵심 성공 요인:</span>
                      <div className="flex gap-2 mt-1">
                        {data.comparison.benchmarkAnalysis.bestPractice.keyFactors.map((factor) => (
                          <Badge key={factor} variant="secondary" className="text-xs">
                            {factor}
                          </Badge>
                        ))}
                      </div>
                    </div>
                  </div>

                  <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
                    <h4 className="font-medium text-blue-800 mb-2">개선 잠재력</h4>
                    <div className="text-2xl font-bold text-blue-600 mb-2">
                      +{data.comparison.benchmarkAnalysis.improvementPotential}점
                    </div>
                    <div className="text-sm text-blue-700">
                      벤치마크 지역의 모범 사례를 적용할 경우 예상되는 점수 향상
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}
        </TabsContent>

        <TabsContent value="insights" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>AI 기반 심층 분석</CardTitle>
              <CardDescription>데이터 패턴 분석을 통한 숨겨진 인사이트 발견</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="p-4 bg-primary/10 border border-primary/20 rounded-lg">
                  <h4 className="font-medium text-primary mb-2">수요-공급 패턴 분석</h4>
                  <p className="text-sm">
                    20-30대 인구 비율이 높음에도 불구하고 해당 연령대가 선호하는 시설(클라이밍짐, 풋살장)의 공급이
                    부족합니다. 반면 50대 이상이 선호하는 시설은 상대적으로 충분한 상황입니다.
                  </p>
                </div>

                <div className="p-4 bg-chart-2/10 border border-chart-2/20 rounded-lg">
                  <h4 className="font-medium text-chart-2 mb-2">시간대별 이용 패턴</h4>
                  <p className="text-sm">
                    평일 저녁(18-21시)과 주말 오전(9-12시)에 이용률이 집중되어 있어, 시설 가동률 개선을 위한 시간대별
                    차등 요금제 도입을 고려할 수 있습니다.
                  </p>
                </div>

                <div className="p-4 bg-chart-3/10 border border-chart-3/20 rounded-lg">
                  <h4 className="font-medium text-chart-3 mb-2">예산 효율성 분석</h4>
                  <p className="text-sm">
                    신규 시설 건설보다 기존 시설의 프로그램 다양화와 운영 시간 확대가 더 높은 비용 효율성을 보일 것으로
                    예상됩니다.
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="recommendations" className="space-y-6">
          {/* Enhanced Recommendations */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <AlertTriangle className="h-5 w-5" />
                데이터 기반 정책 제안
              </CardTitle>
              <CardDescription>분석 결과를 바탕으로 한 구체적이고 실행 가능한 개선 방안</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="p-4 bg-destructive/10 border border-destructive/20 rounded-lg">
                  <h4 className="font-medium text-destructive mb-2">즉시 실행 가능한 개선 사항</h4>
                  <ul className="text-sm space-y-1">
                    <li>• 기존 체육관 일부를 클라이밍 시설로 전환 (예상 비용: 2억원)</li>
                    <li>• 축구장 야간 조명 설치로 풋살장 겸용 활용 (예상 비용: 5천만원)</li>
                    <li>• 디지털 예약 시스템 도입으로 이용률 20% 향상 (예상 비용: 3천만원)</li>
                  </ul>
                </div>

                <div className="p-4 bg-chart-2/10 border border-chart-2/20 rounded-lg">
                  <h4 className="font-medium text-chart-2 mb-2">중장기 발전 방향 (1-3년)</h4>
                  <ul className="text-sm space-y-1">
                    <li>• 민간 체육시설과의 바우처 연계 프로그램 개발</li>
                    <li>• 연령대별 맞춤형 프로그램 확대 운영</li>
                    <li>• 접근성 개선을 위한 셔틀버스 운영</li>
                  </ul>
                </div>

                <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
                  <h4 className="font-medium text-green-800 mb-2">예상 효과</h4>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                    <div>
                      <div className="font-medium">주민 만족도</div>
                      <div className="text-green-600">72.3% → 85.1% (+12.8%p)</div>
                    </div>
                    <div>
                      <div className="font-medium">시설 이용률</div>
                      <div className="text-green-600">78.5% → 89.2% (+10.7%p)</div>
                    </div>
                    <div>
                      <div className="font-medium">예산 효율성</div>
                      <div className="text-green-600">85.4점 → 94.1점 (+8.7점)</div>
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}
