"use client"

import { useState, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { 
  ScatterChart, 
  Scatter, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  BarChart,
  Bar,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell
} from "recharts"
import { TrendingUp, DollarSign, Trophy, Target, BarChart3, Download } from "lucide-react"

interface BudgetPerformanceData {
  sport: string
  region: string
  budget: number
  performance: number
  efficiency: number
  medals: number
  budgetPerMedal: number
}

interface EfficiencyData {
  sport: string
  efficiency: number
  budget: number
  medals: number
  rank: number
}

export function BudgetPerformanceChart() {
  const [selectedYear, setSelectedYear] = useState("2023")
  const [selectedSport, setSelectedSport] = useState("all")
  const [chartType, setChartType] = useState<"scatter" | "bar" | "line">("scatter")

  // Mock 데이터
  const budgetPerformanceData: BudgetPerformanceData[] = [
    {
      sport: "양궁",
      region: "전국",
      budget: 6800000000, // 68억원
      performance: 95,
      efficiency: 2.18,
      medals: 15,
      budgetPerMedal: 453333333
    },
    {
      sport: "태권도", 
      region: "전국",
      budget: 6100000000,
      performance: 88,
      efficiency: 1.95,
      medals: 12,
      budgetPerMedal: 508333333
    },
    {
      sport: "역도",
      region: "전국", 
      budget: 4600000000,
      performance: 82,
      efficiency: 1.73,
      medals: 8,
      budgetPerMedal: 575000000
    },
    {
      sport: "유도",
      region: "전국",
      budget: 5900000000,
      performance: 79,
      efficiency: 1.52,
      medals: 9,
      budgetPerMedal: 655555556
    },
    {
      sport: "펜싱",
      region: "전국",
      budget: 4900000000,
      performance: 75,
      efficiency: 1.41,
      medals: 7,
      budgetPerMedal: 700000000
    },
    {
      sport: "수영",
      region: "전국",
      budget: 8500000000,
      performance: 72,
      efficiency: 1.28,
      medals: 11,
      budgetPerMedal: 772727273
    },
    {
      sport: "골프",
      region: "전국",
      budget: 7200000000,
      performance: 68,
      efficiency: 1.15,
      medals: 6,
      budgetPerMedal: 1200000000
    },
    {
      sport: "축구",
      region: "전국", 
      budget: 15000000000,
      performance: 65,
      efficiency: 0.98,
      medals: 3,
      budgetPerMedal: 5000000000
    }
  ]

  const efficiencyRanking: EfficiencyData[] = budgetPerformanceData
    .map((item, index) => ({
      sport: item.sport,
      efficiency: item.efficiency,
      budget: item.budget,
      medals: item.medals,
      rank: index + 1
    }))
    .sort((a, b) => b.efficiency - a.efficiency)
    .map((item, index) => ({ ...item, rank: index + 1 }))

  const investmentByCategory = [
    { name: "개인 종목", value: 45, amount: 28500000000 },
    { name: "단체 종목", value: 35, amount: 22750000000 },
    { name: "시설 인프라", value: 20, amount: 13000000000 }
  ]

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8', '#82CA9D', '#FFC658', '#FF7300']

  const formatCurrency = (value: number) => {
    return `${(value / 100000000).toFixed(0)}억원`
  }

  const formatEfficiency = (value: number) => {
    return value.toFixed(2)
  }

  return (
    <div className="space-y-6">
      {/* 컨트롤 패널 */}
      <div className="flex items-center gap-4 p-4 bg-muted/30 rounded-lg">
        <div className="flex items-center gap-2">
          <label className="text-sm font-medium">연도:</label>
          <Select value={selectedYear} onValueChange={setSelectedYear}>
            <SelectTrigger className="w-24">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="2023">2023</SelectItem>
              <SelectItem value="2022">2022</SelectItem>
              <SelectItem value="2021">2021</SelectItem>
            </SelectContent>
          </Select>
        </div>
        <div className="flex items-center gap-2">
          <label className="text-sm font-medium">종목:</label>
          <Select value={selectedSport} onValueChange={setSelectedSport}>
            <SelectTrigger className="w-32">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">전체 종목</SelectItem>
              <SelectItem value="양궁">양궁</SelectItem>
              <SelectItem value="태권도">태권도</SelectItem>
              <SelectItem value="수영">수영</SelectItem>
              <SelectItem value="골프">골프</SelectItem>
            </SelectContent>
          </Select>
        </div>
        <div className="flex items-center gap-2">
          <label className="text-sm font-medium">차트:</label>
          <Select value={chartType} onValueChange={(value: "scatter" | "bar" | "line") => setChartType(value)}>
            <SelectTrigger className="w-32">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="scatter">산점도</SelectItem>
              <SelectItem value="bar">막대그래프</SelectItem>
              <SelectItem value="line">선그래프</SelectItem>
            </SelectContent>
          </Select>
        </div>
        <Button variant="outline" size="sm" className="ml-auto">
          <Download className="h-4 w-4 mr-2" />
          데이터 내보내기
        </Button>
      </div>

      <Tabs defaultValue="efficiency" className="space-y-6">
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="efficiency">효율성 분석</TabsTrigger>
          <TabsTrigger value="investment">투자 현황</TabsTrigger>
          <TabsTrigger value="trends">연도별 추이</TabsTrigger>
        </TabsList>

        <TabsContent value="efficiency" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* 메인 차트 */}
            <div className="lg:col-span-2">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <TrendingUp className="h-5 w-5" />
                    예산 효율성 분석 ({selectedYear}년)
                  </CardTitle>
                  <CardDescription>
                    X축: 투입 예산 (억원) | Y축: 성과 점수 | 크기: 메달 수
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="h-[400px]">
                    {chartType === "scatter" && (
                      <ResponsiveContainer width="100%" height="100%">
                        <ScatterChart>
                          <CartesianGrid strokeDasharray="3 3" />
                          <XAxis 
                            type="number" 
                            dataKey="budget" 
                            name="예산"
                            tickFormatter={formatCurrency}
                            domain={['dataMin - 1000000000', 'dataMax + 1000000000']}
                          />
                          <YAxis 
                            type="number" 
                            dataKey="performance" 
                            name="성과"
                            domain={['dataMin - 5', 'dataMax + 5']}
                          />
                          <Tooltip 
                            cursor={{ strokeDasharray: '3 3' }}
                            content={({ active, payload }) => {
                              if (active && payload && payload.length > 0) {
                                const data = payload[0].payload as BudgetPerformanceData
                                return (
                                  <div className="bg-white p-4 border rounded-lg shadow-lg">
                                    <h3 className="font-bold text-lg mb-2">{data.sport}</h3>
                                    <div className="space-y-1 text-sm">
                                      <p><strong>투입 예산:</strong> {formatCurrency(data.budget)}</p>
                                      <p><strong>성과 점수:</strong> {data.performance}점</p>
                                      <p><strong>메달 수:</strong> {data.medals}개</p>
                                      <p><strong>효율성:</strong> {formatEfficiency(data.efficiency)}</p>
                                      <p><strong>메달당 예산:</strong> {formatCurrency(data.budgetPerMedal)}</p>
                                    </div>
                                  </div>
                                )
                              }
                              return null
                            }}
                          />
                          <Scatter 
                            name="종목" 
                            data={budgetPerformanceData} 
                            fill="#8884d8"
                          >
                            {budgetPerformanceData.map((entry, index) => (
                              <Cell 
                                key={`cell-${index}`} 
                                fill={COLORS[index % COLORS.length]}
                              />
                            ))}
                          </Scatter>
                        </ScatterChart>
                      </ResponsiveContainer>
                    )}

                    {chartType === "bar" && (
                      <ResponsiveContainer width="100%" height="100%">
                        <BarChart data={budgetPerformanceData}>
                          <CartesianGrid strokeDasharray="3 3" />
                          <XAxis dataKey="sport" angle={-45} textAnchor="end" height={100} />
                          <YAxis />
                          <Tooltip formatter={(value, name) => [
                            name === "efficiency" ? formatEfficiency(value as number) : value,
                            name === "efficiency" ? "효율성" : name === "budget" ? "예산" : "성과"
                          ]} />
                          <Bar dataKey="efficiency" fill="#8884d8" name="효율성" />
                        </BarChart>
                      </ResponsiveContainer>
                    )}

                    {chartType === "line" && (
                      <ResponsiveContainer width="100%" height="100%">
                        <LineChart data={budgetPerformanceData}>
                          <CartesianGrid strokeDasharray="3 3" />
                          <XAxis dataKey="sport" angle={-45} textAnchor="end" height={100} />
                          <YAxis />
                          <Tooltip />
                          <Line type="monotone" dataKey="efficiency" stroke="#8884d8" strokeWidth={2} name="효율성" />
                          <Line type="monotone" dataKey="performance" stroke="#82ca9d" strokeWidth={2} name="성과" />
                        </LineChart>
                      </ResponsiveContainer>
                    )}
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* 효율성 랭킹 */}
            <div>
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <Trophy className="h-5 w-5" />
                    효율성 순위
                  </CardTitle>
                  <CardDescription>
                    투입 예산 대비 성과 효율성
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {efficiencyRanking.slice(0, 8).map((item) => (
                      <div key={item.sport} className="flex items-center gap-3 p-3 bg-muted/50 rounded-lg">
                        <div className={`w-8 h-8 rounded-full flex items-center justify-center text-white text-sm font-bold ${
                          item.rank === 1 ? 'bg-yellow-500' :
                          item.rank === 2 ? 'bg-gray-400' :
                          item.rank === 3 ? 'bg-amber-600' : 'bg-primary'
                        }`}>
                          {item.rank}
                        </div>
                        <div className="flex-1">
                          <div className="font-medium">{item.sport}</div>
                          <div className="text-sm text-muted-foreground">
                            메달 {item.medals}개 • {formatCurrency(item.budget)}
                          </div>
                        </div>
                        <Badge variant="secondary">
                          {formatEfficiency(item.efficiency)}
                        </Badge>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </TabsContent>

        <TabsContent value="investment" className="space-y-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <BarChart3 className="h-5 w-5" />
                  분야별 투자 현황
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="h-[300px]">
                  <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                      <Pie
                        data={investmentByCategory}
                        cx="50%"
                        cy="50%"
                        labelLine={false}
                        label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                        outerRadius={80}
                        fill="#8884d8"
                        dataKey="value"
                      >
                        {investmentByCategory.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                        ))}
                      </Pie>
                      <Tooltip formatter={(value, name) => [
                        `${value}% (${formatCurrency(investmentByCategory.find(item => item.name === name)?.amount || 0)})`,
                        '투자 비율'
                      ]} />
                    </PieChart>
                  </ResponsiveContainer>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>투자 효율성 개선 제안</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="p-4 bg-green-50 border border-green-200 rounded-lg">
                    <h4 className="font-medium text-green-800 mb-2">고효율 종목 확대</h4>
                    <p className="text-sm text-green-700">
                      양궁, 태권도 등 효율성 2.0 이상 종목에 추가 투자 검토
                    </p>
                  </div>
                  <div className="p-4 bg-orange-50 border border-orange-200 rounded-lg">
                    <h4 className="font-medium text-orange-800 mb-2">저효율 종목 개선</h4>
                    <p className="text-sm text-orange-700">
                      축구, 골프 등 대규모 투자 대비 성과 부족 종목 전략 재검토
                    </p>
                  </div>
                  <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
                    <h4 className="font-medium text-blue-800 mb-2">균형 투자 필요</h4>
                    <p className="text-sm text-blue-700">
                      개인종목 편중에서 벗어나 단체종목 육성 강화
                    </p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="trends" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <TrendingUp className="h-5 w-5" />
                연도별 투자 및 성과 추이
              </CardTitle>
              <CardDescription>
                최근 3년간 예산 투입과 성과의 변화
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="h-[400px] bg-muted rounded-lg flex items-center justify-center">
                <div className="text-center">
                  <TrendingUp className="h-12 w-12 text-primary mx-auto mb-4" />
                  <h3 className="font-semibold text-lg mb-2">연도별 추이 분석</h3>
                  <p className="text-muted-foreground text-sm">
                    2021-2023년 예산 투입 및 성과 변화
                    <br />
                    실제 구현시 LineChart 또는 AreaChart 활용
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