'use client'

import { Button } from '@/components/ui/button'
import type { ApplianceType } from '@/lib/types'
import { Mic, MicOff, Volume2, VolumeX } from 'lucide-react'

interface SidebarProps {
  sidebarOpen: boolean
  selectedAppliance: string | null
  setSelectedAppliance: (id: string) => void
  micEnabled: boolean
  setMicEnabled: (enabled: boolean) => void
  volumeEnabled: boolean
  setVolumeEnabled: (enabled: boolean) => void
  appliances: ApplianceType[]
  callHistory: { date: string; time: string; topic: string }[]
}

export function Sidebar({
  sidebarOpen,
  selectedAppliance,
  setSelectedAppliance,
  micEnabled,
  setMicEnabled,
  volumeEnabled,
  setVolumeEnabled,
  appliances,
  callHistory,
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
            <span className="font-medium">이름:</span> 김지은
          </p>
          <p>
            <span className="font-medium">전화번호:</span> 010-1234-5678
          </p>
          <p>
            <span className="font-medium">주소:</span> 서울시 강남구 테헤란로 123
          </p>
          <p>
            <span className="font-medium">문의 내용:</span> 가전제품 오작동
          </p>
        </div>
      </div>

      <div className="p-4 flex-1">
        <h2 className="font-semibold text-lg mb-2">고객 가전제품</h2>
        <div className="space-y-2">
          {appliances.map((appliance) => (
            <Button
              key={appliance.id}
              variant={selectedAppliance === appliance.id ? 'default' : 'outline'}
              className="w-full justify-start"
              onClick={() => setSelectedAppliance(appliance.id)}
            >
              <span
                className={`mr-2 h-2 w-2 rounded-full ${
                  appliance.status === 'normal'
                    ? 'bg-green-500'
                    : appliance.status === 'warning'
                      ? 'bg-yellow-500'
                      : 'bg-red-500'
                }`}
              />
              {appliance.name}
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
        <Button variant="outline" size="icon" onClick={() => setVolumeEnabled(!volumeEnabled)}>
          {volumeEnabled ? <Volume2 className="h-4 w-4" /> : <VolumeX className="h-4 w-4" />}
        </Button>
        <Button variant="outline" size="icon" onClick={() => setMicEnabled(!micEnabled)}>
          {micEnabled ? <Mic className="h-4 w-4" /> : <MicOff className="h-4 w-4" />}
        </Button>
      </div>
    </div>
  )
}
