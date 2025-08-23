import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"

export function DataUsage() {
  const dataApis = [
    { name: "전국공공체육시설", calls: 45672, status: "active", lastUpdate: "2시간 전" },
    { name: "국민체육진흥기금", calls: 23456, status: "active", lastUpdate: "1시간 전" },
    { name: "체육인복지기금", calls: 18934, status: "active", lastUpdate: "30분 전" },
    { name: "스포츠과학원 실태조사", calls: 12345, status: "maintenance", lastUpdate: "1일 전" },
    { name: "지역별 인구통계", calls: 34567, status: "active", lastUpdate: "4시간 전" },
  ]

  return (
    <Card>
      <CardHeader>
        <CardTitle>데이터 사용 현황</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {dataApis.map((api, index) => (
            <div key={index} className="flex items-center justify-between p-4 border rounded-lg">
              <div className="flex items-center space-x-4">
                <div className="w-2 h-2 rounded-full bg-green-500"></div>
                <div>
                  <p className="font-medium">{api.name}</p>
                  <p className="text-sm text-gray-600">API 호출: {api.calls.toLocaleString()}회</p>
                </div>
              </div>
              <div className="flex items-center space-x-3">
                <Badge variant={api.status === "active" ? "default" : "secondary"}>
                  {api.status === "active" ? "정상" : "점검중"}
                </Badge>
                <span className="text-sm text-gray-500">{api.lastUpdate}</span>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}
