"use client"

import { useState } from "react"
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Badge } from "@/components/ui/badge"

export function NotificationTabs() {
  const [activeTab, setActiveTab] = useState("all")

  const tabs = [
    { id: "all", label: "전체", count: 12 },
    { id: "proposals", label: "제안 관련", count: 5 },
    { id: "reports", label: "리포트", count: 3 },
    { id: "system", label: "시스템", count: 4 },
  ]

  return (
    <div className="mb-6">
      <Tabs value={activeTab} onValueChange={setActiveTab}>
        <TabsList className="grid w-full grid-cols-4">
          {tabs.map((tab) => (
            <TabsTrigger key={tab.id} value={tab.id} className="flex items-center space-x-2">
              <span>{tab.label}</span>
              {tab.count > 0 && (
                <Badge variant="secondary" className="ml-1 text-xs">
                  {tab.count}
                </Badge>
              )}
            </TabsTrigger>
          ))}
        </TabsList>
      </Tabs>
    </div>
  )
}
