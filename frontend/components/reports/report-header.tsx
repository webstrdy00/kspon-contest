import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Share2, History } from "lucide-react"

export function ReportHeader() {
  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="font-heading font-bold text-3xl">우리 동네 리포트</h1>
          <p className="text-muted-foreground mt-1">
            내 지역의 체육 환경을 종합적으로 분석한 맞춤형 리포트를 생성하세요
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="outline" size="sm">
            <History className="h-4 w-4 mr-2" />
            이전 리포트
          </Button>
          <Button variant="outline" size="sm">
            <Share2 className="h-4 w-4 mr-2" />
            공유하기
          </Button>
        </div>
      </div>

      <Card>
        <CardContent className="p-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-center">
            <div>
              <div className="text-2xl font-bold text-primary">247</div>
              <div className="text-sm text-muted-foreground">생성된 리포트</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-chart-2">89%</div>
              <div className="text-sm text-muted-foreground">사용자 만족도</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-chart-4">156</div>
              <div className="text-sm text-muted-foreground">정책 반영 건수</div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
