import { Header } from '@/components/Header'
import { Recommendations } from '@/components/Recommendations'
import { Sidebar } from '@/components/Sidebar'
import { appliances, callHistory, getApplianceData } from '@/lib/applianceService'
import { useState } from 'react'

export default function Dashboard() {
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [selectedAppliance, setSelectedAppliance] = useState<string | null>(null)
  const [micEnabled, setMicEnabled] = useState(true)
  const [volumeEnabled, setVolumeEnabled] = useState(true)

  const applianceData = getApplianceData(selectedAppliance)

  return (
    <div className="flex h-screen bg-background">
      {/* 사이드바 - 고객 정보, 고객의 가전 제품, 해당 고객과의 과거 통화 이력 */}
      <Sidebar
        sidebarOpen={sidebarOpen}
        selectedAppliance={selectedAppliance}
        setSelectedAppliance={setSelectedAppliance}
        micEnabled={micEnabled}
        setMicEnabled={setMicEnabled}
        volumeEnabled={volumeEnabled}
        setVolumeEnabled={setVolumeEnabled}
        appliances={appliances}
        callHistory={callHistory}
      />
      {/* Main Content */}
      <div className="flex-1 flex flex-col h-full overflow-hidden">
        {/* Header */}
        <Header sidebarOpen={sidebarOpen} setSidebarOpen={setSidebarOpen} />

        {/* Main Panel */}
        <main className="flex-1 p-4 overflow-hidden">
          {selectedAppliance && applianceData ? (
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 h-full">
              {/* 왼쪽 섹션 - 제품 상태 모니터링 그래프들들 */}
              {/* 오른쪽 섹션 - 추천 솔루션(LLM) */}
              <Recommendations applianceData={applianceData} />
            </div>
          ) : (
            <div className="h-full flex items-center justify-center">
              <div className="text-center">
                <h2 className="text-xl font-semibold mb-2">가전제품을 선택하세요</h2>
                <p className="text-muted-foreground">왼쪽 사이드바에서 가전제품을 선택하면 상세 정보가 표시됩니다.</p>
              </div>
            </div>
          )}
        </main>
      </div>
    </div>
  )
}
