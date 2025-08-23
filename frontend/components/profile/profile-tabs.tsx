"use client"

import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { MyProposals } from "./my-proposals"
import { MyActivity } from "./my-activity"
import { ProfileSettings } from "./profile-settings"

export function ProfileTabs() {
  return (
    <Tabs defaultValue="proposals" className="space-y-6">
      <TabsList className="grid w-full grid-cols-3">
        <TabsTrigger value="proposals">내 제안</TabsTrigger>
        <TabsTrigger value="activity">활동 내역</TabsTrigger>
        <TabsTrigger value="settings">설정</TabsTrigger>
      </TabsList>

      <TabsContent value="proposals" className="space-y-6">
        <MyProposals />
      </TabsContent>

      <TabsContent value="activity" className="space-y-6">
        <MyActivity />
      </TabsContent>

      <TabsContent value="settings" className="space-y-6">
        <ProfileSettings />
      </TabsContent>
    </Tabs>
  )
}
