import { Card, CardContent, CardHeader } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Lightbulb, Target, Clock, DollarSign, Users, TrendingUp, CheckCircle } from "lucide-react"

interface RegionalRecommendationsProps {
  region: string
}

export function RegionalRecommendations({ region }: RegionalRecommendationsProps) {
  const recommendations = {
    region: decodeURIComponent(region),
    priority: [
      {
        id: 1,
        title: "수영장 신설 및 확충",
        description: "시민 수요가 가장 높은 수영 시설의 부족 문제를 해결하기 위한 우선 과제",
        priority: "높음",
        timeline: "12-18개월",
        budget: "15억원",
        expectedUsers: "연간 25,000명",
        impact: {
          satisfaction: "+12%",
          usage: "+35%",
          health: "의료비 절감 2.1억원/년",
        },
        steps: ["부지 선정 및 타당성 조사 (3개월)", "설계 및 인허가 (6개월)", "건설 및 시설 구축 (9개월)"],
        feasibility: 85,
      },
      {
        id: 2,
        title: "기존 체육관 리모델링",
        description: "노후화된 체육관의 현대화를 통한 이용률 및 만족도 향상",
        priority: "중간",
        timeline: "6-9개월",
        budget: "8억원",
        expectedUsers: "연간 18,000명",
        impact: {
          satisfaction: "+8%",
          usage: "+25%",
          efficiency: "+15%",
        },
        steps: ["시설 진단 및 설계 (2개월)", "단계별 리모델링 (6개월)", "재개장 및 프로그램 운영 (1개월)"],
        feasibility: 92,
      },
      {
        id: 3,
        title: "생활체육 프로그램 다양화",
        description: "연령대별, 관심사별 맞춤형 프로그램 개발로 참여율 증대",
        priority: "중간",
        timeline: "3-6개월",
        budget: "2억원",
        expectedUsers: "연간 12,000명",
        impact: {
          satisfaction: "+6%",
          participation: "+40%",
          community: "지역 결속력 강화",
        },
        steps: ["수요 조사 및 프로그램 기획 (1개월)", "강사 모집 및 교육 (2개월)", "프로그램 런칭 및 운영 (3개월)"],
        feasibility: 95,
      },
    ],
    quickWins: [
      {
        title: "운영시간 연장",
        description: "기존 시설의 운영시간을 연장하여 접근성 개선",
        timeline: "1개월",
        cost: "저비용",
        impact: "이용률 +20%",
      },
      {
        title: "온라인 예약 시스템",
        description: "디지털 예약 시스템 도입으로 편의성 향상",
        timeline: "2개월",
        cost: "저비용",
        impact: "만족도 +15%",
      },
      {
        title: "시설 안내 개선",
        description: "표지판 및 안내 시설 현대화",
        timeline: "1개월",
        cost: "저비용",
        impact: "접근성 +10%",
      },
    ],
    longTerm: [
      {
        title: "스포츠 복합단지 조성",
        description: "대규모 종합 스포츠 시설 건립",
        timeline: "3-5년",
        impact: "지역 랜드마크화",
      },
      {
        title: "스마트 체육시설 구축",
        description: "IoT 기반 스마트 관리 시스템 도입",
        timeline: "2-3년",
        impact: "운영 효율성 극대화",
      },
    ],
  }

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case "높음":
        return "destructive"
      case "중간":
        return "default"
      case "낮음":
        return "secondary"
      default:
        return "outline"
    }
  }

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <div className="flex items-center gap-2">
            <Lightbulb className="h-5 w-5 text-primary" />
            <h2 className="text-xl font-heading font-semibold">정책 제안</h2>
          </div>
          <p className="text-sm text-muted-foreground">
            {recommendations.region}의 체육환경 개선을 위한 구체적인 실행 방안을 제시합니다
          </p>
        </CardHeader>
      </Card>

      {/* 우선순위 제안 */}
      <div className="space-y-4">
        <h3 className="font-heading font-semibold flex items-center gap-2">
          <Target className="h-4 w-4" />
          우선순위 제안
        </h3>
        {recommendations.priority.map((rec) => (
          <Card key={rec.id}>
            <CardHeader>
              <div className="flex items-start justify-between">
                <div className="space-y-2">
                  <div className="flex items-center gap-2">
                    <h4 className="font-medium">{rec.title}</h4>
                    <Badge variant={getPriorityColor(rec.priority)}>{rec.priority}</Badge>
                  </div>
                  <p className="text-sm text-muted-foreground">{rec.description}</p>
                </div>
                <div className="text-right">
                  <div className="font-bold text-lg text-primary">{rec.feasibility}%</div>
                  <div className="text-xs text-muted-foreground">실현가능성</div>
                </div>
              </div>
            </CardHeader>
            <CardContent className="space-y-4">
              {/* 기본 정보 */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="flex items-center gap-2">
                  <Clock className="h-4 w-4 text-muted-foreground" />
                  <div>
                    <div className="text-sm font-medium">{rec.timeline}</div>
                    <div className="text-xs text-muted-foreground">소요기간</div>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <DollarSign className="h-4 w-4 text-muted-foreground" />
                  <div>
                    <div className="text-sm font-medium">{rec.budget}</div>
                    <div className="text-xs text-muted-foreground">예상예산</div>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <Users className="h-4 w-4 text-muted-foreground" />
                  <div>
                    <div className="text-sm font-medium">{rec.expectedUsers}</div>
                    <div className="text-xs text-muted-foreground">예상이용자</div>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <TrendingUp className="h-4 w-4 text-muted-foreground" />
                  <div>
                    <div className="text-sm font-medium">다중 효과</div>
                    <div className="text-xs text-muted-foreground">복합 개선</div>
                  </div>
                </div>
              </div>

              {/* 예상 효과 */}
              <div className="space-y-2">
                <h5 className="font-medium text-sm">예상 효과</h5>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-2">
                  {Object.entries(rec.impact).map(([key, value]) => (
                    <Badge key={key} variant="secondary" className="justify-center">
                      {key === "satisfaction" && "만족도 "}
                      {key === "usage" && "이용률 "}
                      {key === "health" && "건강 "}
                      {key === "efficiency" && "효율성 "}
                      {key === "participation" && "참여율 "}
                      {key === "community" && ""}
                      {value}
                    </Badge>
                  ))}
                </div>
              </div>

              {/* 실행 단계 */}
              <div className="space-y-2">
                <h5 className="font-medium text-sm">실행 단계</h5>
                <div className="space-y-2">
                  {rec.steps.map((step, index) => (
                    <div key={index} className="flex items-center gap-2 text-sm">
                      <div className="h-6 w-6 rounded-full bg-primary/10 flex items-center justify-center text-xs font-medium">
                        {index + 1}
                      </div>
                      <span>{step}</span>
                    </div>
                  ))}
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* 빠른 개선 방안 */}
      <Card>
        <CardHeader>
          <h3 className="font-heading font-semibold flex items-center gap-2">
            <CheckCircle className="h-4 w-4" />
            빠른 개선 방안 (Quick Wins)
          </h3>
          <p className="text-sm text-muted-foreground">단기간에 실행 가능하고 즉시 효과를 볼 수 있는 개선 방안</p>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {recommendations.quickWins.map((win, index) => (
              <div key={index} className="p-4 rounded-lg border">
                <h4 className="font-medium mb-2">{win.title}</h4>
                <p className="text-sm text-muted-foreground mb-3">{win.description}</p>
                <div className="space-y-1 text-xs">
                  <div className="flex justify-between">
                    <span>기간:</span>
                    <span className="font-medium">{win.timeline}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>비용:</span>
                    <span className="font-medium">{win.cost}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>효과:</span>
                    <span className="font-medium text-green-600">{win.impact}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* 장기 비전 */}
      <Card>
        <CardHeader>
          <h3 className="font-heading font-semibold">장기 비전</h3>
          <p className="text-sm text-muted-foreground">미래 지향적 체육환경 조성을 위한 장기 계획</p>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {recommendations.longTerm.map((plan, index) => (
              <div key={index} className="flex items-start gap-4 p-4 rounded-lg border">
                <div className="h-8 w-8 rounded-full bg-primary/10 flex items-center justify-center text-sm font-medium">
                  {index + 1}
                </div>
                <div className="flex-1">
                  <h4 className="font-medium">{plan.title}</h4>
                  <p className="text-sm text-muted-foreground mt-1">{plan.description}</p>
                  <div className="flex items-center gap-4 mt-2 text-xs text-muted-foreground">
                    <span>기간: {plan.timeline}</span>
                    <span>•</span>
                    <span>효과: {plan.impact}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      <div className="text-center">
        <Button size="lg">정책 제안서 전체 다운로드</Button>
      </div>
    </div>
  )
}
