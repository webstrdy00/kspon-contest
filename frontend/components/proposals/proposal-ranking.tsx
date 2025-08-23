"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import {
  Trophy,
  TrendingUp,
  Heart,
  MessageCircle,
  Crown,
  Medal,
  Award,
  Star,
  Users,
  BarChart3,
  Zap,
  CheckCircle,
} from "lucide-react"

const topProposals = [
  {
    id: 1,
    rank: 1,
    title: "부산 해운대구 해변 운동기구 설치 제안",
    author: "박시민",
    likes: 257,
    comments: 31,
    category: "시설 확충",
    trend: "up",
    dataEvidence: ["인구밀도 분석", "수요조사 결과"],
    implementationStatus: "검토중",
    region: "부산광역시",
    weeklyGrowth: 45,
    authorBadges: ["데이터 분석가", "시민 참여상"],
  },
  {
    id: 2,
    rank: 2,
    title: "마포구 홍대 인근 실내 클라이밍짐 신설 제안",
    author: "김체육",
    likes: 189,
    comments: 23,
    category: "시설 확충",
    trend: "up",
    dataEvidence: ["20대 수요 분석", "기존 시설 부족 현황"],
    implementationStatus: "정책 반영",
    region: "서울특별시",
    weeklyGrowth: 32,
    authorBadges: ["정책 제안왕", "우수 시민"],
  },
  {
    id: 3,
    rank: 3,
    title: "강남구 테니스장 이용 시간 확대 요청",
    author: "이정책",
    likes: 134,
    comments: 15,
    category: "운영 개선",
    trend: "stable",
    dataEvidence: ["이용률 분석", "주민 설문조사"],
    implementationStatus: "시범 운영",
    region: "서울특별시",
    weeklyGrowth: 8,
    authorBadges: ["아이디어 뱅크"],
  },
  {
    id: 4,
    rank: 4,
    title: "대전 유성구 파크골프장 확충 제안",
    author: "최골프",
    likes: 98,
    comments: 19,
    category: "시설 확충",
    trend: "up",
    dataEvidence: ["고령 인구 분석", "기존 시설 포화도"],
    implementationStatus: "예산 검토",
    region: "대전광역시",
    weeklyGrowth: 28,
    authorBadges: ["신규 제안자"],
  },
  {
    id: 5,
    rank: 5,
    title: "인천 연수구 수영장 접근성 개선 방안",
    author: "수영사랑",
    likes: 87,
    comments: 12,
    category: "접근성 개선",
    trend: "up",
    dataEvidence: ["교통 접근성 분석", "장애인 이용 현황"],
    implementationStatus: "검토중",
    region: "인천광역시",
    weeklyGrowth: 15,
    authorBadges: ["접근성 전문가"],
  },
]

const topContributors = [
  {
    name: "김체육",
    proposals: 12,
    totalLikes: 1247,
    badges: ["데이터 전문가", "정책 제안왕", "우수 시민"],
    level: "플래티넘",
    points: 2450,
    successRate: 75,
    specialties: ["시설 확충", "운영 개선"],
    joinDate: "2023.03",
    recentAchievement: "정책 반영 5건 달성",
  },
  {
    name: "박시민",
    proposals: 8,
    totalLikes: 892,
    badges: ["시민 참여상", "데이터 분석가"],
    level: "골드",
    points: 1680,
    successRate: 62,
    specialties: ["접근성 개선", "예산 효율성"],
    joinDate: "2023.07",
    recentAchievement: "주간 1위 달성",
  },
  {
    name: "이정책",
    proposals: 15,
    totalLikes: 756,
    badges: ["아이디어 뱅크", "지속 참여자"],
    level: "실버",
    points: 1420,
    successRate: 53,
    specialties: ["운영 개선", "프로그램 제안"],
    joinDate: "2023.01",
    recentAchievement: "제안 15건 달성",
  },
]

const badgeSystem = {
  levels: [
    { name: "브론즈", minPoints: 0, color: "bg-amber-600", benefits: ["기본 제안 권한"] },
    { name: "실버", minPoints: 500, color: "bg-gray-400", benefits: ["우선 검토", "월간 리포트"] },
    { name: "골드", minPoints: 1500, color: "bg-yellow-500", benefits: ["정책 자문 참여", "전문가 매칭"] },
    { name: "플래티넘", minPoints: 2000, color: "bg-blue-500", benefits: ["정책 결정 참여", "VIP 지원"] },
  ],
  achievements: [
    { name: "첫 제안", icon: "🎯", description: "첫 번째 정책 제안 작성" },
    { name: "인기 제안", icon: "❤️", description: "100개 이상 공감 받기" },
    { name: "데이터 전문가", icon: "📊", description: "데이터 근거 제시 10회" },
    { name: "정책 제안왕", icon: "👑", description: "정책 반영 5건 달성" },
    { name: "시민 참여상", icon: "🏆", description: "월간 1위 달성" },
  ],
}

