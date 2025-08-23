import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Download, Share2, RefreshCw } from "lucide-react"

export function DashboardHeader() {
  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="font-heading font-bold text-3xl">인터랙티브 대시보드</h1>
          <p className="text-muted-foreground mt-1">
            전국 체육시설 데이터를 탐색하고 분석하여 정책 인사이트를 발견하세요
          </p>
        </div>
        <div className="flex items-center gap-2">
          <Button variant="outline" size="sm">
            <RefreshCw className="h-4 w-4 mr-2" />
            데이터 새로고침
          </Button>
          <Button variant="outline" size="sm">
            <Download className="h-4 w-4 mr-2" />
            내보내기
          </Button>
          <Button variant="outline" size="sm">
            <Share2 className="h-4 w-4 mr-2" />
            공유
          </Button>
        </div>
      </div>

      <Card>
        <CardContent className="p-4">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 text-center">
            <div>
              <div className="text-2xl font-bold text-primary">24,567</div>
              <div className="text-sm text-muted-foreground">전국 체육시설</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-chart-2">1,847억원</div>
              <div className="text-sm text-muted-foreground">연간 투입 예산</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-chart-3">89%</div>
              <div className="text-sm text-muted-foreground">시설 가동률</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-chart-4">156개</div>
              <div className="text-sm text-muted-foreground">수요 부족 지역</div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
