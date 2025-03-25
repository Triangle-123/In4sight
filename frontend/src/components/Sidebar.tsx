'use client'

import { Button } from '@/components/ui/button'
import type { ApplianceType } from '@/lib/types'
import type { CustomerType } from '@/lib/types'
import { Refrigerator, WashingMachine } from 'lucide-react'

interface SidebarProps {
  sidebarOpen: boolean
  selectedAppliance: ApplianceType | null
  setSelectedAppliance: (appliance: ApplianceType) => void
  appliances: ApplianceType[] | null
  callHistory: { date: string; time: string; topic: string }[]
  customerInfo: CustomerType | null
}

export function Sidebar({
  sidebarOpen,
  selectedAppliance,
  setSelectedAppliance,
  appliances,
  callHistory,
  customerInfo,
}: SidebarProps) {
  return (
    <div
      style={{ width: sidebarOpen ? '20rem' : '0', marginLeft: sidebarOpen ? '0' : '-20rem' }}
      className="h-full bg-muted/40 border-r transition-all duration-300 flex flex-col"
    >
      <div className="p-4 border-b">
        <h2 className="font-semibold text-lg mb-2">고객 정보</h2>
        <div className="space-y-2 text-sm">
          <p>
            <span className="font-medium">이름:</span> {customerInfo ? customerInfo.customerName : ''}
          </p>
          <p>
            <span className="font-medium">전화번호:</span> {customerInfo ? customerInfo.phoneNumber : ''}
          </p>
          <p>
            <span className="font-medium">주소:</span> {customerInfo ? customerInfo.address : ''}
          </p>
          {/* <p>
            <p className="font-medium">문의 내용:</p> 에어컨 틀었는데 하나도 안 시원한데요???? 빨리 해결해주세요!!!
          </p> */}
        </div>
      </div>

      <div className="p-4 flex-1">
        <h2 className="font-semibold text-lg mb-2">고객 가전제품</h2>
        <div className="space-y-2">
          {appliances?.map((appliance) => (
            <Button
              key={appliance.serialNumber}
              variant={selectedAppliance === appliance ? 'default' : 'outline'}
              className="w-full justify-start overflow-hidden"
              onClick={() => setSelectedAppliance(appliance)}
            >
              {appliance.productType === 'REF' ? (
                <Refrigerator />
              ) : appliance.productType === 'WASH' ? (
                <WashingMachine />
              ) : (
                <div>기타 가전</div>
              )}
              <span
                className={`h-2 w-2 rounded-full${
                  appliance.status === 'normal'
                    ? 'bg-green-500'
                    : appliance.status === 'warning'
                      ? 'bg-yellow-500'
                      : 'bg-red-500'
                }`}
              />
              {appliance.modelName}
            </Button>
          ))}
        </div>
      </div>

      <div className="p-4 border-b">
        <h2 className="font-semibold text-lg mb-2">통화 기록</h2>
        <div className="space-y-2 text-sm">
          {callHistory.map((call, index) => (
            <div key={index} className="p-2 bg-background rounded-md">
              <p className="font-medium">
                {call.date} {call.time}
              </p>
              <p className="text-muted-foreground">{call.topic}</p>
            </div>
          ))}
        </div>
      </div>

      <div className="p-4 border-t flex justify-between">
        {/* <Button variant="outline" size="icon" onClick={() => setVolumeEnabled(!volumeEnabled)}>
          {volumeEnabled ? <Volume2 className="h-4 w-4" /> : <VolumeX className="h-4 w-4" />}
        </Button>
        <Button variant="outline" size="icon" onClick={() => setMicEnabled(!micEnabled)}>
          {micEnabled ? <Mic className="h-4 w-4" /> : <MicOff className="h-4 w-4" />}
        </Button> */}
        <p>전자연계 S004</p>
      </div>
    </div>
  )
}
