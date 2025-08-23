import { ProposalDetail } from "@/components/proposals/proposal-detail"
import { ProposalComments } from "@/components/proposals/proposal-comments"
import { RelatedProposals } from "@/components/proposals/related-proposals"

export default function ProposalDetailPage({ params }: { params: { id: string } }) {
  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto p-6 space-y-8">
        <ProposalDetail proposalId={params.id} />
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2">
            <ProposalComments proposalId={params.id} />
          </div>
          <div>
            <RelatedProposals proposalId={params.id} />
          </div>
        </div>
      </div>
    </div>
  )
}
