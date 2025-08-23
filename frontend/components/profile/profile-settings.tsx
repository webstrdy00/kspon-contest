import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Switch } from "@/components/ui/switch"
import { Separator } from "@/components/ui/separator"

export function ProfileSettings() {
  return (
    <div className="space-y-6">
      {/* Profile Information */}
      <Card>
        <CardHeader>
          <CardTitle>프로필 정보</CardTitle>
          <CardDescription>공개 프로필에 표시되는 정보를 관리하세요</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="name">이름</Label>
              <Input id="name" defaultValue="김체육" />
            </div>
            <div className="space-y-2">
              <Label htmlFor="email">이메일</Label>
              <Input id="email" type="email" defaultValue="kim@example.com" />
            </div>
          </div>
          <div className="space-y-2">
            <Label htmlFor="location">지역</Label>
            <Select defaultValue="seoul-mapo">
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="seoul-mapo">서울특별시 마포구</SelectItem>
                <SelectItem value="seoul-gangnam">서울특별시 강남구</SelectItem>
                <SelectItem value="busan-haeundae">부산광역시 해운대구</SelectItem>
              </SelectContent>
            </Select>
          </div>
          <Button>프로필 업데이트</Button>
        </CardContent>
      </Card>

      {/* Notification Settings */}
      <Card>
        <CardHeader>
          <CardTitle>알림 설정</CardTitle>
          <CardDescription>받고 싶은 알림을 선택하세요</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <Label htmlFor="proposal-notifications">새로운 제안 알림</Label>
              <p className="text-sm text-muted-foreground">관심 지역의 새 제안이 등록될 때 알림을 받습니다</p>
            </div>
            <Switch id="proposal-notifications" defaultChecked />
          </div>
          <Separator />
          <div className="flex items-center justify-between">
            <div>
              <Label htmlFor="comment-notifications">댓글 알림</Label>
              <p className="text-sm text-muted-foreground">내 제안에 댓글이 달릴 때 알림을 받습니다</p>
            </div>
            <Switch id="comment-notifications" defaultChecked />
          </div>
          <Separator />
          <div className="flex items-center justify-between">
            <div>
              <Label htmlFor="like-notifications">공감 알림</Label>
              <p className="text-sm text-muted-foreground">내 제안에 공감을 받을 때 알림을 받습니다</p>
            </div>
            <Switch id="like-notifications" />
          </div>
          <Separator />
          <div className="flex items-center justify-between">
            <div>
              <Label htmlFor="policy-notifications">정책 반영 알림</Label>
              <p className="text-sm text-muted-foreground">제안이 정책에 반영될 때 알림을 받습니다</p>
            </div>
            <Switch id="policy-notifications" defaultChecked />
          </div>
        </CardContent>
      </Card>

      {/* Privacy Settings */}
      <Card>
        <CardHeader>
          <CardTitle>개인정보 설정</CardTitle>
          <CardDescription>개인정보 공개 범위를 설정하세요</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <Label htmlFor="public-profile">프로필 공개</Label>
              <p className="text-sm text-muted-foreground">다른 사용자가 내 프로필을 볼 수 있습니다</p>
            </div>
            <Switch id="public-profile" defaultChecked />
          </div>
          <Separator />
          <div className="flex items-center justify-between">
            <div>
              <Label htmlFor="show-stats">통계 공개</Label>
              <p className="text-sm text-muted-foreground">제안 수, 공감 수 등의 통계를 공개합니다</p>
            </div>
            <Switch id="show-stats" defaultChecked />
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
