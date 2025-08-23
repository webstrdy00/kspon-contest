"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Input } from "@/components/ui/input"
import { Heart, MessageCircle, Eye, Filter, Search, Calendar, User, MapPin } from "lucide-react"

const mockProposals = [
  {
    id: 1,
    title: "마포구 홍대 인근 실내 클라이밍짐 신설 제안",
    author: "김체육",
    region: "서울 마포구",
    category: "시설 확충",
    description:
      "20대 인구 비율이 높은 홍대 지역에 젊은층이 선호하는 클라이밍 시설이 부족합니다. 데이터 분석 결과를 바탕으로 신설을 제안합니다.",
    likes: 127,
    comments: 23,
    views: 456,
    status: "검토중",
    createdAt: "2024-01-15",
    hasDataAttachment: true,
  },
  {
    id: 2,
    title: "강남구 테니스장 이용 시간 확대 요청",
    author: "이정책",
    region: "서울 강남구",
    category: "운영 개선",
    description: "직장인들의 퇴근 후 이용을 위해 테니스장 운영 시간을 오후 10시까지 연장해주세요.",
    likes: 89,
    comments: 15,
    views: 234,
    status: "진행중",
    createdAt: "2024-01-12",
    hasDataAttachment: false,
  },
  {
    id: 3,
    title: "부산 해운대구 해변 운동기구 설치 제안",
    author: "박시민",
    region: "부산 해운대구",
    category: "시설 확충",
    description: "해변을 찾는 시민들이 운동할 수 있도록 야외 운동기구 설치를 제안합니다.",
    likes: 156,
    comments: 31,
    views: 678,
    status: "완료",
    createdAt: "2024-01-10",
    hasDataAttachment: true,
  },
  {
    id: 4,
    title: "대구 수성구 수영장 접근성 개선 방안",
    author: "최분석",
    region: "대구 수성구",
    category: "접근성",
    description: "고령자와 장애인을 위한 수영장 접근성 개선이 필요합니다.",
    likes: 73,
    comments: 12,
    views: 189,
    status: "검토중",
    createdAt: "2024-01-08",
    hasDataAttachment: true,
  },
]

export function ProposalList() {
  const [searchTerm, setSearchTerm] = useState("")
  const [selectedCategory, setSelectedCategory] = useState("all")
  const [selectedStatus, setSelectedStatus] = useState("all")

  const getStatusColor = (status: string) => {
    switch (status) {
      case "완료":
        return "default"
      case "진행중":
        return "secondary"
      case "검토중":
        return "outline"
      default:
        return "outline"
    }
  }

  return (
    <div className="space-y-6">
      {/* Filters */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Filter className="h-4 w-4" />
            필터 및 검색
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
              <Input
                placeholder="제안 검색..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-9"
              />
            </div>
            <Select value={selectedCategory} onValueChange={setSelectedCategory}>
              <SelectTrigger>
                <SelectValue placeholder="카테고리" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">전체 카테고리</SelectItem>
                <SelectItem value="시설 확충">시설 확충</SelectItem>
                <SelectItem value="운영 개선">운영 개선</SelectItem>
                <SelectItem value="접근성">접근성</SelectItem>
                <SelectItem value="예산">예산</SelectItem>
              </SelectContent>
            </Select>
            <Select value={selectedStatus} onValueChange={setSelectedStatus}>
              <SelectTrigger>
                <SelectValue placeholder="상태" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">전체 상태</SelectItem>
                <SelectItem value="검토중">검토중</SelectItem>
                <SelectItem value="진행중">진행중</SelectItem>
                <SelectItem value="완료">완료</SelectItem>
              </SelectContent>
            </Select>
            <Select defaultValue="latest">
              <SelectTrigger>
                <SelectValue placeholder="정렬" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="latest">최신순</SelectItem>
                <SelectItem value="popular">인기순</SelectItem>
                <SelectItem value="comments">댓글순</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </CardContent>
      </Card>

      {/* Proposal List */}
      <div className="space-y-4">
        {mockProposals.map((proposal) => (
          <Card key={proposal.id} className="hover:shadow-md transition-shadow cursor-pointer">
            <CardHeader>
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-2">
                    <Badge variant="outline">{proposal.category}</Badge>
                    <Badge variant={getStatusColor(proposal.status)}>{proposal.status}</Badge>
                    {proposal.hasDataAttachment && (
                      <Badge variant="secondary" className="text-xs">
                        데이터 첨부
                      </Badge>
                    )}
                  </div>
                  <CardTitle className="text-lg hover:text-primary transition-colors">{proposal.title}</CardTitle>
                  <CardDescription className="mt-2">{proposal.description}</CardDescription>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4 text-sm text-muted-foreground">
                  <div className="flex items-center gap-1">
                    <User className="h-4 w-4" />
                    {proposal.author}
                  </div>
                  <div className="flex items-center gap-1">
                    <MapPin className="h-4 w-4" />
                    {proposal.region}
                  </div>
                  <div className="flex items-center gap-1">
                    <Calendar className="h-4 w-4" />
                    {proposal.createdAt}
                  </div>
                </div>
                <div className="flex items-center gap-4">
                  <Button variant="ghost" size="sm" className="gap-1">
                    <Heart className="h-4 w-4" />
                    {proposal.likes}
                  </Button>
                  <Button variant="ghost" size="sm" className="gap-1">
                    <MessageCircle className="h-4 w-4" />
                    {proposal.comments}
                  </Button>
                  <Button variant="ghost" size="sm" className="gap-1">
                    <Eye className="h-4 w-4" />
                    {proposal.views}
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Load More */}
      <div className="text-center">
        <Button variant="outline">더 많은 제안 보기</Button>
      </div>
    </div>
  )
}
