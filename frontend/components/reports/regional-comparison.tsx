import { Card, CardContent, CardHeader } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { TrendingUp, TrendingDown, Minus, MapPin } from "lucide-react"

interface RegionalComparisonProps {
  region: string
}

export function RegionalComparison({ region }: RegionalComparisonProps) {
  const comparisonData = {
    region: decodeURIComponent(region),
    comparisons: [
      {
        type: "전국 평균",
        metrics: [
          { name: "체육시설 수", value: 45, comparison: 52, trend: "down", diff: -13.5 },
          { name: "예산 효율성", value: 78.5, comparison: 82.1, trend: "down", diff: -4.4 },
          { name: "시민 만족도", value: 72.4, comparison: 75.8, trend: "down", diff: -4.5 },
          { name: "이용률", value: 68.2, comparison: 71.3, trend: "down", diff: -4.3 },
        ],
      },
      {
        type: "인접 지역",
        regions: ["서초구", "송파구", "영등포구"],
        metrics: [
          { name: "체육시설 수", value: 45, comparison: 48, trend: "down", diff: -6.3 },
          { name: "예산 효율성", value: 78.5, comparison: 81.2, trend: "down", diff: -3.3 },
          { name: "시민 만족도", value: 72.4, comparison: 74.1, trend: "down", diff: -2.3 },
          { name: "이용률", value: 68.2, comparison: 69.8, trend: "down", diff: -2.3 },
        ],
      },
      {
        type: "유사 지역",
        description: "인구 규모 및 도시 특성이 유사한 지역",
        regions: ["부산 해운대구", "대구 수성구", "인천 연수구"],
        metrics: [
          { name: "체육시설 수", value: 45, comparison: 43, trend: "up", diff: 4.7 },
          { name: "예산 효율성", value: 78.5, comparison: 76.8, trend: "up", diff: 2.2 },
          { name: "시민 만족도", value: 72.4, comparison: 70.9, trend: "up", diff: 2.1 },
          { name: "이용률", value: 68.2, comparison: 66.5, trend: "up", diff: 2.6 },
        ],
      },
    ],
    benchmarks: [
      {
        region: "서초구",
        score: 89.2,
        strengths: ["높은 예산 효율성", "우수한 시설 접근성"],
        isTop: true,
      },
      {
        region: "송파구",
        score: 87.8,
        strengths: ["다양한 프로그램", "높은 시민 참여율"],
        isTop: true,
      },
      {
        region: "마포구",
        score: 85.4,
        strengths: ["혁신적 운영", "지역 특성 반영"],
        isTop: true,
      },
    ],
  }

  const getTrendIcon = (trend: string) => {
    switch (trend) {
      case "up":
        return <TrendingUp className="h-4 w-4 text-green-500" />
      case "down":
        return <TrendingDown className="h-4 w-4 text-red-500" />
      default:
        return <Minus className="h-4 w-4 text-gray-500" />
    }
  }

  const getTrendColor = (trend: string) => {
    switch (trend) {
      case "up":
        return "text-green-600"
      case "down":
        return "text-red-600"
      default:
        return "text-gray-600"
    }
  }

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <h2 className="text-xl font-heading font-semibold">지역 비교 분석</h2>
          <p className="text-sm text-muted-foreground">
            {comparisonData.region}의 체육환경을 다양한 기준으로 비교 분석합니다
          </p>
        </CardHeader>
        <CardContent className="space-y-6">
          {comparisonData.comparisons.map((comparison, index) => (
            <div key={index} className="space-y-4">
              <div className="flex items-center justify-between">
                <h3 className="font-medium">{comparison.type}</h3>
                {comparison.regions && (
                  <div className="flex items-center gap-1">
                    <MapPin className="h-3 w-3 text-muted-foreground" />
                    <span className="text-xs text-muted-foreground">{comparison.regions.join(", ")}</span>
                  </div>
                )}
              </div>

              {comparison.description && <p className="text-sm text-muted-foreground">{comparison.description}</p>}

              <div className="grid grid-cols-1 gap-3">
                {comparison.metrics.map((metric, metricIndex) => (
                  <div key={metricIndex} className="flex items-center justify-between p-3 rounded-lg border">
                    <div className="flex items-center gap-3">
                      {getTrendIcon(metric.trend)}
                      <span className="font-medium text-sm">{metric.name}</span>
                    </div>
                    <div className="flex items-center gap-3">
                      <div className="text-right">
                        <div className="font-medium">{metric.value}</div>
                        <div className="text-xs text-muted-foreground">vs {metric.comparison}</div>
                      </div>
                      <Badge
                        variant={
                          metric.trend === "up" ? "default" : metric.trend === "down" ? "destructive" : "secondary"
                        }
                        className="text-xs"
                      >
                        {metric.diff > 0 ? "+" : ""}
                        {metric.diff.toFixed(1)}%
                      </Badge>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </CardContent>
      </Card>

      {/* 벤치마크 지역 */}
      <Card>
        <CardHeader>
          <h3 className="font-heading font-semibold">벤치마크 지역</h3>
          <p className="text-sm text-muted-foreground">체육환경 우수 지역의 성공 사례를 참고하세요</p>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {comparisonData.benchmarks.map((benchmark, index) => (
              <div key={index} className="p-4 rounded-lg border hover:bg-muted/50 transition-colors">
                <div className="flex items-start justify-between mb-3">
                  <div className="flex items-center gap-2">
                    <h4 className="font-medium">{benchmark.region}</h4>
                    {benchmark.isTop && (
                      <Badge variant="default" className="text-xs">
                        TOP 3
                      </Badge>
                    )}
                  </div>
                  <div className="text-right">
                    <div className="font-bold text-lg text-primary">{benchmark.score}</div>
                    <div className="text-xs text-muted-foreground">종합점수</div>
                  </div>
                </div>
                <div className="space-y-1">
                  <p className="text-sm font-medium">주요 강점:</p>
                  <div className="flex flex-wrap gap-1">
                    {benchmark.strengths.map((strength, strengthIndex) => (
                      <Badge key={strengthIndex} variant="secondary" className="text-xs">
                        {strength}
                      </Badge>
                    ))}
                  </div>
                </div>
              </div>
            ))}
          </div>
          <div className="mt-4 text-center">
            <Button variant="outline" size="sm">
              벤치마크 상세 분석 보기
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
