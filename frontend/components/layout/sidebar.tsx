"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { Button } from "@/components/ui/button"
import { BarChart3, Map, FileText, MessageSquare, Home, TrendingUp } from "lucide-react"

const navigation = [
  { name: "홈", href: "/", icon: Home },
  { name: "인터랙티브 대시보드", href: "/dashboard", icon: Map },
  { name: "예산-성과 분석", href: "/dashboard/budget-performance", icon: TrendingUp },
  { name: "우리 동네 리포트", href: "/reports", icon: FileText },
  { name: "정책 제안", href: "/proposals", icon: MessageSquare },
  { name: "통계", href: "/stats", icon: BarChart3 },
]

export function Sidebar() {
  const pathname = usePathname()
  
  return (
    <div className="w-64 border-r border-border bg-card">
      <nav className="flex flex-col gap-2 p-4">
        {navigation.map((item) => {
          const isActive = pathname === item.href || (item.href !== "/" && pathname.startsWith(item.href))
          return (
            <Link key={item.name} href={item.href}>
              <Button variant={isActive ? "default" : "ghost"} className="w-full justify-start gap-3 h-10">
                <item.icon className="h-4 w-4" />
                {item.name}
              </Button>
            </Link>
          )
        })}
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
