"use client"

import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Separator } from "@/components/ui/separator"
import { 
  ThumbsUp, 
  MessageSquare, 
  Eye, 
  MapPin, 
  Calendar, 
  User,
  Clock,
  CheckCircle,
  XCircle
} from "lucide-react"

interface Proposal {
  id: number
  title: string
  author: string
  content: string
  region: string
  category: string
  status: string
  likes: number
  comments: number
  views: number
  createdAt: string
  tags: string[]
}

interface ProposalCardProps {
  proposal: Proposal
  viewMode: "list" | "grid"
}

export function ProposalCard({ proposal, viewMode }: ProposalCardProps) {
  const getStatusColor = (status: string) => {
    switch (status) {
      case "승인":
        return "bg-green-100 text-green-800 border-green-300"
      case "처리완료":
        return "bg-blue-100 text-blue-800 border-blue-300"
      case "검토중":
        return "bg-yellow-100 text-yellow-800 border-yellow-300"
      case "거부":
        return "bg-red-100 text-red-800 border-red-300"
      default:
        return "bg-gray-100 text-gray-800 border-gray-300"
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "승인":
      case "처리완료":
        return <CheckCircle className="h-3 w-3" />
      case "검토중":
        return <Clock className="h-3 w-3" />
      case "거부":
        return <XCircle className="h-3 w-3" />
      default:
        return <Clock className="h-3 w-3" />
    }
  }

  if (viewMode === "grid") {
    return (
      <Card className="hover:shadow-md transition-all duration-200 cursor-pointer">
        <CardHeader className="pb-3">
          <div className="flex items-start justify-between mb-2">
            <Badge 
              variant="outline" 
              className={`text-xs px-2 py-1 ${getStatusColor(proposal.status)}`}
            >
              <div className="flex items-center gap-1">
                {getStatusIcon(proposal.status)}
                {proposal.status}
              </div>
            </Badge>
            <Badge variant="secondary" className="text-xs">
              {proposal.category}
            </Badge>
          </div>
          <CardTitle className="text-lg leading-tight hover:text-primary transition-colors">
            {proposal.title}
          </CardTitle>
        </CardHeader>
        
        <CardContent className="pt-0">
          <p className="text-sm text-muted-foreground mb-4 line-clamp-3">
            {proposal.content}
          </p>
          
          {/* 태그 */}
          <div className="flex flex-wrap gap-1 mb-4">
            {proposal.tags.slice(0, 2).map((tag, index) => (
              <Badge key={index} variant="outline" className="text-xs">
                #{tag}
              </Badge>
            ))}
            {proposal.tags.length > 2 && (
              <Badge variant="outline" className="text-xs">
                +{proposal.tags.length - 2}
              </Badge>
            )}
          </div>

          {/* 작성자 및 지역 정보 */}
          <div className="space-y-2 mb-4 text-xs text-muted-foreground">
            <div className="flex items-center gap-1">
              <User className="h-3 w-3" />
              <span>{proposal.author}</span>
            </div>
            <div className="flex items-center gap-1">
              <MapPin className="h-3 w-3" />
              <span>{proposal.region}</span>
            </div>
            <div className="flex items-center gap-1">
              <Calendar className="h-3 w-3" />
              <span>{proposal.createdAt}</span>
            </div>
          </div>

          <Separator className="mb-4" />

          {/* 상호작용 통계 */}
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-3 text-xs text-muted-foreground">
              <div className="flex items-center gap-1">
                <ThumbsUp className="h-3 w-3" />
                <span>{proposal.likes}</span>
              </div>
              <div className="flex items-center gap-1">
                <MessageSquare className="h-3 w-3" />
                <span>{proposal.comments}</span>
              </div>
              <div className="flex items-center gap-1">
                <Eye className="h-3 w-3" />
                <span>{proposal.views}</span>
              </div>
            </div>
          </div>

          {/* 액션 버튼 */}
          <div className="flex gap-2">
            <Button size="sm" variant="outline" className="flex-1">
              <ThumbsUp className="h-3 w-3 mr-1" />
              공감
            </Button>
            <Button size="sm" variant="outline" className="flex-1">
              <MessageSquare className="h-3 w-3 mr-1" />
              댓글
            </Button>
          </div>
        </CardContent>
      </Card>
    )
  }

  // List view
  return (
    <Card className="hover:shadow-md transition-all duration-200 cursor-pointer">
      <CardHeader>
        <div className="flex items-start justify-between">
          <div className="flex-1 space-y-2">
            <div className="flex items-center gap-2 flex-wrap">
              <Badge 
                variant="outline" 
                className={`text-xs px-2 py-1 ${getStatusColor(proposal.status)}`}
              >
                <div className="flex items-center gap-1">
                  {getStatusIcon(proposal.status)}
                  {proposal.status}
                </div>
              </Badge>
              <Badge variant="secondary" className="text-xs">
                {proposal.category}
              </Badge>
              {proposal.likes > 200 && (
                <Badge variant="outline" className="text-xs bg-red-50 text-red-600 border-red-200">
                  인기글
                </Badge>
              )}
            </div>
            
            <CardTitle className="text-xl leading-tight hover:text-primary transition-colors">
              {proposal.title}
            </CardTitle>
            
            <div className="flex items-center gap-4 text-sm text-muted-foreground flex-wrap">
              <div className="flex items-center gap-1">
                <User className="h-3 w-3" />
                <span>{proposal.author}</span>
              </div>
              <div className="flex items-center gap-1">
                <MapPin className="h-3 w-3" />
                <span>{proposal.region}</span>
              </div>
              <div className="flex items-center gap-1">
                <Calendar className="h-3 w-3" />
                <span>{proposal.createdAt}</span>
              </div>
            </div>
          </div>
        </div>
      </CardHeader>
      
      <CardContent>
        <p className="text-muted-foreground mb-4 leading-relaxed">
          {proposal.content}
        </p>
        
        {/* 태그 */}
        <div className="flex flex-wrap gap-1 mb-4">
          {proposal.tags.map((tag, index) => (
            <Badge key={index} variant="outline" className="text-xs">
              #{tag}
            </Badge>
          ))}
        </div>

        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4 text-sm text-muted-foreground">
            <div className="flex items-center gap-1">
              <ThumbsUp className="h-4 w-4 text-green-600" />
              <span className="text-green-600 font-medium">{proposal.likes}</span>
            </div>
            <div className="flex items-center gap-1">
              <MessageSquare className="h-4 w-4" />
              <span>{proposal.comments}</span>
            </div>
            <div className="flex items-center gap-1">
              <Eye className="h-4 w-4" />
              <span>{proposal.views}</span>
            </div>
          </div>
          
          <div className="flex gap-2">
            <Button variant="outline" size="sm">
              <ThumbsUp className="h-4 w-4 mr-2" />
              공감하기
            </Button>
            <Button variant="outline" size="sm">
              <MessageSquare className="h-4 w-4 mr-2" />
              댓글 ({proposal.comments})
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}