"use client"

import { useState } from "react"
import { Header } from "@/components/layout/header"
import { Sidebar } from "@/components/layout/sidebar"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import { RegionalReportGenerator } from "@/components/reports/regional-report-generator"
import { FileText, Download, Eye, Search, MapPin, Calendar, Star, TrendingUp } from "lucide-react"

export default function ReportsPage() {
  const [searchTerm, setSearchTerm] = useState("")
  const [selectedRegion, setSelectedRegion] = useState("")
  const [selectedType, setSelectedType] = useState("")

  const mockReports = [
    {
      id: 1,
      title: "서울특별시 중구 체육환경 종합 리포트",
      region: "서울특별시 중구",
      summary: "중구는 20대 인구 비율이 높지만 젊은층 선호 시설이 부족합니다.",
      generatedAt: "2025-01-25",
      viewCount: 145,
      downloadCount: 23,
      rating: 4.2
    },
    {
      id: 2,
      title: "부산광역시 해운대구 체육시설 현황 분석",
      region: "부산광역시 해운대구",
      summary: "해안가 특성을 활용한 수상스포츠 시설이 잘 갖추어져 있습니다.",
      generatedAt: "2025-01-24",
      viewCount: 89,
      downloadCount: 15,
      rating: 4.5
    },
    {
      id: 3,
      title: "대구광역시 수성구 생활체육 현황 리포트",
      region: "대구광역시 수성구",
      summary: "고령층을 위한 체육시설과 프로그램이 우수합니다.",
      generatedAt: "2025-01-23",
      viewCount: 67,
      downloadCount: 8,
      rating: 3.8
    }
  ]

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
                <h1 className="text-3xl font-bold tracking-tight">우리 동네 리포트</h1>
                <p className="text-muted-foreground">
                  지역별 체육환경 종합 분석 리포트를 생성하고 확인하세요
                </p>
              </div>
              <Button>
                <FileText className="mr-2 h-4 w-4" />
                새 리포트 생성
              </Button>
            </div>

            {/* 빠른 검색 */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Search className="h-5 w-5" />
                  빠른 리포트 검색
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                  <div>
                    <Label htmlFor="region">지역 선택</Label>
                    <Select value={selectedRegion} onValueChange={setSelectedRegion}>
                      <SelectTrigger>
                        <SelectValue placeholder="지역을 선택하세요" />
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
                    <Label htmlFor="type">리포트 유형</Label>
                    <Select value={selectedType} onValueChange={setSelectedType}>
                      <SelectTrigger>
                        <SelectValue placeholder="유형 선택" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="basic">기본 현황</SelectItem>
                        <SelectItem value="analysis">심화 분석</SelectItem>
                        <SelectItem value="satisfaction">만족도 조사</SelectItem>
                        <SelectItem value="facility">시설별 분석</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div>
                    <Label htmlFor="search">키워드 검색</Label>
                    <Input 
                      id="search"
                      placeholder="검색어를 입력하세요"
                      value={searchTerm}
                      onChange={(e) => setSearchTerm(e.target.value)}
                    />
                  </div>
                  <div className="flex items-end">
                    <Button className="w-full">
                      <Search className="h-4 w-4 mr-2" />
                      검색
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* 리포트 생성기 */}
            <RegionalReportGenerator />

            {/* 최근 생성된 리포트 */}
            <Card>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle className="flex items-center gap-2">
                      <FileText className="h-5 w-5" />
                      최근 생성된 리포트
                    </CardTitle>
                    <CardDescription>
                      최근에 생성된 지역별 리포트 목록입니다
                    </CardDescription>
                  </div>
                  <Badge variant="outline">
                    총 {mockReports.length}개 리포트
                  </Badge>
                </div>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {mockReports.map((report) => (
                    <div key={report.id} className="flex items-center justify-between p-4 border rounded-lg hover:bg-muted/50 transition-colors">
                      <div className="flex items-start gap-4">
                        <div className="p-2 bg-primary/10 rounded-lg">
                          <FileText className="h-5 w-5 text-primary" />
                        </div>
                        <div className="flex-1">
                          <h3 className="font-semibold mb-1">{report.title}</h3>
                          <p className="text-sm text-muted-foreground mb-2">{report.summary}</p>
                          <div className="flex items-center gap-2 text-xs text-muted-foreground">
                            <MapPin className="h-3 w-3" />
                            <span>{report.region}</span>
                            <Separator orientation="vertical" className="h-3" />
                            <Calendar className="h-3 w-3" />
                            <span>{report.generatedAt}</span>
                            <Separator orientation="vertical" className="h-3" />
                            <Star className="h-3 w-3" />
                            <span>{report.rating}</span>
                          </div>
                        </div>
                      </div>
                      <div className="flex items-center gap-3">
                        <div className="flex items-center gap-4 text-sm text-muted-foreground">
                          <div className="flex items-center gap-1">
                            <Eye className="h-3 w-3" />
                            {report.viewCount}
                          </div>
                          <div className="flex items-center gap-1">
                            <Download className="h-3 w-3" />
                            {report.downloadCount}
                          </div>
                        </div>
                        <div className="flex gap-2">
                          <Button size="sm" variant="ghost">
                            <Eye className="h-4 w-4" />
                          </Button>
                          <Button size="sm" variant="ghost">
                            <Download className="h-4 w-4" />
                          </Button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* 리포트 템플릿 */}
            <Card>
              <CardHeader>
                <CardTitle>리포트 템플릿</CardTitle>
                <CardDescription>
                  미리 정의된 템플릿을 사용하여 빠르게 리포트를 생성할 수 있습니다
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <Card className="hover:shadow-md transition-shadow cursor-pointer">
                    <CardHeader className="pb-3">
                      <CardTitle className="text-lg">기본 현황 리포트</CardTitle>
                      <CardDescription className="text-sm">
                        해당 지역의 체육시설 현황과 기본 통계를 제공합니다
                      </CardDescription>
                    </CardHeader>
                    <CardContent className="pt-0">
                      <div className="space-y-2 mb-4">
                        <div className="flex items-center gap-2 text-sm">
                          <TrendingUp className="h-3 w-3 text-primary" />
                          <span>시설 현황</span>
                        </div>
                        <div className="flex items-center gap-2 text-sm">
                          <TrendingUp className="h-3 w-3 text-primary" />
                          <span>이용률 통계</span>
                        </div>
                        <div className="flex items-center gap-2 text-sm">
                          <TrendingUp className="h-3 w-3 text-primary" />
                          <span>지역별 분포</span>
                        </div>
                        <div className="flex items-center gap-2 text-sm">
                          <TrendingUp className="h-3 w-3 text-primary" />
                          <span>기본 분석</span>
                        </div>
                      </div>
                      <Button className="w-full" variant="outline">
                        템플릿 사용
                      </Button>
                    </CardContent>
                  </Card>
                  <Card className="hover:shadow-md transition-shadow cursor-pointer">
                    <CardHeader className="pb-3">
                      <CardTitle className="text-lg">심화 분석 리포트</CardTitle>
                      <CardDescription className="text-sm">
                        수요-공급 분석과 개선 제안을 포함한 심화 리포트입니다
                      </CardDescription>
                    </CardHeader>
                    <CardContent className="pt-0">
                      <div className="space-y-2 mb-4">
                        <div className="flex items-center gap-2 text-sm">
                          <TrendingUp className="h-3 w-3 text-primary" />
                          <span>수요-공급 분석</span>
                        </div>
                        <div className="flex items-center gap-2 text-sm">
                          <TrendingUp className="h-3 w-3 text-primary" />
                          <span>GAP 분석</span>
                        </div>
                        <div className="flex items-center gap-2 text-sm">
                          <TrendingUp className="h-3 w-3 text-primary" />
                          <span>개선 제안</span>
                        </div>
                        <div className="flex items-center gap-2 text-sm">
                          <TrendingUp className="h-3 w-3 text-primary" />
                          <span>투자 우선순위</span>
                        </div>
                      </div>
                      <Button className="w-full" variant="outline">
                        템플릿 사용
                      </Button>
                    </CardContent>
                  </Card>
                  <Card className="hover:shadow-md transition-shadow cursor-pointer">
                    <CardHeader className="pb-3">
                      <CardTitle className="text-lg">시민 만족도 리포트</CardTitle>
                      <CardDescription className="text-sm">
                        시민 만족도 조사 결과와 개선 방안을 분석합니다
                      </CardDescription>
                    </CardHeader>
                    <CardContent className="pt-0">
                      <div className="space-y-2 mb-4">
                        <div className="flex items-center gap-2 text-sm">
                          <TrendingUp className="h-3 w-3 text-primary" />
                          <span>만족도 분석</span>
                        </div>
                        <div className="flex items-center gap-2 text-sm">
                          <TrendingUp className="h-3 w-3 text-primary" />
                          <span>불만 요인</span>
                        </div>
                        <div className="flex items-center gap-2 text-sm">
                          <TrendingUp className="h-3 w-3 text-primary" />
                          <span>개선 방향</span>
                        </div>
                        <div className="flex items-center gap-2 text-sm">
                          <TrendingUp className="h-3 w-3 text-primary" />
                          <span>비교 분석</span>
                        </div>
                      </div>
                      <Button className="w-full" variant="outline">
                        템플릿 사용
                      </Button>
                    </CardContent>
                  </Card>
                </div>
              </CardContent>
            </Card>
          </div>
        </main>
      </div>
    </div>
  )
}
