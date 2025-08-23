import { NotificationHeader } from "@/components/notifications/notification-header"
import { NotificationTabs } from "@/components/notifications/notification-tabs"
import { NotificationList } from "@/components/notifications/notification-list"

export default function NotificationsPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <NotificationHeader />

      <div className="max-w-4xl mx-auto p-6">
        <NotificationTabs />
        <NotificationList />
      </div>
    </div>
  )
}
