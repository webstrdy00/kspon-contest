import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"

export function RegionalActivity() {
  const regionalData = [
    { region: "서울특별시", users: 3247, proposals: 892, reports: 1456 },
    { region: "경기도", users: 2891, proposals: 743, reports: 1234 },
    { region: "부산광역시", users: 1456, proposals: 387, reports: 678 },
    { region: "대구광역시", users: 1234, proposals: 298, reports: 543 },
    { region: "인천광역시", users: 1098, proposals: 267, reports: 456 },
  ]

  return (
    <Card>
      <CardHeader>
        <CardTitle>지역별 활동 현황</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b">
                <th className="text-left p-3">지역</th>
                <th className="text-right p-3">사용자</th>
                <th className="text-right p-3">제안</th>
                <th className="text-right p-3">리포트</th>
                <th className="text-right p-3">활동도</th>
              </tr>
            </thead>
            <tbody>
              {regionalData.map((region, index) => (
                <tr key={index} className="border-b hover:bg-gray-50">
                  <td className="p-3 font-medium">{region.region}</td>
                  <td className="p-3 text-right">{region.users.toLocaleString()}</td>
                  <td className="p-3 text-right">{region.proposals.toLocaleString()}</td>
                  <td className="p-3 text-right">{region.reports.toLocaleString()}</td>
                  <td className="p-3 text-right">
                    <div className="w-16 bg-gray-200 rounded-full h-2 ml-auto">
                      <div
                        className="bg-cyan-500 h-2 rounded-full"
                        style={{ width: `${Math.min((region.users / 3247) * 100, 100)}%` }}
                      ></div>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </CardContent>
    </Card>
  )
}
