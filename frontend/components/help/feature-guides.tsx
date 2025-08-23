import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { ChevronRight } from "lucide-react"

export function FeatureGuides() {
  const guides = [
    {
      category: "대시보드",
      items: [
        { title: "수요-공급 분석 맵 사용법", difficulty: "초급", time: "5분" },
        { title: "예산-성과 분석 해석하기", difficulty: "중급", time: "10분" },
        { title: "필터링과 데이터 내보내기", difficulty: "초급", time: "3분" },
      ],
    },
    {
      category: "리포트",
      items: [
        { title: "우리 동네 리포트 생성하기", difficulty: "초급", time: "7분" },
        { title: "비교 분석 기능 활용하기", difficulty: "중급", time: "12분" },
        { title: "PDF 다운로드 및 공유하기", difficulty: "초급", time: "2분" },
      ],
    },
    {
      category: "정책 제안",
      items: [
        { title: "효과적인 제안 작성법", difficulty: "중급", time: "15분" },
        { title: "데이터 근거 첨부하기", difficulty: "중급", time: "8분" },
        { title: "공감과 댓글 시스템", difficulty: "초급", time: "5분" },
      ],
    },
  ]

  return (
    <Card>
      <CardHeader>
        <CardTitle>기능별 가이드</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-6">
          {guides.map((category, index) => (
            <div key={index}>
              <h3 className="font-semibold text-lg mb-3">{category.category}</h3>
              <div className="space-y-2">
                {category.items.map((item, itemIndex) => (
                  <div
                    key={itemIndex}
                    className="flex items-center justify-between p-3 hover:bg-gray-50 rounded-lg cursor-pointer"
                  >
                    <div className="flex items-center space-x-3">
                      <span className="font-medium">{item.title}</span>
                      <Badge variant="outline">{item.difficulty}</Badge>
                      <span className="text-sm text-gray-500">{item.time}</span>
                    </div>
                    <ChevronRight className="h-4 w-4 text-gray-400" />
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}
