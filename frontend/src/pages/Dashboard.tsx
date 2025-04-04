import { DeviceStatus } from '@/components/DeviceStatus'
import { Header } from '@/components/Header'
import { Recommendations } from '@/components/Recommendations'
import { Sidebar } from '@/components/Sidebar'
import {
  callHistoryPlaceholder,
  getAppliancePlaceholder,
} from '@/lib/placeholder-data'
import { ApplianceDataType, ApplianceType } from '@/lib/types'
import useStore from '@/store/store'
import { useEffect, useState } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'

// import { v4 as uuidv4 } from 'uuid'

// Constants
// const API_URL = import.meta.env.VITE_API_BASE_URL
const TASK_ID = 'frontend_test'

// 전역 변수 선언
let globalSetSelectedAppliance: React.Dispatch<
  React.SetStateAction<ApplianceType | null>
> | null = null

export default function Dashboard() {
  const createSseConnection = useStore((state) => state.createSseConnection)
  const closeSseConnection = useStore((state) => state.closeSseConnection)
  const setTaskId = useStore((state) => state.setTaskId)
  const setError = useStore((state) => state.setError)
  const isConnected = useStore((state) => state.isConnected)
  const error = useStore((state) => state.error)
  const customerInfo = useStore((state) => state.customerInfo)
  const appliances = useStore((state) => state.appliances)
  const selectedAppliance = useStore((state) => state.selectedAppliance)
  const setSelectedAppliance = useStore((state) => state.setSelectedAppliance)
  // const sensorData = useStore((state) => state.sensorData)
  // const eventData = useStore((state) => state.eventData)
  const navigate = useNavigate()
  const setNavigate = useStore((state) => state.setNavigate)
  // UI States
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [loading, setLoading] = useState(false)
  const [applianceData, setApplianceData] = useState<ApplianceDataType | null>(
    null,
  )
  // const [graphData, setGraphData] = useState(null)

  // 전역 변수에 setter 함수 할당
  globalSetSelectedAppliance = setSelectedAppliance
  setNavigate(navigate)

  useEffect(() => {
    if (!isConnected) {
      createSseConnection('')
    }
  }, [isConnected])

  useEffect(() => {
    if (selectedAppliance) {
      setApplianceData(getAppliancePlaceholder(selectedAppliance))
    }
  }, [selectedAppliance])

  // 상담사 상담 종료 요청 이벤트
  const handleDisconnect = () => {
    fetch(`${API_URL}/counseling/customer/disconnect`, {
      method: 'POST',
      body: customerInfo?.phoneNumber,
    })
  }

  return (
    <div className="flex h-screen bg-background">
      {/* 사이드바 - 고객 정보, 고객의 가전 제품, 해당 고객과의 과거 통화 이력 */}
      <Sidebar
        sidebarOpen={sidebarOpen}
        customerInfo={customerInfo}
        appliances={appliances}
        callHistory={callHistoryPlaceholder}
      />
      {/* Main Content */}
      <div className="flex-1 flex flex-col h-full overflow-hidden">
        {/* Header */}
        <Header />

        {/* Main Panel */}
        <main className="flex-1 p-4 overflow-hidden">
          {/* {error && (
            <div className="mb-4 p-3 bg-red-50 border border-red-200 text-red-700 rounded">
              {error}
            </div>
          )}

          {loading && (
            <div className="mb-4 p-3 bg-blue-50 border border-blue-200 text-blue-700 rounded">
              솔루션을 분석 중입니다...
            </div>
          )}

          {!isConnected && !error && (
            <div className="mb-4 p-3 bg-yellow-50 border border-yellow-200 text-yellow-700 rounded">
              서버에 연결 중입니다...
            </div>
          )} */}

          {selectedAppliance != null ? (
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 h-full overflow-hidden">
              {/* 왼쪽 섹션 - 제품 상태 모니터링 그래프들 */}
              <DeviceStatus />

              {/* 오른쪽 섹션 - 추천 솔루션(LLM) */}
              <Recommendations />
            </div>
          ) : (
            <div className="h-full flex items-center justify-center">
              <div className="text-center">
                <h2 className="text-xl font-semibold mb-2">
                  가전제품을 선택하세요
                </h2>
                <p className="text-muted-foreground">
                  왼쪽 사이드바에서 가전제품을 선택하면 상세 정보가 표시됩니다.
                </p>
              </div>
            </div>
          )}
        </main>
      </div>
    </div>
  )
}

// 함수 이름을 변경하여 재귀 호출 문제 해결
export const resetSelectedAppliance = (appliance: ApplianceType | null) => {
  if (globalSetSelectedAppliance) {
    globalSetSelectedAppliance(appliance)
  }
}
