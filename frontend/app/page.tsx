import { Header } from "@/components/layout/header"
import { Sidebar } from "@/components/layout/sidebar"
import { HeroSection } from "@/components/home/hero-section"
import { FeaturesOverview } from "@/components/home/features-overview"
import { LiveStats } from "@/components/home/live-stats"
import { RecentActivity } from "@/components/home/recent-activity"
import { QuickStart } from "@/components/home/quick-start"
import { DataPreview } from "@/components/home/data-preview"
import { ImpactShowcase } from "@/components/home/impact-showcase"
import { Footer } from "@/components/layout/footer"

export default function HomePage() {
  return (
    <div className="min-h-screen bg-background">
      <Header />
      <div className="flex">
        <Sidebar />
        <div className="flex-1">
          <main className="w-full">
            <div className="space-y-12">
              <HeroSection />
              <div className="px-6 lg:px-12 space-y-12">
                <LiveStats />
                <DataPreview />
                <FeaturesOverview />
                <ImpactShowcase />
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                  <RecentActivity />
                  <QuickStart />
                </div>
              </div>
            </div>
          </main>
          <Footer />
        </div>
      </div>
    </div>
  )
}
