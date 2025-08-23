import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from "@/components/ui/collapsible"
import { ChevronDown } from "lucide-react"

export function FAQ() {
  const faqs = [
    {
      question: "스포츠 데이터랩은 무료로 사용할 수 있나요?",
      answer:
        "네, 모든 기본 기능은 무료로 제공됩니다. 회원가입 후 대시보드 조회, 리포트 생성, 정책 제안 등 모든 핵심 기능을 자유롭게 이용하실 수 있습니다.",
    },
    {
      question: "데이터는 얼마나 자주 업데이트되나요?",
      answer:
        "공공데이터 API를 통해 실시간으로 데이터를 수집하며, 대부분의 데이터는 일일 단위로 업데이트됩니다. 일부 통계 데이터는 월간 또는 분기별로 업데이트됩니다.",
    },
    {
      question: "내가 작성한 제안이 실제 정책에 반영되나요?",
      answer:
        "높은 공감을 받은 우수 제안은 관련 기관에 전달되며, 실제로 정책에 반영된 사례들이 있습니다. 정책 반영 현황은 제안 상세 페이지에서 확인할 수 있습니다.",
    },
    {
      question: "리포트를 다른 사람과 공유할 수 있나요?",
      answer:
        "생성된 리포트는 PDF로 다운로드하거나 링크를 통해 공유할 수 있습니다. 개인정보가 포함된 내용은 자동으로 제외됩니다.",
    },
    {
      question: "모바일에서도 사용할 수 있나요?",
      answer: "네, 반응형 웹 디자인으로 제작되어 스마트폰과 태블릿에서도 최적화된 환경으로 이용하실 수 있습니다.",
    },
  ]

  return (
    <Card>
      <CardHeader>
        <CardTitle>자주 묻는 질문</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {faqs.map((faq, index) => (
            <Collapsible key={index}>
              <CollapsibleTrigger className="flex items-center justify-between w-full p-4 text-left hover:bg-gray-50 rounded-lg">
                <span className="font-medium">{faq.question}</span>
                <ChevronDown className="h-4 w-4" />
              </CollapsibleTrigger>
              <CollapsibleContent className="px-4 pb-4">
                <p className="text-gray-600">{faq.answer}</p>
              </CollapsibleContent>
            </Collapsible>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}
