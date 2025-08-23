import { Card, CardContent, CardHeader } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Download, Share2, MapPin, Users, TrendingUp, AlertTriangle } from "lucide-react"

interface RegionalDetailReportProps {
  region: string
}

export function RegionalDetailReport({ region }: RegionalDetailReportProps) {
  // Mock data - 실제로는 API에서 가져올 데이터
  const reportData = {
    region: decodeURIComponent(region),
    generatedAt: "2024-01-18",
    population: 561234,
    facilities: {
      total: 45,
      perCapita: 0.8,
      nationalAverage: 1.2,
      gap: -33.3,
    },
    budget: {
      total: 1200000000,
      perCapita: 2138,
      efficiency: 78.5,
      nationalAverage: 82.1,
    },
    demand: {
      swimming: 34.2,
      fitness: 28.7,
      tennis: 15.3,
      golf: 12.8,
      others: 9.0,
    },
    satisfaction: 72.4,
    issues: [
      { type: "부족", facility: "수영장", severity: "높음", impact: "시민 불만 증가" },
      { type: "노후", facility: "체육관", severity: "중간", impact: "이용률 저하" },
      { type: "접근성", facility: "테니스장", severity: "낮음", impact: "특정 지역 편중" },
    ],
  }

  return (
    <div className="space-y-6">
      {/* 리포트 헤더 */}
      <Card>
        <CardHeader>
          <div className="flex items-start justify-between">
            <div className="space-y-2">
              <div className="flex items-center gap-2">
                <MapPin className="h-5 w-5 text-primary" />
                <h1 className="text-3xl font-heading font-bold">{reportData.region} 체육환경 종합분석</h1>
              </div>
              <p className="text-muted-foreground">
                생성일: {reportData.generatedAt} | 인구: {reportData.population.toLocaleString()}명
              </p>
            </div>
            <div className="flex items-center gap-2">
              <Button variant="outline" size="sm">
                <Share2 className="h-4 w-4 mr-2" />
                공유
              </Button>
              <Button size="sm">
                <Download className="h-4 w-4 mr-2" />
                PDF 다운로드
              </Button>
            </div>
          </div>
        </CardHeader>
      </Card>

      {/* 핵심 지표 */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-6">
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm text-muted-foreground">체육시설 수</span>
                <Badge variant={reportData.facilities.gap < 0 ? "destructive" : "default"}>
                  {reportData.facilities.gap > 0 ? "+" : ""}
                  {reportData.facilities.gap.toFixed(1)}%
                </Badge>
              </div>
              <div className="text-2xl font-bold">{reportData.facilities.total}개</div>
              <p className="text-xs text-muted-foreground">
                인구 1만명당 {reportData.facilities.perCapita}개 (전국 평균: {reportData.facilities.nationalAverage}개)
              </p>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm text-muted-foreground">예산 효율성</span>
                <TrendingUp className="h-4 w-4 text-green-500" />
              </div>
              <div className="text-2xl font-bold">{reportData.budget.efficiency}%</div>
              <p className="text-xs text-muted-foreground">
                전국 평균 대비 {(reportData.budget.efficiency - reportData.budget.nationalAverage).toFixed(1)}%p
              </p>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm text-muted-foreground">시민 만족도</span>
                <Users className="h-4 w-4 text-blue-500" />
              </div>
              <div className="text-2xl font-bold">{reportData.satisfaction}%</div>
              <p className="text-xs text-muted-foreground">1,234명 응답 (신뢰도 95%)</p>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-6">
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-sm text-muted-foreground">개선 필요 항목</span>
                <AlertTriangle className="h-4 w-4 text-amber-500" />
              </div>
              <div className="text-2xl font-bold">{reportData.issues.length}개</div>
              <p className="text-xs text-muted-foreground">
                우선순위 높음: {reportData.issues.filter((i) => i.severity === "높음").length}개
              </p>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* 수요 분석 */}
      <Card>
        <CardHeader>
          <h2 className="text-xl font-heading font-semibold">시민 운동 수요 분석</h2>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {Object.entries(reportData.demand).map(([sport, percentage]) => (
              <div key={sport} className="space-y-2">
                <div className="flex justify-between items-center">
                  <span className="font-medium">
                    {sport === "swimming" && "수영"}
                    {sport === "fitness" && "헬스/피트니스"}
                    {sport === "tennis" && "테니스"}
                    {sport === "golf" && "골프"}
                    {sport === "others" && "기타"}
                  </span>
                  <span className="text-sm text-muted-foreground">{percentage}%</span>
                </div>
                <div className="w-full bg-muted rounded-full h-2">
                  <div
                    className="bg-primary h-2 rounded-full transition-all duration-500"
                    style={{ width: `${percentage}%` }}
                  ></div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* 주요 이슈 */}
      <Card>
        <CardHeader>
          <h2 className="text-xl font-heading font-semibold">주요 개선 과제</h2>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {reportData.issues.map((issue, index) => (
              <div key={index} className="flex items-start gap-4 p-4 rounded-lg border">
                <div
                  className={`h-2 w-2 rounded-full mt-2 ${
                    issue.severity === "높음"
                      ? "bg-red-500"
                      : issue.severity === "중간"
                        ? "bg-amber-500"
                        : "bg-green-500"
                  }`}
                ></div>
                <div className="flex-1 space-y-1">
                  <div className="flex items-center gap-2">
                    <span className="font-medium">
                      {issue.facility} {issue.type}
                    </span>
                    <Badge
                      variant={
                        issue.severity === "높음" ? "destructive" : issue.severity === "중간" ? "default" : "secondary"
                      }
                      className="text-xs"
                    >
                      {issue.severity}
                    </Badge>
                  </div>
                  <p className="text-sm text-muted-foreground">{issue.impact}</p>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
