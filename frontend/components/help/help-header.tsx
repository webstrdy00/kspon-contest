import { Search } from "lucide-react"
import { Input } from "@/components/ui/input"

export function HelpHeader() {
  return (
    <div className="bg-gradient-to-r from-cyan-600 to-orange-600 text-white">
      <div className="max-w-4xl mx-auto p-8 text-center">
        <h1 className="text-4xl font-bold mb-4">도움말 센터</h1>
        <p className="text-xl text-cyan-100 mb-8">스포츠 데이터랩 사용법을 쉽게 배워보세요</p>

        <div className="max-w-md mx-auto relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
          <Input placeholder="궁금한 내용을 검색하세요..." className="pl-10 bg-white text-gray-900" />
        </div>
      </div>
    </div>
  )
}
