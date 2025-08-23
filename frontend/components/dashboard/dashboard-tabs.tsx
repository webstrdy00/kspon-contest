"use client"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { SupplyDemandMap } from "./supply-demand-map"
import { BudgetPerformanceAnalysis } from "./budget-performance-analysis"

export function DashboardTabs() {
  return (
    <Tabs defaultValue="supply-demand" className="space-y-6">
      <TabsList className="grid w-full grid-cols-2">
        <TabsTrigger value="supply-demand">수요-공급 분석</TabsTrigger>
        <TabsTrigger value="budget-performance">예산-성과 분석</TabsTrigger>
      </TabsList>

      <TabsContent value="supply-demand" className="space-y-6">
        <SupplyDemandMap />
      </TabsContent>

      <TabsContent value="budget-performance" className="space-y-6">
        <BudgetPerformanceAnalysis />
      </TabsContent>
    </Tabs>
  )
}
