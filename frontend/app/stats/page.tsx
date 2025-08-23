import { StatsHeader } from "@/components/stats/stats-header"
import { PlatformOverview } from "@/components/stats/platform-overview"
import { UserEngagement } from "@/components/stats/user-engagement"
import { ProposalTrends } from "@/components/stats/proposal-trends"
import { RegionalActivity } from "@/components/stats/regional-activity"
import { DataUsage } from "@/components/stats/data-usage"

export default function StatsPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <StatsHeader />

      <div className="max-w-7xl mx-auto p-6 space-y-8">
        <PlatformOverview />

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <UserEngagement />
          <ProposalTrends />
        </div>

        <RegionalActivity />

        <DataUsage />
      </div>
    </div>
  )
}
