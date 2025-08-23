import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader } from "@/components/ui/card"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Heart, Share2, Flag, TrendingUp, MapPin, Calendar, Users, Award } from "lucide-react"

interface ProposalDetailProps {
  proposalId: string
}

export function ProposalDetail({ proposalId }: ProposalDetailProps) {
  // Mock data - 실제로는 API에서 가져올 데이터
  const proposal = {
    id: proposalId,
    title: "강남구 유휴부지에 파크골프장 설치 제안",
    content: `강남구 삼성동 일대의 유휴부지를 활용하여 시민들을 위한 파크골프장을 설치할 것을 제안합니다.

## 📊 데이터 기반 근거

**현재 강남구 체육시설 현황:**
- 인구 대비 체육시설 비율: 전국 평균 대비 73% 수준
- 50대 이상 인구 비율: 32.4% (전국 평균 28.1%)
- 파크골프 수요 조사: 응답자의 67%가 이용 의향 표시

**기대 효과:**
- 연간 예상 이용자: 약 15,000명
- 지역 경제 활성화: 연간 약 3억원 규모
- 건강 증진 효과: 의료비 절감 연간 약 1.2억원

## 🗺️ 제안 위치

삼성동 159-1번지 일대 (약 12,000㎡)
- 지하철 2호선 삼성역에서 도보 10분
- 주변 아파트 단지 밀집 지역
- 현재 임시 주차장으로 활용 중

## 💰 예산 계획

총 사업비: 약 8억원
- 부지 정비: 2억원
- 시설 조성: 5억원
- 부대시설: 1억원

연간 운영비: 약 3,000만원
이용료 수입으로 자립 운영 가능`,
    author: {
      name: "김체육",
      avatar: "/placeholder.svg?height=40&width=40",
      level: "골드",
      badges: ["데이터 분석가", "지역 전문가"],
    },
    createdAt: "2024-01-15",
    likes: 257,
    views: 1834,
    status: "검토중",
    category: "체육시설",
    region: "강남구",
    attachments: [
      { type: "chart", title: "강남구 체육시설 현황 분석", url: "#" },
      { type: "map", title: "제안 위치 지도", url: "#" },
      { type: "report", title: "수요 조사 결과", url: "#" },
    ],
    supporters: 257,
    comments: 34,
    shares: 12,
  }

  return (
    <div className="space-y-6">
      {/* 제안 헤더 */}
      <Card>
        <CardHeader className="space-y-4">
          <div className="flex items-start justify-between">
            <div className="space-y-2">
              <div className="flex items-center gap-2">
                <Badge variant="secondary">{proposal.category}</Badge>
                <Badge variant="outline">{proposal.region}</Badge>
                <Badge
                  variant={proposal.status === "검토중" ? "default" : "secondary"}
                  className="bg-amber-100 text-amber-800"
                >
                  {proposal.status}
                </Badge>
              </div>
              <h1 className="text-3xl font-heading font-bold">{proposal.title}</h1>
            </div>
            <div className="flex items-center gap-2">
              <Button variant="outline" size="sm">
                <Share2 className="h-4 w-4 mr-2" />
                공유
              </Button>
              <Button variant="outline" size="sm">
                <Flag className="h-4 w-4 mr-2" />
                신고
              </Button>
            </div>
          </div>

          {/* 작성자 정보 */}
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Avatar>
                <AvatarImage src={proposal.author.avatar || "/placeholder.svg"} />
                <AvatarFallback>{proposal.author.name[0]}</AvatarFallback>
              </Avatar>
              <div>
                <div className="flex items-center gap-2">
                  <span className="font-medium">{proposal.author.name}</span>
                  <Badge variant="outline" className="text-xs">
                    <Award className="h-3 w-3 mr-1" />
                    {proposal.author.level}
                  </Badge>
                </div>
                <div className="flex items-center gap-1 text-sm text-muted-foreground">
                  {proposal.author.badges.map((badge, index) => (
                    <Badge key={index} variant="secondary" className="text-xs">
                      {badge}
                    </Badge>
                  ))}
                </div>
              </div>
            </div>
            <div className="text-sm text-muted-foreground">
              <Calendar className="h-4 w-4 inline mr-1" />
              {proposal.createdAt}
            </div>
          </div>

          {/* 통계 */}
          <div className="flex items-center gap-6 text-sm text-muted-foreground">
            <div className="flex items-center gap-1">
              <Heart className="h-4 w-4" />
              공감 {proposal.supporters}명
            </div>
            <div className="flex items-center gap-1">
              <Users className="h-4 w-4" />
              댓글 {proposal.comments}개
            </div>
            <div className="flex items-center gap-1">
              <TrendingUp className="h-4 w-4" />
              조회 {proposal.views}회
            </div>
          </div>
        </CardHeader>
      </Card>

      {/* 공감 버튼 */}
      <Card>
        <CardContent className="p-6">
          <div className="flex items-center justify-center">
            <Button size="lg" className="gap-2">
              <Heart className="h-5 w-5" />이 제안에 공감합니다 ({proposal.likes})
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* 제안 내용 */}
      <Card>
        <CardHeader>
          <h2 className="text-xl font-heading font-semibold">제안 내용</h2>
        </CardHeader>
        <CardContent className="prose max-w-none">
          <div className="whitespace-pre-wrap">{proposal.content}</div>
        </CardContent>
      </Card>

      {/* 첨부 자료 */}
      <Card>
        <CardHeader>
          <h2 className="text-xl font-heading font-semibold">첨부 자료</h2>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {proposal.attachments.map((attachment, index) => (
              <Card key={index} className="cursor-pointer hover:shadow-md transition-shadow">
                <CardContent className="p-4">
                  <div className="flex items-center gap-3">
                    <div className="h-10 w-10 rounded-lg bg-primary/10 flex items-center justify-center">
                      {attachment.type === "chart" && <TrendingUp className="h-5 w-5 text-primary" />}
                      {attachment.type === "map" && <MapPin className="h-5 w-5 text-primary" />}
                      {attachment.type === "report" && <Users className="h-5 w-5 text-primary" />}
                    </div>
                    <div>
                      <p className="font-medium text-sm">{attachment.title}</p>
                      <p className="text-xs text-muted-foreground">
                        {attachment.type === "chart" && "데이터 차트"}
                        {attachment.type === "map" && "지도 자료"}
                        {attachment.type === "report" && "분석 리포트"}
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
