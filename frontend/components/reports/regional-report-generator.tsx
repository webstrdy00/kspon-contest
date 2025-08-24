"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Textarea } from "@/components/ui/textarea"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Separator } from "@/components/ui/separator"
import { 
  MapPin, 
  FileText, 
  Settings, 
  Clock, 
  CheckCircle, 
  AlertCircle, 
  BarChart3,
  Users,
  Building2,
  TrendingUp,
  Download
} from "lucide-react"

interface ReportConfig {
  region: string
  reportType: string
  includeAnalysis: boolean
  includeSatisfaction: boolean
  includeRecommendations: boolean
  customPrompt?: string
}

interface ReportStatus {
  stage: 'idle' | 'data-collection' | 'analysis' | 'generation' | 'completed' | 'error'
  progress: number
  message: string
  estimatedTime?: number
}

export function RegionalReportGenerator() {
  const [config, setConfig] = useState<ReportConfig>({
    region: "",
    reportType: "comprehensive",
    includeAnalysis: true,
    includeSatisfaction: true,
    includeRecommendations: true
  })

  const [status, setStatus] = useState<ReportStatus>({
    stage: 'idle',
    progress: 0,
    message: "리포트 생성 준비 완료"
  })

  const [generatedReport, setGeneratedReport] = useState<any>(null)

  const handleGenerateReport = async () => {
    setStatus({ stage: 'data-collection', progress: 10, message: "지역 데이터 수집 중..." })
    
    // Simulate report generation process
    setTimeout(() => {
      setStatus({ stage: 'analysis', progress: 40, message: "데이터 분석 중..." })
    }, 2000)

    setTimeout(() => {
      setStatus({ stage: 'generation', progress: 80, message: "리포트 생성 중..." })
    }, 4000)

    setTimeout(() => {
      setStatus({ stage: 'completed', progress: 100, message: "리포트 생성 완료!" })
      setGeneratedReport({
        title: `${getRegionName(config.region)} 체육환경 종합 리포트`,
        summary: mockReportSummary,
        generatedAt: new Date().toISOString().split('T')[0]
      })
    }, 6000)
  }

  const getRegionName = (code: string) => {
    const regions: { [key: string]: string } = {
      "11": "서울특별시",
      "26": "부산광역시", 
      "27": "대구광역시",
      "28": "인천광역시",
      "29": "광주광역시",
      "30": "대전광역시"
    }
    return regions[code] || code
  }

  const mockReportSummary = {
    totalFacilities: 1247,
    satisfaction: 82.5,
    supplyDemandRatio: 0.78,
    recommendations: [
      "수영장 시설 확충 필요 (부족률 22%)",
      "고령자 친화 시설 개선 권장",
      "접근성 개선을 위한 대중교통 연계 강화"
    ],
    demographics: {
      totalPopulation: 485632,
      ageGroups: {
        "20-30대": 28.5,
        "30-40대": 24.2,
        "40-50대": 22.1,
        "50대 이상": 25.2
      }
    }
  }

  const renderGenerationSteps = () => {
    const steps = [
      { key: 'data-collection', label: '데이터 수집', icon: <Building2 className="h-4 w-4" /> },
      { key: 'analysis', label: '분석 처리', icon: <BarChart3 className="h-4 w-4" /> },
      { key: 'generation', label: '리포트 생성', icon: <FileText className="h-4 w-4" /> },
      { key: 'completed', label: '완료', icon: <CheckCircle className="h-4 w-4" /> }
    ]

    return (
      <div className="flex items-center justify-between">
        {steps.map((step, index) => (
          <div key={step.key} className="flex items-center">
            <div className={`flex items-center justify-center w-8 h-8 rounded-full ${
              status.stage === step.key ? 'bg-primary text-primary-foreground' :
              steps.findIndex(s => s.key === status.stage) > index || status.stage === 'completed' ? 'bg-green-500 text-white' :
              'bg-muted text-muted-foreground'
            }`}>
              {step.icon}
            </div>
            {index < steps.length - 1 && (
              <div className={`w-16 h-0.5 ml-2 ${
                steps.findIndex(s => s.key === status.stage) > index || status.stage === 'completed' ? 'bg-green-500' : 'bg-muted'
              }`} />
            )}
          </div>
        ))}
      </div>
    )
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <MapPin className="h-5 w-5" />
          지역 리포트 자동 생성기
        </CardTitle>
        <CardDescription>
          AI 기반으로 선택한 지역의 체육환경을 종합 분석하여 자동으로 리포트를 생성합니다
        </CardDescription>
      </CardHeader>

      <CardContent>
        <Tabs defaultValue="config" className="space-y-6">
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="config">설정</TabsTrigger>
            <TabsTrigger value="preview">미리보기</TabsTrigger>
          </TabsList>

          <TabsContent value="config" className="space-y-6">
            {/* 기본 설정 */}
            <div className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="region">지역 선택</Label>
                  <Select value={config.region} onValueChange={(value) => setConfig({...config, region: value})}>
                    <SelectTrigger>
                      <SelectValue placeholder="분석할 지역을 선택하세요" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="11">서울특별시</SelectItem>
                      <SelectItem value="26">부산광역시</SelectItem>
                      <SelectItem value="27">대구광역시</SelectItem>
                      <SelectItem value="28">인천광역시</SelectItem>
                      <SelectItem value="29">광주광역시</SelectItem>
                      <SelectItem value="30">대전광역시</SelectItem>
                      <SelectItem value="31">울산광역시</SelectItem>
                      <SelectItem value="36">세종특별자치시</SelectItem>
                      <SelectItem value="41">경기도</SelectItem>
                      <SelectItem value="42">강원도</SelectItem>
                      <SelectItem value="43">충청북도</SelectItem>
                      <SelectItem value="44">충청남도</SelectItem>
                      <SelectItem value="45">전라북도</SelectItem>
                      <SelectItem value="46">전라남도</SelectItem>
                      <SelectItem value="47">경상북도</SelectItem>
                      <SelectItem value="48">경상남도</SelectItem>
                      <SelectItem value="49">제주특별자치도</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div>
                  <Label htmlFor="reportType">리포트 유형</Label>
                  <Select value={config.reportType} onValueChange={(value) => setConfig({...config, reportType: value})}>
                    <SelectTrigger>
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="comprehensive">종합 분석</SelectItem>
                      <SelectItem value="facilities">시설 중심</SelectItem>
                      <SelectItem value="demographics">인구 중심</SelectItem>
                      <SelectItem value="satisfaction">만족도 중심</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>

              {/* 포함할 분석 옵션 */}
              <div className="space-y-3">
                <Label>포함할 분석 항목</Label>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                  <label className="flex items-center space-x-2 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={config.includeAnalysis}
                      onChange={(e) => setConfig({...config, includeAnalysis: e.target.checked})}
                      className="rounded border-gray-300"
                    />
                    <span className="text-sm">수요-공급 분석</span>
                  </label>
                  <label className="flex items-center space-x-2 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={config.includeSatisfaction}
                      onChange={(e) => setConfig({...config, includeSatisfaction: e.target.checked})}
                      className="rounded border-gray-300"
                    />
                    <span className="text-sm">만족도 조사</span>
                  </label>
                  <label className="flex items-center space-x-2 cursor-pointer">
                    <input
                      type="checkbox"
                      checked={config.includeRecommendations}
                      onChange={(e) => setConfig({...config, includeRecommendations: e.target.checked})}
                      className="rounded border-gray-300"
                    />
                    <span className="text-sm">개선 제안</span>
                  </label>
                </div>
              </div>

              {/* 추가 요청사항 */}
              <div>
                <Label htmlFor="customPrompt">추가 분석 요청사항 (선택)</Label>
                <Textarea
                  id="customPrompt"
                  placeholder="특별히 분석하고 싶은 내용이 있다면 입력하세요..."
                  value={config.customPrompt || ""}
                  onChange={(e) => setConfig({...config, customPrompt: e.target.value})}
                  className="mt-2"
                />
              </div>
            </div>

            {/* 생성 진행 상황 */}
            {status.stage !== 'idle' && (
              <div className="space-y-4 p-4 bg-muted/50 rounded-lg">
                <div className="flex items-center justify-between">
                  <h4 className="font-medium">리포트 생성 진행 상황</h4>
                  <Badge variant={status.stage === 'completed' ? 'default' : 'secondary'}>
                    {status.stage === 'completed' ? '완료' : '진행중'}
                  </Badge>
                </div>
                
                <Progress value={status.progress} className="w-full" />
                
                <div className="flex items-center gap-2 text-sm text-muted-foreground">
                  <Clock className="h-4 w-4" />
                  {status.message}
                </div>

                {renderGenerationSteps()}
              </div>
            )}

            {/* 생성 버튼 */}
            <div className="flex justify-end gap-3">
              <Button variant="outline" disabled={status.stage !== 'idle' && status.stage !== 'completed'}>
                <Settings className="h-4 w-4 mr-2" />
                설정 저장
              </Button>
              <Button 
                onClick={handleGenerateReport} 
                disabled={!config.region || (status.stage !== 'idle' && status.stage !== 'completed')}
              >
                <FileText className="h-4 w-4 mr-2" />
                {status.stage === 'idle' || status.stage === 'completed' ? '리포트 생성' : '생성 중...'}
              </Button>
            </div>
          </TabsContent>

          <TabsContent value="preview" className="space-y-6">
            {generatedReport ? (
              <div className="space-y-6">
                {/* 리포트 헤더 */}
                <div className="text-center space-y-2 p-6 bg-gradient-to-r from-primary/10 to-secondary/10 rounded-lg">
                  <h2 className="text-2xl font-bold">{generatedReport.title}</h2>
                  <p className="text-muted-foreground">생성일: {generatedReport.generatedAt}</p>
                </div>

                {/* 요약 통계 */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <Card>
                    <CardContent className="p-4">
                      <div className="text-2xl font-bold">{mockReportSummary.totalFacilities.toLocaleString()}</div>
                      <p className="text-sm text-muted-foreground">총 체육시설</p>
                    </CardContent>
                  </Card>
                  <Card>
                    <CardContent className="p-4">
                      <div className="text-2xl font-bold">{mockReportSummary.satisfaction}%</div>
                      <p className="text-sm text-muted-foreground">만족도</p>
                    </CardContent>
                  </Card>
                  <Card>
                    <CardContent className="p-4">
                      <div className="text-2xl font-bold">{(mockReportSummary.supplyDemandRatio * 100).toFixed(0)}%</div>
                      <p className="text-sm text-muted-foreground">공급률</p>
                    </CardContent>
                  </Card>
                  <Card>
                    <CardContent className="p-4">
                      <div className="text-2xl font-bold">{mockReportSummary.demographics.totalPopulation.toLocaleString()}</div>
                      <p className="text-sm text-muted-foreground">총 인구</p>
                    </CardContent>
                  </Card>
                </div>

                {/* 주요 발견사항 */}
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <TrendingUp className="h-5 w-5" />
                      주요 개선 제안
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      {mockReportSummary.recommendations.map((rec, index) => (
                        <div key={index} className="flex items-start gap-3 p-3 bg-muted/50 rounded-lg">
                          <AlertCircle className="h-5 w-5 text-orange-500 mt-0.5" />
                          <span className="text-sm">{rec}</span>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>

                {/* 인구 구조 */}
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <Users className="h-5 w-5" />
                      연령별 인구 분포
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      {Object.entries(mockReportSummary.demographics.ageGroups).map(([age, percent]) => (
                        <div key={age} className="flex items-center justify-between">
                          <span className="text-sm">{age}</span>
                          <div className="flex items-center gap-3">
                            <Progress value={percent as number} className="w-24" />
                            <span className="text-sm font-medium">{percent}%</span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>

                {/* 다운로드 버튼 */}
                <div className="flex justify-end gap-3">
                  <Button variant="outline">
                    <FileText className="h-4 w-4 mr-2" />
                    HTML 보기
                  </Button>
                  <Button>
                    <Download className="h-4 w-4 mr-2" />
                    PDF 다운로드
                  </Button>
                </div>
              </div>
            ) : (
              <div className="text-center py-12 space-y-4">
                <FileText className="h-12 w-12 text-muted-foreground mx-auto" />
                <h3 className="font-semibold text-lg">리포트 미리보기</h3>
                <p className="text-muted-foreground">
                  리포트를 생성하면 여기에서 미리보기를 확인할 수 있습니다
                </p>
                <Button variant="outline" onClick={() => document.querySelector('[value="config"]')?.click()}>
                  설정으로 이동
                </Button>
              </div>
            )}
          </TabsContent>
        </Tabs>
      </CardContent>
    </Card>
  )
}