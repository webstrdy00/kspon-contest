"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { RegionalReport } from "./regional-report"
import { MapPin, FileText, Loader2 } from "lucide-react"

const regions = [
  { value: "seoul-mapo", label: "서울특별시 마포구", city: "서울특별시", district: "마포구" },
  { value: "seoul-gangnam", label: "서울특별시 강남구", city: "서울특별시", district: "강남구" },
  { value: "busan-haeundae", label: "부산광역시 해운대구", city: "부산광역시", district: "해운대구" },
  { value: "daegu-suseong", label: "대구광역시 수성구", city: "대구광역시", district: "수성구" },
  { value: "incheon-yeonsu", label: "인천광역시 연수구", city: "인천광역시", district: "연수구" },
  { value: "gwangju-seogu", label: "광주광역시 서구", city: "광주광역시", district: "서구" },
]

export function ReportGenerator() {
  const [selectedRegion, setSelectedRegion] = useState<string>("")
  const [isGenerating, setIsGenerating] = useState(false)
  const [reportGenerated, setReportGenerated] = useState(false)

  const handleGenerateReport = async () => {
    if (!selectedRegion) return

    setIsGenerating(true)
    // Simulate report generation
    await new Promise((resolve) => setTimeout(resolve, 2000))
    setIsGenerating(false)
    setReportGenerated(true)
  }

  const selectedRegionData = regions.find((r) => r.value === selectedRegion)

  return (
    <div className="space-y-6">
      {/* Region Selection */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <MapPin className="h-5 w-5" />
            지역 선택
          </CardTitle>
          <CardDescription>
            리포트를 생성할 지역을 선택해주세요. 시/군/구 단위로 상세한 분석을 제공합니다.
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="text-sm font-medium mb-2 block">지역 선택</label>
              <Select value={selectedRegion} onValueChange={setSelectedRegion}>
                <SelectTrigger>
                  <SelectValue placeholder="지역을 선택하세요" />
                </SelectTrigger>
                <SelectContent>
                  {regions.map((region) => (
                    <SelectItem key={region.value} value={region.value}>
                      {region.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            <div className="flex items-end">
              <Button
                onClick={handleGenerateReport}
                disabled={!selectedRegion || isGenerating}
                className="w-full gap-2"
              >
                {isGenerating ? (
                  <>
                    <Loader2 className="h-4 w-4 animate-spin" />
                    리포트 생성 중...
                  </>
                ) : (
                  <>
                    <FileText className="h-4 w-4" />
                    리포트 생성하기
                  </>
                )}
              </Button>
            </div>
          </div>

          {selectedRegion && !reportGenerated && (
            <div className="p-4 bg-muted/50 rounded-lg">
              <h4 className="font-medium mb-2">생성될 리포트 내용</h4>
              <ul className="text-sm text-muted-foreground space-y-1">
                <li>• 인구 및 여가 현황 분석</li>
                <li>• 체육시설 수요-공급 현황</li>
                <li>• 체육 예산 및 성과 분석</li>
                <li>• 전국 평균 및 인접 지역과의 비교</li>
                <li>• 정책 제안 및 개선 방향</li>
              </ul>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Generated Report */}
      {reportGenerated && selectedRegionData && <RegionalReport regionData={selectedRegionData} />}
    </div>
  )
}
