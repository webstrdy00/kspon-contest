import { Button } from "@/components/ui/button"
import { BarChart3, Map, FileText, MessageSquare, Settings, Home } from "lucide-react"

const navigation = [
  { name: "대시보드", href: "/", icon: Home, current: false },
  { name: "인터랙티브 맵", href: "/dashboard", icon: Map, current: false },
  { name: "데이터 분석", href: "/analytics", icon: BarChart3, current: false },
  { name: "우리 동네 리포트", href: "/reports", icon: FileText, current: false },
  { name: "정책 제안", href: "/proposals", icon: MessageSquare, current: true }, // Updated current state for proposals page
  { name: "설정", href: "/settings", icon: Settings, current: false },
]

export function Sidebar() {
  return (
    <div className="w-64 border-r border-border bg-card">
      <nav className="flex flex-col gap-2 p-4">
        {navigation.map((item) => (
          <Button key={item.name} variant={item.current ? "default" : "ghost"} className="justify-start gap-3 h-10">
            <item.icon className="h-4 w-4" />
            {item.name}
          </Button>
        ))}
      </nav>

      <div className="mt-8 p-4">
        <div className="rounded-lg bg-muted p-4">
          <h3 className="font-heading font-semibold text-sm mb-2">최근 업데이트</h3>
          <p className="text-xs text-muted-foreground mb-3">2024년 체육시설 현황 데이터가 업데이트되었습니다.</p>
          <Button size="sm" variant="outline" className="w-full bg-transparent">
            자세히 보기
          </Button>
        </div>
      </div>
    </div>
  )
}
