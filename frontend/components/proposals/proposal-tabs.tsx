"use client"

import { useState } from "react"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { ProposalList } from "./proposal-list"
import { CreateProposal } from "./create-proposal"
import { ProposalRanking } from "./proposal-ranking"

export function ProposalTabs() {
  const [activeTab, setActiveTab] = useState("list")

  return (
    <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
      <TabsList className="grid w-full grid-cols-3">
        <TabsTrigger value="list">전체 제안</TabsTrigger>
        <TabsTrigger value="ranking">인기 제안</TabsTrigger>
        <TabsTrigger value="create">제안 작성</TabsTrigger>
      </TabsList>

      <TabsContent value="list" className="space-y-6">
        <ProposalList />
      </TabsContent>

      <TabsContent value="ranking" className="space-y-6">
        <ProposalRanking />
      </TabsContent>

      <TabsContent value="create" className="space-y-6">
        <CreateProposal />
      </TabsContent>
    </Tabs>
  )
}