export function ProposalRanking() {
  const [timeRange, setTimeRange] = useState("weekly")
  const [category, setCategory] = useState("all")
  const [selectedProposal, setSelectedProposal] = useState<number | null>(null)

  const getRankIcon = (rank: number) => {
    switch (rank) {
      case 1:
        return <Crown className="h-5 w-5 text-yellow-500" />
      case 2:
        return <Medal className="h-5 w-5 text-gray-400" />
      case 3:
        return <Award className="h-5 w-5 text-amber-600" />
      default:
        return <span className="font-bold text-lg text-muted-foreground">{rank}</span>
    }
  }

  const getLevelColor = (level: string) => {
    const levelData = badgeSystem.levels.find((l) => l.name === level)
    return levelData?.color || "bg-gray-400"
  }

  const getImplementationStatusColor = (status: string) => {
    switch (status) {
      case "정책 반영":
        return "bg-green-500"
      case "시범 운영":
        return "bg-blue-500"
      case "예산 검토":
        return "bg-yellow-500"
      case "검토중":
        return "bg-orange-500"
      default:
        return "bg-gray-500"
    }
  }

  return (
    <div className="space-y-6">
      <Tabs defaultValue="rankings" className="w-full">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="rankings">인기 제안</TabsTrigger>
          <TabsTrigger value="contributors">우수 제안자</TabsTrigger>
          <TabsTrigger value="badges">배지 시스템</TabsTrigger>
          <TabsTrigger value="analytics">참여 분석</TabsTrigger>
        </TabsList>

        <TabsContent value="rankings" className="space-y-6">
          {/* Enhanced Filters */}
          <div className="flex items-center gap-4">
            <Select value={timeRange} onValueChange={setTimeRange}>
              <SelectTrigger className="w-40">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="weekly">이번 주</SelectItem>
                <SelectItem value="monthly">이번 달</SelectItem>
                <SelectItem value="quarterly">이번 분기</SelectItem>
                <SelectItem value="yearly">올해</SelectItem>
              </SelectContent>
            </Select>

            <Select value={category} onValueChange={setCategory}>
              <SelectTrigger className="w-40">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">전체 카테고리</SelectItem>
                <SelectItem value="시설 확충">시설 확충</SelectItem>
                <SelectItem value="운영 개선">운영 개선</SelectItem>
                <SelectItem value="접근성 개선">접근성 개선</SelectItem>
                <SelectItem value="프로그램 제안">프로그램 제안</SelectItem>
              </SelectContent>
            </Select>
          </div>

          {/* Enhanced Top Proposals */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Trophy className="h-5 w-5 text-yellow-500" />
                {timeRange === "weekly" ? "이번 주" : timeRange === "monthly" ? "이번 달" : "이번 분기"} 인기 제안 TOP 5
              </CardTitle>
              <CardDescription>데이터 근거와 함께 가장 많은 공감을 받은 제안들입니다</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {topProposals.map((proposal) => (
                  <div
                    key={proposal.id}
                    className={`p-4 border rounded-lg hover:shadow-md transition-all cursor-pointer ${
                      selectedProposal === proposal.id ? "border-primary bg-primary/5" : ""
                    }`}
                    onClick={() => setSelectedProposal(selectedProposal === proposal.id ? null : proposal.id)}
                  >
                    <div className="flex items-start gap-4">
                      <div className="flex items-center justify-center w-12 h-12 rounded-full bg-muted">
                        {getRankIcon(proposal.rank)}
                      </div>
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-2">
                          <Badge variant="outline">{proposal.category}</Badge>
                          <Badge variant="secondary">{proposal.region}</Badge>
                          <div
                            className={`w-2 h-2 rounded-full ${getImplementationStatusColor(proposal.implementationStatus)}`}
                          ></div>
                          <span className="text-xs text-muted-foreground">{proposal.implementationStatus}</span>
                          {proposal.trend === "up" && (
                            <div className="flex items-center gap-1 text-green-600">
                              <TrendingUp className="h-3 w-3" />
                              <span className="text-xs">+{proposal.weeklyGrowth}</span>
                            </div>
                          )}
                        </div>
                        <h3 className="font-medium hover:text-primary transition-colors mb-1">{proposal.title}</h3>
                        <div className="flex items-center gap-4 text-sm text-muted-foreground">
                          <span>by {proposal.author}</span>
                          <div className="flex gap-1">
                            {proposal.authorBadges.slice(0, 2).map((badge) => (
                              <Badge key={badge} variant="secondary" className="text-xs">
                                {badge}
                              </Badge>
                            ))}
                          </div>
                        </div>
                      </div>
                      <div className="flex items-center gap-4 text-sm">
                        <div className="flex items-center gap-1">
                          <Heart className="h-4 w-4 text-red-500" />
                          {proposal.likes}
                        </div>
                        <div className="flex items-center gap-1">
                          <MessageCircle className="h-4 w-4 text-blue-500" />
                          {proposal.comments}
                        </div>
                      </div>
                    </div>

                    {selectedProposal === proposal.id && (
                      <div className="mt-4 pt-4 border-t space-y-3">
                        <div>
                          <h4 className="font-medium text-sm mb-2">데이터 근거</h4>
                          <div className="flex gap-2">
                            {proposal.dataEvidence.map((evidence) => (
                              <Badge key={evidence} variant="outline" className="text-xs">
                                <BarChart3 className="h-3 w-3 mr-1" />
                                {evidence}
                              </Badge>
                            ))}
                          </div>
                        </div>
                        <div className="flex items-center justify-between">
                          <div className="text-sm">
                            <span className="text-muted-foreground">진행 상황:</span>
                            <span className="ml-2 font-medium">{proposal.implementationStatus}</span>
                          </div>
                          <Button variant="outline" size="sm">
                            상세 보기
                          </Button>
                        </div>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="contributors" className="space-y-6">
          {/* Enhanced Top Contributors */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Award className="h-5 w-5 text-primary" />
                이달의 우수 제안자
              </CardTitle>
              <CardDescription>데이터 기반 정책 제안으로 시민 참여를 이끌고 있는 분들입니다</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {topContributors.map((contributor, index) => (
                  <div key={contributor.name} className="p-4 border rounded-lg">
                    <div className="flex items-start gap-4">
                      <div className="flex flex-col items-center">
                        <div className="w-16 h-16 bg-primary/10 rounded-full flex items-center justify-center mb-2">
                          {getRankIcon(index + 1)}
                        </div>
                        <div className={`px-2 py-1 rounded text-xs text-white ${getLevelColor(contributor.level)}`}>
                          {contributor.level}
                        </div>
                      </div>
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-2">
                          <h3 className="font-medium">{contributor.name}</h3>
                          <Badge variant="outline" className="text-xs">
                            {contributor.points.toLocaleString()}P
                          </Badge>
                        </div>
                        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm mb-3">
                          <div>
                            <div className="text-muted-foreground">제안 수</div>
                            <div className="font-medium">{contributor.proposals}개</div>
                          </div>
                          <div>
                            <div className="text-muted-foreground">총 공감</div>
                            <div className="font-medium">{contributor.totalLikes.toLocaleString()}개</div>
                          </div>
                          <div>
                            <div className="text-muted-foreground">성공률</div>
                            <div className="font-medium text-green-600">{contributor.successRate}%</div>
                          </div>
                          <div>
                            <div className="text-muted-foreground">참여 기간</div>
                            <div className="font-medium">{contributor.joinDate}~</div>
                          </div>
                        </div>
                        <div className="space-y-2">
                          <div>
                            <span className="text-sm text-muted-foreground">전문 분야:</span>
                            <div className="flex gap-1 mt-1">
                              {contributor.specialties.map((specialty) => (
                                <Badge key={specialty} variant="secondary" className="text-xs">
                                  {specialty}
                                </Badge>
                              ))}
                            </div>
                          </div>
                          <div>
                            <span className="text-sm text-muted-foreground">보유 배지:</span>
                            <div className="flex gap-1 mt-1">
                              {contributor.badges.map((badge) => (
                                <Badge key={badge} variant="outline" className="text-xs">
                                  <Star className="h-3 w-3 mr-1" />
                                  {badge}
                                </Badge>
                              ))}
                            </div>
                          </div>
                          <div className="text-sm">
                            <span className="text-muted-foreground">최근 성과:</span>
                            <span className="ml-2 text-primary font-medium">{contributor.recentAchievement}</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="badges" className="space-y-6">
          {/* Badge System */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Zap className="h-5 w-5 text-primary" />
                배지 및 레벨 시스템
              </CardTitle>
              <CardDescription>참여도와 기여도에 따른 보상 시스템으로 시민 참여를 촉진합니다</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-6">
                <div>
                  <h4 className="font-medium mb-4">레벨 시스템</h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {badgeSystem.levels.map((level) => (
                      <div key={level.name} className="p-4 border rounded-lg">
                        <div className="flex items-center gap-3 mb-2">
                          <div className={`w-4 h-4 rounded-full ${level.color}`}></div>
                          <span className="font-medium">{level.name}</span>
                          <Badge variant="outline" className="text-xs">
                            {level.minPoints.toLocaleString()}P+
                          </Badge>
                        </div>
                        <div className="text-sm text-muted-foreground">
                          <div className="font-medium mb-1">혜택:</div>
                          <ul className="space-y-1">
                            {level.benefits.map((benefit) => (
                              <li key={benefit} className="flex items-center gap-2">
                                <CheckCircle className="h-3 w-3 text-green-500" />
                                {benefit}
                              </li>
                            ))}
                          </ul>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                <div>
                  <h4 className="font-medium mb-4">성취 배지</h4>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    {badgeSystem.achievements.map((achievement) => (
                      <div key={achievement.name} className="p-4 border rounded-lg text-center">
                        <div className="text-2xl mb-2">{achievement.icon}</div>
                        <div className="font-medium mb-1">{achievement.name}</div>
                        <div className="text-sm text-muted-foreground">{achievement.description}</div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="analytics" className="space-y-6">
          {/* Enhanced Statistics */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Users className="h-5 w-5" />
                시민 참여 현황
              </CardTitle>
              <CardDescription>데이터 기반 정책 제안 플랫폼의 참여 통계</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-center mb-6">
                <div>
                  <div className="text-2xl font-bold text-primary">47</div>
                  <div className="text-sm text-muted-foreground">이달 새 제안</div>
                </div>
                <div>
                  <div className="text-2xl font-bold text-chart-2">1,234</div>
                  <div className="text-sm text-muted-foreground">총 공감 수</div>
                </div>
                <div>
                  <div className="text-2xl font-bold text-chart-4">89</div>
                  <div className="text-sm text-muted-foreground">활성 사용자</div>
                </div>
                <div>
                  <div className="text-2xl font-bold text-green-600">12</div>
                  <div className="text-sm text-muted-foreground">정책 반영</div>
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h4 className="font-medium mb-3">카테고리별 제안 현황</h4>
                  <div className="space-y-2">
                    <div className="flex justify-between items-center">
                      <span className="text-sm">시설 확충</span>
                      <div className="flex items-center gap-2">
                        <div className="w-20 h-2 bg-muted rounded-full overflow-hidden">
                          <div className="h-full bg-primary rounded-full" style={{ width: "65%" }}></div>
                        </div>
                        <span className="text-sm font-medium">31건</span>
                      </div>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-sm">운영 개선</span>
                      <div className="flex items-center gap-2">
                        <div className="w-20 h-2 bg-muted rounded-full overflow-hidden">
                          <div className="h-full bg-chart-2 rounded-full" style={{ width: "45%" }}></div>
                        </div>
                        <span className="text-sm font-medium">21건</span>
                      </div>
                    </div>
                    <div className="flex justify-between items-center">
                      <span className="text-sm">접근성 개선</span>
                      <div className="flex items-center gap-2">
                        <div className="w-20 h-2 bg-muted rounded-full overflow-hidden">
                          <div className="h-full bg-chart-3 rounded-full" style={{ width: "30%" }}></div>
                        </div>
                        <span className="text-sm font-medium">14건</span>
                      </div>
                    </div>
                  </div>
                </div>

                <div>
                  <h4 className="font-medium mb-3">정책 반영 현황</h4>
                  <div className="space-y-3">
                    <div className="flex items-center justify-between p-2 bg-green-50 rounded">
                      <span className="text-sm">정책 반영</span>
                      <Badge variant="default">12건</Badge>
                    </div>
                    <div className="flex items-center justify-between p-2 bg-blue-50 rounded">
                      <span className="text-sm">시범 운영</span>
                      <Badge variant="secondary">8건</Badge>
                    </div>
                    <div className="flex items-center justify-between p-2 bg-yellow-50 rounded">
                      <span className="text-sm">예산 검토</span>
                      <Badge variant="outline">15건</Badge>
                    </div>
                    <div className="flex items-center justify-between p-2 bg-orange-50 rounded">
                      <span className="text-sm">검토중</span>
                      <Badge variant="outline">23건</Badge>
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}
