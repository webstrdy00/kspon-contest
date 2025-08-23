import { Header } from "@/components/layout/header"
import { NavigationMenu } from "@/components/layout/navigation-menu"
import { ProposalHeader } from "@/components/proposals/proposal-header"
import { ProposalTabs } from "@/components/proposals/proposal-tabs"

export default function ProposalsPage() {
  return (
    <div className="min-h-screen bg-background">
      <Header />
      <NavigationMenu />
      <div className="container mx-auto p-6 space-y-6">
        <ProposalHeader />
        <ProposalTabs />
      </div>
    </div>
  )
}
