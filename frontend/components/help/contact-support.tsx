import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Mail, MessageCircle, Phone, FileText } from "lucide-react"

export function ContactSupport() {
  const contacts = [
    {
      icon: <Mail className="h-5 w-5" />,
      title: "이메일 문의",
      description: "상세한 문의사항이나 기술적 문제",
      action: "support@sportslab.kr",
      color: "bg-blue-100 text-blue-600",
    },
    {
      icon: <MessageCircle className="h-5 w-5" />,
      title: "실시간 채팅",
      description: "빠른 답변이 필요한 간단한 질문",
      action: "채팅 시작",
      color: "bg-green-100 text-green-600",
    },
    {
      icon: <Phone className="h-5 w-5" />,
      title: "전화 상담",
      description: "긴급한 문제나 직접 상담",
      action: "02-1234-5678",
      color: "bg-orange-100 text-orange-600",
    },
    {
      icon: <FileText className="h-5 w-5" />,
      title: "개선 제안",
      description: "새로운 기능이나 서비스 개선 아이디어",
      action: "제안하기",
      color: "bg-purple-100 text-purple-600",
    },
  ]

  return (
    <Card>
      <CardHeader>
        <CardTitle>문의 및 지원</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {contacts.map((contact, index) => (
            <div key={index} className="flex items-start space-x-4 p-4 border rounded-lg">
              <div className={`flex-shrink-0 w-10 h-10 rounded-lg flex items-center justify-center ${contact.color}`}>
                {contact.icon}
              </div>
              <div className="flex-1">
                <h3 className="font-semibold mb-1">{contact.title}</h3>
                <p className="text-gray-600 text-sm mb-3">{contact.description}</p>
                <Button variant="outline" size="sm">
                  {contact.action}
                </Button>
              </div>
            </div>
          ))}
        </div>

        <div className="mt-6 p-4 bg-cyan-50 rounded-lg">
          <h4 className="font-semibold text-cyan-800 mb-2">운영 시간</h4>
          <p className="text-cyan-700 text-sm">
            평일: 09:00 - 18:00
            <br />
            주말 및 공휴일: 10:00 - 16:00
            <br />
            이메일 문의는 24시간 접수 가능합니다.
          </p>
        </div>
      </CardContent>
    </Card>
  )
}
