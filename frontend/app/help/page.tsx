import { HelpHeader } from "@/components/help/help-header"
import { QuickStart } from "@/components/help/quick-start"
import { FeatureGuides } from "@/components/help/feature-guides"
import { FAQ } from "@/components/help/faq"
import { ContactSupport } from "@/components/help/contact-support"

export default function HelpPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <HelpHeader />

      <div className="max-w-4xl mx-auto p-6 space-y-8">
        <QuickStart />
        <FeatureGuides />
        <FAQ />
        <ContactSupport />
      </div>
    </div>
  )
}
