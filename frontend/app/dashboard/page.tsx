import { Header } from "@/components/layout/header"
import { NavigationMenu } from "@/components/layout/navigation-menu"
import { DashboardTabs } from "@/components/dashboard/dashboard-tabs"
import { DashboardHeader } from "@/components/dashboard/dashboard-header"

export default function DashboardPage() {
  return (
    <div className="min-h-screen bg-background">
      <Header />
      <NavigationMenu />
      <div className="container mx-auto p-6 space-y-6">
        <DashboardHeader />
        <DashboardTabs />
      </div>
    </div>
  )
}
