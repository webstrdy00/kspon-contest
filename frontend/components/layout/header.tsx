"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { Badge } from "@/components/ui/badge"
import { Search, Bell, User, Settings, LogOut, Award, Heart, FileText } from "lucide-react"

export function Header() {
  const [isLoggedIn, setIsLoggedIn] = useState(true) // Mock login state
  const [user] = useState({
    name: "김체육",
    email: "kim@example.com",
    avatar: "",
    badges: ["데이터 전문가", "정책 제안왕"],
    stats: {
      proposals: 12,
      likes: 247,
      reports: 5,
    },
  })

  return (
    <header className="border-b border-border bg-card">
      <div className="flex h-16 items-center justify-between px-6">
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-3">
            <div className="relative">
              <svg
                width="32"
                height="32"
                viewBox="0 0 32 32"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
                className="text-primary"
              >
                <rect width="32" height="32" rx="8" fill="currentColor" className="opacity-10" />
                <path d="M8 12h4v8h-4v-8zm6-4h4v12h-4V8zm6 6h4v6h-4v-6z" fill="currentColor" className="opacity-80" />
                <circle cx="10" cy="8" r="2" fill="currentColor" />
                <circle cx="16" cy="6" r="2" fill="currentColor" />
                <circle cx="22" cy="10" r="2" fill="currentColor" />
              </svg>
            </div>
            <div className="flex flex-col">
              <h1 className="font-heading font-bold text-lg text-foreground leading-none">스포츠 데이터랩</h1>
              <span className="text-xs text-muted-foreground font-medium">Sports Data Lab</span>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-4">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
            <input
              type="search"
              placeholder="지역, 시설, 정책 검색..."
              className="h-9 w-64 rounded-md border border-input bg-background pl-9 pr-3 text-sm placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring"
            />
          </div>

          {isLoggedIn ? (
            <>
              <Button variant="ghost" size="icon" className="relative">
                <Bell className="h-4 w-4" />
                <span className="absolute -top-1 -right-1 h-3 w-3 bg-destructive rounded-full text-xs flex items-center justify-center text-white">
                  3
                </span>
              </Button>

              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="ghost" className="relative h-8 w-8 rounded-full">
                    <Avatar className="h-8 w-8">
                      <AvatarImage src={user.avatar || "/placeholder.svg"} alt={user.name} />
                      <AvatarFallback>{user.name.charAt(0)}</AvatarFallback>
                    </Avatar>
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent className="w-80" align="end" forceMount>
                  <DropdownMenuLabel className="font-normal">
                    <div className="flex flex-col space-y-2">
                      <div className="flex items-center gap-3">
                        <Avatar className="h-12 w-12">
                          <AvatarImage src={user.avatar || "/placeholder.svg"} alt={user.name} />
                          <AvatarFallback className="text-lg">{user.name.charAt(0)}</AvatarFallback>
                        </Avatar>
                        <div>
                          <p className="text-sm font-medium leading-none">{user.name}</p>
                          <p className="text-xs leading-none text-muted-foreground mt-1">{user.email}</p>
                        </div>
                      </div>
                      <div className="flex flex-wrap gap-1">
                        {user.badges.map((badge) => (
                          <Badge key={badge} variant="secondary" className="text-xs">
                            {badge}
                          </Badge>
                        ))}
                      </div>
                      <div className="grid grid-cols-3 gap-2 text-center text-xs">
                        <div>
                          <div className="font-medium">{user.stats.proposals}</div>
                          <div className="text-muted-foreground">제안</div>
                        </div>
                        <div>
                          <div className="font-medium">{user.stats.likes}</div>
                          <div className="text-muted-foreground">공감</div>
                        </div>
                        <div>
                          <div className="font-medium">{user.stats.reports}</div>
                          <div className="text-muted-foreground">리포트</div>
                        </div>
                      </div>
                    </div>
                  </DropdownMenuLabel>
                  <DropdownMenuSeparator />
                  <DropdownMenuItem>
                    <User className="mr-2 h-4 w-4" />
                    <span>프로필</span>
                  </DropdownMenuItem>
                  <DropdownMenuItem>
                    <FileText className="mr-2 h-4 w-4" />
                    <span>내 제안</span>
                  </DropdownMenuItem>
                  <DropdownMenuItem>
                    <Heart className="mr-2 h-4 w-4" />
                    <span>공감한 제안</span>
                  </DropdownMenuItem>
                  <DropdownMenuItem>
                    <Award className="mr-2 h-4 w-4" />
                    <span>배지 및 성과</span>
                  </DropdownMenuItem>
                  <DropdownMenuItem>
                    <Settings className="mr-2 h-4 w-4" />
                    <span>설정</span>
                  </DropdownMenuItem>
                  <DropdownMenuSeparator />
                  <DropdownMenuItem onClick={() => setIsLoggedIn(false)}>
                    <LogOut className="mr-2 h-4 w-4" />
                    <span>로그아웃</span>
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            </>
          ) : (
            <div className="flex items-center gap-2">
              <Button variant="ghost" onClick={() => setIsLoggedIn(true)}>
                로그인
              </Button>
              <Button>회원가입</Button>
            </div>
          )}
        </div>
      </div>
    </header>
  )
}
