"use client"

import { useState } from "react"
import { Header } from "@/components/layout/header"
import { Sidebar } from "@/components/layout/sidebar"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Badge } from "@/components/ui/badge"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { useAuth } from "@/contexts/AuthContext"
import { 
  User, 
  MessageSquare, 
  ThumbsUp, 
  FileText, 
  Calendar, 
  Edit,
  Save,
  X,
  CheckCircle,
  AlertCircle,
  Eye,
  TrendingUp
} from "lucide-react"

export default function ProfilePage() {
  const { user, updateProfile } = useAuth()
  const [isEditing, setIsEditing] = useState(false)
  const [formData, setFormData] = useState({
    name: user?.name || "",
    region: user?.region || ""
  })
  const [updateMessage, setUpdateMessage] = useState("")
  const [isLoading, setIsLoading] = useState(false)

  const regions = [
    "서울특별시", "부산광역시", "대구광역시", "인천광역시",
    "광주광역시", "대전광역시", "울산광역시", "세종특별자치시",
    "경기도", "강원도", "충청북도", "충청남도", 
    "전라북도", "전라남도", "경상북도", "경상남도", "제주특별자치도"
  ]

  // Mock 사용자 활동 데이터
  const userStats = {
    proposalsCreated: 5,
    likesReceived: 127,
    commentsReceived: 34,
    profileViews: 89
  }

  const myProposals = [
    {
      id: 1,
      title: "동네 공원에 야외 운동기구 설치 요청",
      status: "검토중",
      likes: 45,
      comments: 8,
      createdAt: "2025-01-20"
    },
    {
      id: 2,
      title: "장애인 친화적 체육시설 개선 요청",
      status: "승인",
      likes: 82,
      comments: 15,
      createdAt: "2025-01-15"
    },
    {
      id: 3,
      title: "학교 운동장 야간 개방 시간 확대",
      status: "처리완료",
      likes: 67,
      comments: 11,
      createdAt: "2025-01-10"
    }
  ]

  const handleSave = async () => {
    setIsLoading(true)
    setUpdateMessage("")
    
    try {
      const result = await updateProfile({
        name: formData.name,
        region: formData.region
      })
      
      if (result.success) {
        setIsEditing(false)
        setUpdateMessage("프로필이 성공적으로 업데이트되었습니다.")
      } else {
        setUpdateMessage(result.error || "업데이트에 실패했습니다.")
      }
    } catch (error) {
      setUpdateMessage("프로필 업데이트 중 오류가 발생했습니다.")
    } finally {
      setIsLoading(false)
    }
  }

  const handleCancel = () => {
    setFormData({
      name: user?.name || "",
      region: user?.region || ""
    })
    setIsEditing(false)
    setUpdateMessage("")
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case "승인": return "bg-green-100 text-green-800"
      case "처리완료": return "bg-blue-100 text-blue-800"
      case "검토중": return "bg-yellow-100 text-yellow-800"
      default: return "bg-gray-100 text-gray-800"
    }
  }

  if (!user) {
    return (
      <div className="min-h-screen bg-background">
        <Header />
        <div className="flex">
          <Sidebar />
          <main className="flex-1 p-6">
            <Alert>
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>
                로그인이 필요합니다. <a href="/auth/login" className="underline text-primary">로그인하기</a>
              </AlertDescription>
            </Alert>
          </main>
        </div>
      </div>
    )
  }

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
                <h1 className="text-3xl font-bold tracking-tight">프로필</h1>
                <p className="text-muted-foreground">
                  개인 정보와 활동 내역을 관리하세요
                </p>
              </div>
              {!isEditing && (
                <Button onClick={() => setIsEditing(true)}>
                  <Edit className="mr-2 h-4 w-4" />
                  프로필 편집
                </Button>
              )}
            </div>

            {updateMessage && (
              <Alert>
                <CheckCircle className="h-4 w-4" />
                <AlertDescription>{updateMessage}</AlertDescription>
              </Alert>
            )}

            <Tabs defaultValue="profile" className="space-y-6">
              <TabsList>
                <TabsTrigger value="profile">개인 정보</TabsTrigger>
                <TabsTrigger value="activity">활동 내역</TabsTrigger>
                <TabsTrigger value="proposals">내 제안서</TabsTrigger>
              </TabsList>

              {/* 개인 정보 탭 */}
              <TabsContent value="profile" className="space-y-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {/* 프로필 정보 */}
                  <Card>
                    <CardHeader>
                      <CardTitle className="flex items-center gap-2">
                        <User className="h-5 w-5" />
                        기본 정보
                      </CardTitle>
                      <CardDescription>
                        기본 프로필 정보를 관리할 수 있습니다
                      </CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-4">
                      <div>
                        <Label htmlFor="email">이메일</Label>
                        <Input
                          id="email"
                          type="email"
                          value={user.email}
                          disabled
                          className="bg-muted"
                        />
                        <p className="text-xs text-muted-foreground mt-1">
                          이메일은 변경할 수 없습니다
                        </p>
                      </div>

                      <div>
                        <Label htmlFor="name">이름</Label>
                        <Input
                          id="name"
                          value={isEditing ? formData.name : user.name}
                          onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                          disabled={!isEditing}
                          className={!isEditing ? "bg-muted" : ""}
                        />
                      </div>

                      <div>
                        <Label htmlFor="region">거주 지역</Label>
                        {isEditing ? (
                          <Select 
                            value={formData.region} 
                            onValueChange={(value) => setFormData({ ...formData, region: value })}
                          >
                            <SelectTrigger>
                              <SelectValue />
                            </SelectTrigger>
                            <SelectContent>
                              {regions.map((region) => (
                                <SelectItem key={region} value={region}>
                                  {region}
                                </SelectItem>
                              ))}
                            </SelectContent>
                          </Select>
                        ) : (
                          <Input
                            value={user.region}
                            disabled
                            className="bg-muted"
                          />
                        )}
                      </div>

                      <div>
                        <Label htmlFor="role">계정 유형</Label>
                        <Input
                          id="role"
                          value={user.role === 'admin' ? '관리자' : '일반 사용자'}
                          disabled
                          className="bg-muted"
                        />
                      </div>

                      <div>
                        <Label htmlFor="joinDate">가입일</Label>
                        <Input
                          id="joinDate"
                          value={user.createdAt}
                          disabled
                          className="bg-muted"
                        />
                      </div>

                      {isEditing && (
                        <div className="flex gap-2 pt-4">
                          <Button onClick={handleSave} disabled={isLoading}>
                            {isLoading ? (
                              <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2" />
                            ) : (
                              <Save className="mr-2 h-4 w-4" />
                            )}
                            저장
                          </Button>
                          <Button variant="outline" onClick={handleCancel}>
                            <X className="mr-2 h-4 w-4" />
                            취소
                          </Button>
                        </div>
                      )}
                    </CardContent>
                  </Card>

                  {/* 통계 */}
                  <Card>
                    <CardHeader>
                      <CardTitle className="flex items-center gap-2">
                        <TrendingUp className="h-5 w-5" />
                        활동 통계
                      </CardTitle>
                      <CardDescription>
                        플랫폼에서의 활동 현황입니다
                      </CardDescription>
                    </CardHeader>
                    <CardContent>
                      <div className="grid grid-cols-2 gap-4">
                        <div className="text-center p-4 bg-muted/50 rounded-lg">
                          <div className="text-2xl font-bold text-primary">{userStats.proposalsCreated}</div>
                          <div className="text-sm text-muted-foreground">작성한 제안</div>
                        </div>
                        <div className="text-center p-4 bg-muted/50 rounded-lg">
                          <div className="text-2xl font-bold text-green-600">{userStats.likesReceived}</div>
                          <div className="text-sm text-muted-foreground">받은 공감</div>
                        </div>
                        <div className="text-center p-4 bg-muted/50 rounded-lg">
                          <div className="text-2xl font-bold text-blue-600">{userStats.commentsReceived}</div>
                          <div className="text-sm text-muted-foreground">받은 댓글</div>
                        </div>
                        <div className="text-center p-4 bg-muted/50 rounded-lg">
                          <div className="text-2xl font-bold text-purple-600">{userStats.profileViews}</div>
                          <div className="text-sm text-muted-foreground">프로필 조회</div>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                </div>
              </TabsContent>

              {/* 활동 내역 탭 */}
              <TabsContent value="activity" className="space-y-6">
                <Card>
                  <CardHeader>
                    <CardTitle>최근 활동</CardTitle>
                    <CardDescription>
                      최근 30일간의 활동 내역입니다
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      <div className="flex items-center gap-4 p-3 border rounded-lg">
                        <MessageSquare className="h-4 w-4 text-primary" />
                        <div className="flex-1">
                          <p className="font-medium">새 제안서를 작성했습니다</p>
                          <p className="text-sm text-muted-foreground">동네 공원에 야외 운동기구 설치 요청</p>
                        </div>
                        <span className="text-xs text-muted-foreground">2025-01-20</span>
                      </div>
                      <div className="flex items-center gap-4 p-3 border rounded-lg">
                        <ThumbsUp className="h-4 w-4 text-green-600" />
                        <div className="flex-1">
                          <p className="font-medium">제안서가 승인되었습니다</p>
                          <p className="text-sm text-muted-foreground">장애인 친화적 체육시설 개선 요청</p>
                        </div>
                        <span className="text-xs text-muted-foreground">2025-01-18</span>
                      </div>
                      <div className="flex items-center gap-4 p-3 border rounded-lg">
                        <CheckCircle className="h-4 w-4 text-blue-600" />
                        <div className="flex-1">
                          <p className="font-medium">제안서가 처리 완료되었습니다</p>
                          <p className="text-sm text-muted-foreground">학교 운동장 야간 개방 시간 확대</p>
                        </div>
                        <span className="text-xs text-muted-foreground">2025-01-15</span>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              {/* 내 제안서 탭 */}
              <TabsContent value="proposals" className="space-y-6">
                <Card>
                  <CardHeader>
                    <CardTitle className="flex items-center gap-2">
                      <FileText className="h-5 w-5" />
                      내가 작성한 제안서 ({myProposals.length})
                    </CardTitle>
                    <CardDescription>
                      작성한 모든 제안서를 확인할 수 있습니다
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      {myProposals.map((proposal) => (
                        <div key={proposal.id} className="flex items-center justify-between p-4 border rounded-lg hover:bg-muted/50 transition-colors">
                          <div className="flex-1">
                            <div className="flex items-center gap-2 mb-2">
                              <Badge className={`text-xs ${getStatusColor(proposal.status)}`}>
                                {proposal.status}
                              </Badge>
                            </div>
                            <h3 className="font-medium mb-2">{proposal.title}</h3>
                            <div className="flex items-center gap-4 text-sm text-muted-foreground">
                              <div className="flex items-center gap-1">
                                <ThumbsUp className="h-3 w-3" />
                                {proposal.likes}
                              </div>
                              <div className="flex items-center gap-1">
                                <MessageSquare className="h-3 w-3" />
                                {proposal.comments}
                              </div>
                              <div className="flex items-center gap-1">
                                <Calendar className="h-3 w-3" />
                                {proposal.createdAt}
                              </div>
                            </div>
                          </div>
                          <div className="flex gap-2">
                            <Button size="sm" variant="outline">
                              <Eye className="h-4 w-4 mr-1" />
                              보기
                            </Button>
                            {proposal.status === "검토중" && (
                              <Button size="sm" variant="outline">
                                <Edit className="h-4 w-4 mr-1" />
                                수정
                              </Button>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>
            </Tabs>
          </div>
        </main>
      </div>
    </div>
  )
}
