'use client'

import MarqueeButton from '@/components/MarqueeButton'
import { Button } from '@/components/ui/button'
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarHeader,
} from '@/components/ui/sidebar'
import useStore from '@/store/store'
import { X } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import { callHistoryPlaceholder } from '@/lib/placeholder-data'

const API_URL = import.meta.env.VITE_API_BASE_URL

export default function DashboardSidebar() {
  const selectedAppliance = useStore((state) => state.selectedAppliance)
  const setSelectedAppliance = useStore((state) => state.setSelectedAppliance)
  const customerInfo = useStore((state) => state.customerInfo)
  const appliances = useStore((state) => state.appliances)
  const navigate = useNavigate()
  const reset = useStore((state) => state.reset)

  // 상담사 상담 종료 요청 이벤트
  const handleDisconnect = () => {
    fetch(`${API_URL}/counseling/customer/disconnect`, {
      method: 'POST',
      body: customerInfo?.phoneNumber,
    })
      .then((response) => {
        console.log('상담 종료 요청 성공:', response)
      })
      .catch((error) => {
        console.error('상담 종료 요청 실패:', error)
      })
  }

  return (
    <Sidebar>
      <SidebarHeader className="border-b">
        <h2 className="font-bold text-lg mb-2">고객 정보</h2>
        <div className="space-y-2 text-sm overflow-x-hidden">
          <p>
            <span className="font-semibold">이름 : </span>
            <span>{customerInfo ? customerInfo.customerName : ''}</span>
          </p>
          <p>
            <span className="font-semibold">전화번호 : </span>
            <span>{customerInfo ? customerInfo.phoneNumber : ''}</span>
          </p>
          <p>
            <span className="font-semibold">주소 : </span>
            <span>{customerInfo ? customerInfo.address : ''}</span>
          </p>
        </div>
      </SidebarHeader>

      <SidebarContent>
        <SidebarGroup className="grow border-b">
          <h2 className="font-bold text-lg mb-2">고객 가전제품</h2>
          <div className="space-y-2">
            {appliances?.map((appliance) => (
              <MarqueeButton
                key={appliance.serialNumber}
                className={`w-full ${selectedAppliance?.serialNumber === appliance.serialNumber ? '!bg-blue-600 !text-white hover:!bg-blue-700' : 'hover:bg-gray-100'}`}
                onClick={() => setSelectedAppliance(appliance)}
              >
                {appliance.modelName}
              </MarqueeButton>
            ))}
          </div>
        </SidebarGroup>

        <SidebarGroup className="border-b">
          <h2 className="font-semibold text-lg mb-2">통화 기록</h2>
          <div className="space-y-2 text-sm">
            {callHistoryPlaceholder.map((call, index) => (
              <div key={index} className="p-2 bg-background rounded-md">
                <p className="font-medium">
                  {call.date} {call.time}
                </p>
                <p className="text-muted-foreground">{call.topic}</p>
              </div>
            ))}
          </div>
        </SidebarGroup>
      </SidebarContent>
      <SidebarFooter>
        <Button
          variant="outline"
          onClick={() => {
            console.log('상담 종료')
          }}
          className="text-white bg-red-600 hover:bg-white hover:text-red-600 hover:shadow-md"
        >
          <X className="h-4 w-4 mr-2" />
          상담 종료
        </Button>
      </SidebarFooter>
    </Sidebar>
  )
}
