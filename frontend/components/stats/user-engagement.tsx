import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

export function UserEngagement() {
  const engagementData = [
    { activity: "대시보드 조회", count: 15420, percentage: 45 },
    { activity: "리포트 생성", count: 8756, percentage: 26 },
    { activity: "제안 작성", count: 3421, percentage: 10 },
    { activity: "댓글 작성", count: 5234, percentage: 15 },
    { activity: "공감 투표", count: 1289, percentage: 4 },
  ]

  return (
    <Card>
      <CardHeader>
        <CardTitle>사용자 참여도</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {engagementData.map((item, index) => (
            <div key={index} className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <div className="w-3 h-3 rounded-full bg-cyan-500"></div>
                <span className="text-sm font-medium">{item.activity}</span>
              </div>
              <div className="flex items-center space-x-3">
                <span className="text-sm text-gray-600">{item.count.toLocaleString()}</span>
                <div className="w-20 bg-gray-200 rounded-full h-2">
                  <div className="bg-cyan-500 h-2 rounded-full" style={{ width: `${item.percentage}%` }}></div>
                </div>
                <span className="text-sm font-medium w-8">{item.percentage}%</span>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}
