import { Button } from "@/components/ui/button"
import { Github, Mail } from "lucide-react"

export function Footer() {
  return (
    <footer className="bg-slate-900 text-white py-12 mt-16">
      <div className="px-6 lg:px-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div className="col-span-1 md:col-span-2">
            <h3 className="text-xl font-bold mb-4">스포츠 데이터랩</h3>
            <p className="text-slate-300 mb-4 max-w-md">
              공공데이터를 활용하여 시민과 함께 만드는 체육 정책 플랫폼입니다. 데이터 기반의 합리적인 정책 제안으로 더
              나은 체육 환경을 만들어갑니다.
            </p>
            <div className="flex space-x-4">
              <Button variant="ghost" size="sm" className="text-slate-300 hover:text-white">
                <Github className="h-4 w-4 mr-2" />
                GitHub
              </Button>
              <Button variant="ghost" size="sm" className="text-slate-300 hover:text-white">
                <Mail className="h-4 w-4 mr-2" />
                문의하기
              </Button>
            </div>
          </div>

          <div>
            <h4 className="font-semibold mb-4">주요 기능</h4>
            <ul className="space-y-2 text-slate-300">
              <li>
                <a href="/dashboard" className="hover:text-white">
                  데이터 대시보드
                </a>
              </li>
              <li>
                <a href="/reports" className="hover:text-white">
                  지역별 리포트
                </a>
              </li>
              <li>
                <a href="/proposals" className="hover:text-white">
                  정책 제안
                </a>
              </li>
              <li>
                <a href="/stats" className="hover:text-white">
                  통계 분석
                </a>
              </li>
            </ul>
          </div>

          <div>
            <h4 className="font-semibold mb-4">지원</h4>
            <ul className="space-y-2 text-slate-300">
              <li>
                <a href="/help" className="hover:text-white">
                  도움말
                </a>
              </li>
              <li>
                <a href="#" className="hover:text-white">
                  API 문서
                </a>
              </li>
              <li>
                <a href="#" className="hover:text-white">
                  개발자 가이드
                </a>
              </li>
              <li>
                <a href="#" className="hover:text-white">
                  공지사항
                </a>
              </li>
            </ul>
          </div>
        </div>

        <div className="border-t border-slate-700 mt-8 pt-8 text-center text-slate-400">
          <p>&copy; 2025 스포츠 데이터랩. 2025년 국민체육진흥공단 공공데이터 활용 경진대회 출품작</p>
        </div>
      </div>
    </footer>
  )
}
