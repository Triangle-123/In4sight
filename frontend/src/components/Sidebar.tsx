'use client'

import { Button } from '@/components/ui/button'
import useStore from '@/store/store'
import { Refrigerator, WashingMachine, X } from 'lucide-react'

interface SidebarProps {
  callHistory: { date: string; time: string; topic: string }[]
}

export function Sidebar({ callHistory }: SidebarProps) {
  const selectedAppliance = useStore((state) => state.selectedAppliance)
  const setSelectedAppliance = useStore((state) => state.setSelectedAppliance)
  const customerInfo = useStore((state) => state.customerInfo)
  const appliances = useStore((state) => state.appliances)

  // 상담사 상담 종료 요청 이벤트
  const handleDisconnect = () => {
    fetch(`${API_URL}/counseling/customer/disconnect`, {
      method: 'POST',
      body: customerInfo?.phoneNumber,
    })
  }

  return (
    <div className="w-80 h-full bg-muted/40 border-r flex flex-col">
      <div className="p-4 border-b">
        <h2 className="font-semibold text-lg mb-2">고객 정보</h2>
        <div className="space-y-2 text-sm">
          <p>
            <span className="font-medium">이름:</span>{' '}
            {customerInfo ? customerInfo.customerName : ''}
          </p>
          <p>
            <span className="font-medium">전화번호:</span>{' '}
            {customerInfo ? customerInfo.phoneNumber : ''}
          </p>
          <p>
            <span className="font-medium">주소:</span>{' '}
            {customerInfo ? customerInfo.address : ''}
          </p>
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

      <div className="p-3 border-t flex justify-between">
        <Button 
          variant="outline" 
          onClick={() => {
            console.log('상담 종료')
          }} 
          className="w-full text-white bg-red-600 hover:bg-red-700 hover:text-white"
        >
          <X className="h-4 w-4 mr-2" />
          상담 종료
        </Button>
      </div>
    </div>
  )
}
