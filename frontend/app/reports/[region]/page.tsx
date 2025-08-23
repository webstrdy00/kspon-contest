import { RegionalDetailReport } from "@/components/reports/regional-detail-report"
import { RegionalComparison } from "@/components/reports/regional-comparison"
import { RegionalRecommendations } from "@/components/reports/regional-recommendations"

export default function RegionalDetailPage({ params }: { params: { region: string } }) {
  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto p-6 space-y-8">
        <RegionalDetailReport region={params.region} />
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <RegionalComparison region={params.region} />
          <RegionalRecommendations region={params.region} />
        </div>
      </div>
    </div>
  )
}
