import { Card, CardContent, CardHeader } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Badge } from "@/components/ui/badge"
import { Heart, Reply, MoreHorizontal } from "lucide-react"

interface ProposalCommentsProps {
  proposalId: string
}

export function ProposalComments({ proposalId }: ProposalCommentsProps) {
  const comments = [
    {
      id: "1",
      author: {
        name: "이정책",
        avatar: "/placeholder.svg?height=32&width=32",
        level: "실버",
        isExpert: true,
      },
      content:
        "데이터 분석이 매우 체계적이네요. 특히 의료비 절감 효과까지 고려한 점이 인상적입니다. 다만 겨울철 이용률 저하에 대한 대안도 함께 고려해보시면 좋을 것 같습니다.",
      createdAt: "2024-01-16",
      likes: 23,
      replies: 3,
      isLiked: false,
    },
    {
      id: "2",
      author: {
        name: "박시민",
        avatar: "/placeholder.svg?height=32&width=32",
        level: "브론즈",
        isExpert: false,
      },
      content:
        "삼성동 주민입니다. 정말 필요한 시설이라고 생각해요! 현재 운동할 곳이 부족해서 멀리까지 가야 하는 상황이거든요. 적극 지지합니다.",
      createdAt: "2024-01-16",
      likes: 15,
      replies: 1,
      isLiked: true,
    },
    {
      id: "3",
      author: {
        name: "최전문",
        avatar: "/placeholder.svg?height=32&width=32",
        level: "골드",
        isExpert: true,
      },
      content:
        "파크골프장 운영 경험이 있는 입장에서 말씀드리면, 제안하신 연간 운영비가 다소 낙관적일 수 있습니다. 인건비와 시설 유지비를 좀 더 보수적으로 산정해보시기 바랍니다.",
      createdAt: "2024-01-17",
      likes: 31,
      replies: 5,
      isLiked: false,
    },
  ]

  return (
    <Card>
      <CardHeader>
        <h2 className="text-xl font-heading font-semibold">댓글 ({comments.length})</h2>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* 댓글 작성 */}
        <div className="space-y-3">
          <Textarea
            placeholder="이 제안에 대한 의견을 남겨주세요. 건설적인 토론을 위해 근거와 함께 작성해주시면 더욱 좋습니다."
            className="min-h-[100px]"
          />
          <div className="flex justify-end">
            <Button>댓글 작성</Button>
          </div>
        </div>

        {/* 댓글 목록 */}
        <div className="space-y-4">
          {comments.map((comment) => (
            <div key={comment.id} className="border-l-2 border-muted pl-4 space-y-3">
              <div className="flex items-start justify-between">
                <div className="flex items-center gap-3">
                  <Avatar className="h-8 w-8">
                    <AvatarImage src={comment.author.avatar || "/placeholder.svg"} />
                    <AvatarFallback>{comment.author.name[0]}</AvatarFallback>
                  </Avatar>
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="font-medium text-sm">{comment.author.name}</span>
                      <Badge variant="outline" className="text-xs">
                        {comment.author.level}
                      </Badge>
                      {comment.author.isExpert && (
                        <Badge variant="secondary" className="text-xs">
                          전문가
                        </Badge>
                      )}
                    </div>
                    <p className="text-xs text-muted-foreground">{comment.createdAt}</p>
                  </div>
                </div>
                <Button variant="ghost" size="sm">
                  <MoreHorizontal className="h-4 w-4" />
                </Button>
              </div>

              <p className="text-sm leading-relaxed">{comment.content}</p>

              <div className="flex items-center gap-4">
                <Button variant="ghost" size="sm" className={`gap-1 ${comment.isLiked ? "text-red-500" : ""}`}>
                  <Heart className={`h-4 w-4 ${comment.isLiked ? "fill-current" : ""}`} />
                  {comment.likes}
                </Button>
                <Button variant="ghost" size="sm" className="gap-1">
                  <Reply className="h-4 w-4" />
                  답글 {comment.replies}
                </Button>
              </div>
            </div>
          ))}
        </div>

        <div className="text-center">
          <Button variant="outline">댓글 더 보기</Button>
        </div>
      </CardContent>
    </Card>
  )
}
