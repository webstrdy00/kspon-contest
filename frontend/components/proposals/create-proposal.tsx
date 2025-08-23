"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Badge } from "@/components/ui/badge"
import { Label } from "@/components/ui/label"
import { PlusCircle, FileText, BarChart3, X, Upload } from "lucide-react"

export function CreateProposal() {
  const [title, setTitle] = useState("")
  const [description, setDescription] = useState("")
  const [category, setCategory] = useState("")
  const [region, setRegion] = useState("")
  const [attachedData, setAttachedData] = useState<string[]>([])

  const handleAttachData = (dataType: string) => {
    if (!attachedData.includes(dataType)) {
      setAttachedData([...attachedData, dataType])
    }
  }

  const handleRemoveData = (dataType: string) => {
    setAttachedData(attachedData.filter((item) => item !== dataType))
  }

  const handleSubmit = () => {
    // Handle form submission
    console.log("Submitting proposal:", { title, description, category, region, attachedData })
  }

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <PlusCircle className="h-5 w-5" />새 정책 제안 작성
          </CardTitle>
          <CardDescription>데이터를 근거로 한 구체적이고 실현 가능한 정책 제안을 작성해주세요</CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Basic Information */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="title">제안 제목</Label>
              <Input
                id="title"
                placeholder="구체적이고 명확한 제목을 입력하세요"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="category">카테고리</Label>
              <Select value={category} onValueChange={setCategory}>
                <SelectTrigger>
                  <SelectValue placeholder="카테고리 선택" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="시설 확충">시설 확충</SelectItem>
                  <SelectItem value="운영 개선">운영 개선</SelectItem>
                  <SelectItem value="접근성">접근성 개선</SelectItem>
                  <SelectItem value="예산">예산 관련</SelectItem>
                  <SelectItem value="정책">정책 개선</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          <div className="space-y-2">
            <Label htmlFor="region">대상 지역</Label>
            <Select value={region} onValueChange={setRegion}>
              <SelectTrigger>
                <SelectValue placeholder="지역 선택" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="seoul-mapo">서울특별시 마포구</SelectItem>
                <SelectItem value="seoul-gangnam">서울특별시 강남구</SelectItem>
                <SelectItem value="busan-haeundae">부산광역시 해운대구</SelectItem>
                <SelectItem value="daegu-suseong">대구광역시 수성구</SelectItem>
                <SelectItem value="incheon-yeonsu">인천광역시 연수구</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <Label htmlFor="description">제안 내용</Label>
            <Textarea
              id="description"
              placeholder="현재 상황, 문제점, 해결 방안을 구체적으로 설명해주세요"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              rows={6}
            />
          </div>

          {/* Data Attachment */}
          <div className="space-y-4">
            <div>
              <Label>근거 데이터 첨부</Label>
              <p className="text-sm text-muted-foreground">
                대시보드나 리포트의 데이터를 첨부하여 제안의 근거를 강화하세요
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <Card
                className="cursor-pointer hover:shadow-md transition-shadow"
                onClick={() => handleAttachData("supply-demand-chart")}
              >
                <CardContent className="p-4">
                  <div className="flex items-center gap-3">
                    <BarChart3 className="h-8 w-8 text-primary" />
                    <div>
                      <h4 className="font-medium">수요-공급 분석 차트</h4>
                      <p className="text-sm text-muted-foreground">지역별 시설 분포 데이터</p>
                    </div>
                  </div>
                </CardContent>
              </Card>

              <Card
                className="cursor-pointer hover:shadow-md transition-shadow"
                onClick={() => handleAttachData("regional-report")}
              >
                <CardContent className="p-4">
                  <div className="flex items-center gap-3">
                    <FileText className="h-8 w-8 text-chart-2" />
                    <div>
                      <h4 className="font-medium">우리 동네 리포트</h4>
                      <p className="text-sm text-muted-foreground">종합 분석 리포트</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Attached Data */}
            {attachedData.length > 0 && (
              <div className="space-y-2">
                <Label>첨부된 데이터</Label>
                <div className="flex flex-wrap gap-2">
                  {attachedData.map((data) => (
                    <Badge key={data} variant="secondary" className="gap-2">
                      {data === "supply-demand-chart" ? "수요-공급 분석 차트" : "우리 동네 리포트"}
                      <X className="h-3 w-3 cursor-pointer" onClick={() => handleRemoveData(data)} />
                    </Badge>
                  ))}
                </div>
              </div>
            )}

            {/* File Upload */}
            <div className="space-y-2">
              <Label>추가 자료 업로드</Label>
              <div className="border-2 border-dashed border-muted-foreground/25 rounded-lg p-6 text-center">
                <Upload className="h-8 w-8 text-muted-foreground mx-auto mb-2" />
                <p className="text-sm text-muted-foreground">
                  이미지, PDF, 문서 파일을 드래그하거나 클릭하여 업로드하세요
                </p>
                <Button variant="outline" size="sm" className="mt-2 bg-transparent">
                  파일 선택
                </Button>
              </div>
            </div>
          </div>

          {/* Guidelines */}
          <Card className="bg-muted/50">
            <CardContent className="p-4">
              <h4 className="font-medium mb-2">좋은 제안 작성 가이드</h4>
              <ul className="text-sm text-muted-foreground space-y-1">
                <li>• 구체적인 문제 상황과 해결 방안을 제시하세요</li>
                <li>• 데이터나 통계를 활용하여 객관적 근거를 제공하세요</li>
                <li>• 실현 가능한 범위 내에서 제안하세요</li>
                <li>• 예상 효과와 비용을 고려해주세요</li>
              </ul>
            </CardContent>
          </Card>

          {/* Submit Button */}
          <div className="flex justify-end gap-2">
            <Button variant="outline">임시 저장</Button>
            <Button onClick={handleSubmit} disabled={!title || !description || !category || !region}>
              제안 등록하기
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
