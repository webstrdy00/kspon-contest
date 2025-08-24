"use client"

import { useState } from "react"
import { Header } from "@/components/layout/header"
import { Sidebar } from "@/components/layout/sidebar"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { ProposalCard } from "@/components/proposals/proposal-card"
import { CreateProposalModal } from "@/components/proposals/create-proposal-modal"
import { 
  MessageSquare, 
  MessageSquarePlus, 
  ThumbsUp, 
  ThumbsDown, 
  Eye, 
  Search, 
  Plus, 
  Filter,
  MapPin, 
  Calendar, 
  TrendingUp,
  Clock,
  CheckCircle,
  Users,
  Star
} from "lucide-react"

export default function ProposalsPage() {
  const [searchTerm, setSearchTerm] = useState("")
  const [selectedCategory, setSelectedCategory] = useState("전체")
  const [sortBy, setSortBy] = useState("recent")
  const [filterBy, setFilterBy] = useState("all")
  const [showCreateModal, setShowCreateModal] = useState(false)

  const mockProposals = [
    {
      id: 1,
      title: "동네 공원에 야외 운동기구 설치 요청",
      author: "시민김철수",
      content: "우리 동네 근린공원에 어르신들이 사용할 수 있는 야외 운동기구 설치를 제안합니다. 현재 산책로만 있어서 아쉽습니다.",
      region: "서울시 강남구",
      category: "시설 확충",
      status: "검토중",
      likes: 245,
      comments: 18,
      views: 1247,
      createdAt: "2025-01-20",
      tags: ["야외운동기구", "공원", "어르신"]
    },
    {
      id: 2,
      title: "동네 체육관 운영 시간 연장 건의",
      author: "직장인박영희",
      content: "현재 오후 6시에 문을 닫는 구립 체육관의 운영시간을 오후 10시까지 연장해주시면 직장인들이 퇴근 후에도 이용할 수 있을 것 같습니다.",
      region: "부산시 해운대구", 
      category: "운영 개선",
      status: "승인",
      likes: 189,
      comments: 32,
      views: 892,
      createdAt: "2025-01-18",
      tags: ["체육관", "운영시간", "직장인"]
    },
    {
      id: 3,
      title: "학교 운동장 개방 시간 확대",
      author: "학부모이순신",
      content: "초등학교 운동장이 주말에만 개방되는데, 평일 저녁시간에도 개방하여 아이들이 더 자유롭게 뛰어놀 수 있도록 해주세요.",
      region: "대구시 수성구",
      category: "접근성 개선", 
      status: "검토중",
      likes: 156,
      comments: 24,
      views: 678,
      createdAt: "2025-01-15",
      tags: ["학교운동장", "개방시간", "어린이"]
    },
    {
      id: 4,
      title: "수영장 물 온도 조절 개선",
      author: "수영동호회",
      content: "구립 수영장의 물 온도가 너무 낮아서 특히 겨울철에는 이용하기 어렵습니다. 적정 온도로 관리해 주세요.",
      region: "인천시 남동구",
      category: "시설 개선",
      status: "처리완료",
      likes: 78,
      comments: 12,
      views: 445,
      createdAt: "2025-01-12",
      tags: ["수영장", "온도조절", "시설개선"]
    },
    {
      id: 5,
      title: "장애인 친화 운동시설 설치",
      author: "장애인협회",
      content: "휠체어를 이용하는 분들도 사용할 수 있는 운동기구와 시설을 동네 체육공원에 설치해 주시기 바랍니다.",
      region: "광주시 서구",
      category: "접근성 개선",
      status: "검토중", 
      likes: 312,
      comments: 45,
      views: 1156,
      createdAt: "2025-01-10",
      tags: ["장애인", "접근성", "운동기구"]
    }
  ]

  const stats = {
    totalProposals: mockProposals.length,
    approvedProposals: mockProposals.filter(p => p.status === "승인" || p.status === "처리완료").length,
    underReview: mockProposals.filter(p => p.status === "검토중").length,
    averageRating: 4.2
  }

  const filteredProposals = mockProposals.filter(proposal => {
    const matchesSearch = proposal.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         proposal.content.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         proposal.tags.some(tag => tag.toLowerCase().includes(searchTerm.toLowerCase()))
    
    const matchesFilter = filterBy === "all" || 
                         (filterBy === "approved" && (proposal.status === "승인" || proposal.status === "처리완료")) ||
                         (filterBy === "pending" && proposal.status === "검토중") ||
                         (filterBy === "popular" && proposal.likes > 200)
    
    return matchesSearch && matchesFilter
  })

  const sortedProposals = [...filteredProposals].sort((a, b) => {
    switch (sortBy) {
      case "popular":
        return b.likes - a.likes
      case "comments":
        return b.comments - a.comments
      case "recent":
      default:
        return new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
    }
  })

  return (
    <div className="min-h-screen bg-background">
      <Header />
      <div className="flex">
        <Sidebar />
        <main className="flex-1 p-6">
          <div className="space-y-6">
            {/* 페이지 헤더 */}
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-3xl font-bold tracking-tight">시민 정책 제안</h1>
                <p className="text-muted-foreground">
                  지역 체육환경 개선을 위한 시민들의 아이디어를 공유하고 투표하세요
                </p>
              </div>
              <Button onClick={() => setShowCreateModal(true)}>
                <MessageSquarePlus className="mr-2 h-4 w-4" />
                제안 작성
              </Button>
            </div>

            {/* 통계 카드 */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <Card>
                <CardContent className="p-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-muted-foreground">총 제안</p>
                      <p className="text-2xl font-bold">{stats.totalProposals}</p>
                    </div>
                    <MessageSquarePlus className="h-8 w-8 text-primary" />
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardContent className="p-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-muted-foreground">승인/완료</p>
                      <p className="text-2xl font-bold">{stats.approvedProposals}</p>
                    </div>
                    <CheckCircle className="h-8 w-8 text-green-500" />
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardContent className="p-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-muted-foreground">검토중</p>
                      <p className="text-2xl font-bold">{stats.underReview}</p>
                    </div>
                    <Clock className="h-8 w-8 text-orange-500" />
                  </div>
                </CardContent>
              </Card>

              <Card>
                <CardContent className="p-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-muted-foreground">평균 평점</p>
                      <p className="text-2xl font-bold">{stats.averageRating}</p>
                    </div>
                    <Star className="h-8 w-8 text-yellow-500" />
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* 검색 및 필터 */}
            <Card>
              <CardContent className="p-4">
                <div className="flex flex-col md:flex-row gap-4">
                  <div className="flex-1">
                    <div className="relative">
                      <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                      <Input
                        placeholder="제안 검색..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        className="pl-10"
                      />
                    </div>
                  </div>
                  
                  <Select value={filterBy} onValueChange={setFilterBy}>
                    <SelectTrigger className="w-40">
                      <Filter className="h-4 w-4 mr-2" />
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="all">전체</SelectItem>
                      <SelectItem value="approved">승인/완료</SelectItem>
                      <SelectItem value="pending">검토중</SelectItem>
                      <SelectItem value="popular">인기글</SelectItem>
                    </SelectContent>
                  </Select>

                  <Select value={sortBy} onValueChange={setSortBy}>
                    <SelectTrigger className="w-32">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="recent">최신순</SelectItem>
                      <SelectItem value="popular">인기순</SelectItem>
                      <SelectItem value="comments">댓글순</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </CardContent>
            </Card>

            {/* 제안 목록 */}
            <Tabs defaultValue="list" className="space-y-4">
              <TabsList>
                <TabsTrigger value="list">목록형</TabsTrigger>
                <TabsTrigger value="grid">그리드형</TabsTrigger>
              </TabsList>

              <TabsContent value="list" className="space-y-4">
                {sortedProposals.length > 0 ? (
                  <div className="space-y-4">
                    {sortedProposals.map((proposal) => (
                      <ProposalCard key={proposal.id} proposal={proposal} viewMode="list" />
                    ))}
                  </div>
                ) : (
                  <Card>
                    <CardContent className="p-12 text-center">
                      <MessageSquarePlus className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                      <h3 className="font-semibold text-lg mb-2">검색 결과가 없습니다</h3>
                      <p className="text-muted-foreground mb-4">
                        다른 키워드로 검색하거나 필터를 조정해보세요
                      </p>
                      <Button variant="outline" onClick={() => {
                        setSearchTerm("")
                        setFilterBy("all")
                      }}>
                        전체 보기
                      </Button>
                    </CardContent>
                  </Card>
                )}
              </TabsContent>

              <TabsContent value="grid" className="space-y-4">
                {sortedProposals.length > 0 ? (
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {sortedProposals.map((proposal) => (
                      <ProposalCard key={proposal.id} proposal={proposal} viewMode="grid" />
                    ))}
                  </div>
                ) : (
                  <Card>
                    <CardContent className="p-12 text-center">
                      <MessageSquarePlus className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
                      <h3 className="font-semibold text-lg mb-2">검색 결과가 없습니다</h3>
                      <p className="text-muted-foreground mb-4">
                        다른 키워드로 검색하거나 필터를 조정해보세요
                      </p>
                      <Button variant="outline" onClick={() => {
                        setSearchTerm("")
                        setFilterBy("all")
                      }}>
                        전체 보기
                      </Button>
                    </CardContent>
                  </Card>
                )}
              </TabsContent>
            </Tabs>

            {/* 페이지 하단 정보 */}
            <Card>
              <CardContent className="p-4">
                <div className="flex items-center justify-between text-sm text-muted-foreground">
                  <div>
                    총 {filteredProposals.length}개의 제안이 있습니다
                  </div>
                  <div className="flex items-center gap-2">
                    <span>마지막 업데이트:</span>
                    <span>2025-01-20</span>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </main>
      </div>

      <CreateProposalModal 
        open={showCreateModal} 
        onClose={() => setShowCreateModal(false)} 
      />
    </div>
  )
}

