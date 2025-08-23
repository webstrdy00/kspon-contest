import { Header } from "@/components/layout/header"
import { NavigationMenu } from "@/components/layout/navigation-menu"
import { ReportGenerator } from "@/components/reports/report-generator"
import { ReportHeader } from "@/components/reports/report-header"

export default function ReportsPage() {
  return (
    <div className="min-h-screen bg-background">
      <Header />
      <NavigationMenu />
      <div className="container mx-auto p-6 space-y-6">
        <ReportHeader />
        <ReportGenerator />
      </div>
    </div>
  )
}
