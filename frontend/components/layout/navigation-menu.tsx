"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { cn } from "@/lib/utils"
import { Home, BarChart3, FileText, MessageSquare, TrendingUp, HelpCircle } from "lucide-react"

const menuItems = [
  {
    title: "홈",
    href: "/",
    icon: Home,
    description: "메인 페이지",
  },
  {
    title: "대시보드",
    href: "/dashboard",
    icon: BarChart3,
    description: "데이터 시각화",
  },
  {
    title: "지역 리포트",
    href: "/reports",
    icon: FileText,
    description: "우리 동네 분석",
  },
  {
    title: "정책 제안",
    href: "/proposals",
    icon: MessageSquare,
    description: "시민 제안",
  },
  {
    title: "통계",
    href: "/stats",
    icon: TrendingUp,
    description: "플랫폼 현황",
  },
  {
    title: "도움말",
    href: "/help",
    icon: HelpCircle,
    description: "사용 가이드",
  },
]

export function NavigationMenu() {
  const pathname = usePathname()

  return (
    <nav className="border-b border-border bg-card/50">
      <div className="px-6">
        <div className="flex items-center space-x-8">
          {menuItems.map((item) => {
            const Icon = item.icon
            const isActive = pathname === item.href || (item.href !== "/" && pathname.startsWith(item.href))

            return (
              <Link
                key={item.href}
                href={item.href}
                className={cn(
                  "flex items-center gap-2 py-4 text-sm font-medium transition-colors hover:text-primary relative",
                  isActive ? "text-primary" : "text-muted-foreground hover:text-foreground",
                )}
              >
                <Icon className="h-4 w-4" />
                <span>{item.title}</span>
                {isActive && <div className="absolute bottom-0 left-0 right-0 h-0.5 bg-primary rounded-full" />}
              </Link>
            )
          })}
        </div>
      </div>
    </nav>
  )
}
