import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { Plus } from "lucide-react"

export function ProposalHeader() {
  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="font-heading font-bold text-3xl">정책 제안</h1>
          <p className="text-muted-foreground mt-1">
            데이터를 근거로 체육 정책 개선 아이디어를 제안하고, 시민들과 함께 토론해보세요
          </p>
        </div>
        <Button size="lg" className="gap-2">
          <Plus className="h-4 w-4" />새 제안 작성
        </Button>
      </div>

      <Card>
        <CardContent className="p-4">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 text-center">
            <div>
              <div className="text-2xl font-bold text-primary">1,234</div>
              <div className="text-sm text-muted-foreground">총 제안 수</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-chart-2">156</div>
              <div className="text-sm text-muted-foreground">정책 반영</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-chart-4">89%</div>
              <div className="text-sm text-muted-foreground">시민 참여율</div>
            </div>
            <div>
              <div className="text-2xl font-bold text-chart-5">4.2</div>
              <div className="text-sm text-muted-foreground">평균 평점</div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
