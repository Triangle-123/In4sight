import { DeviceStatus } from '@/components/DeviceStatus'
import { Header } from '@/components/Header'
import { Recommendations } from '@/components/Recommendations'
import { Sidebar } from '@/components/Sidebar'
import { callHistoryPlaceholder, getAppliancePlaceholder } from '@/lib/placeholder-data'
import { ApplianceDataType, ApplianceType } from '@/lib/types'
import useStore from '@/store/store'
import { useEffect, useState } from 'react'

// import { v4 as uuidv4 } from 'uuid'

// Constants
// const MAX_RECONNECT_ATTEMPTS = 5
const API_URL = import.meta.env.VITE_API_BASE_URL
const TASK_ID = 'frontend_test'

// 전역 변수 선언
let globalSetSelectedAppliance: React.Dispatch<React.SetStateAction<ApplianceType | null>> | null = null

export default function Dashboard() {
  const createSseConnection = useStore((state) => state.createSseConnection)
  const closeSseConnection = useStore((state) => state.closeSseConnection)
  const setTaskId = useStore((state) => state.setTaskId)
  const setError = useStore((state) => state.setError)
  const isConnected = useStore((state) => state.isConnected)
  const error = useStore((state) => state.error)
  const customerInfo = useStore((state) => state.customerInfo)
  const appliances = useStore((state) => state.appliances)
  // const sensorData = useStore((state) => state.sensorData)
  // const eventData = useStore((state) => state.eventData)

  // UI States
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [loading, setLoading] = useState(false)
  const [selectedAppliance, setSelectedAppliance] = useState<ApplianceType | null>(null)
  const [applianceData, setApplianceData] = useState<ApplianceDataType | null>(null)
  // const [graphData, setGraphData] = useState(null)

  // 전역 변수에 setter 함수 할당
  globalSetSelectedAppliance = setSelectedAppliance

  useEffect(() => {
    if (selectedAppliance) {
      setApplianceData(getAppliancePlaceholder(selectedAppliance))
    }
  }, [selectedAppliance])

  useEffect(() => {
    // 고객 별로 상이한 taskId 사용
    const newTaskId = TASK_ID
    setTaskId(newTaskId)

    const eventSource = createSseConnection(newTaskId)
    console.log('eventSource', eventSource)
    // @Deprecated
    // startCounselling(newTaskId)

    return () => {
      console.log('SSE connection 제거')
      closeSseConnection()
    }
  }, [])

  // @Deprecated
  // const startCounselling = async (id: string) => {
  //   const currentTaskId = id || TASK_ID
  //   if (!currentTaskId) return

  //   setLoading(true)
  //   setError(null)

  //   try {
  //     const customerRequestDto = { customerName: '최싸피', phoneNumber: '010-1234-0004' }

  //     const response = await fetch(API_URL + `/counseling/${currentTaskId}`, {
  //       method: 'POST',
  //       headers: { 'Content-Type': 'application/json' },
  //       body: JSON.stringify(customerRequestDto),
  //     })

  //     if (!response.ok) {
  //       const errorText = await response.text()
  //       throw new Error(errorText || '솔루션 요청 중 오류가 발생했습니다')
  //     // } else {
  //     //   console.log('솔루션 요청 성공', response)
  //     }

  //     console.log('상담을 시작합니다...')
  //   } catch (err) {
  //     console.error('상담을 시작하지 못했습니다:', err)
  //     setError(err instanceof Error ? err.message : '솔루션 요청 중 오류가 발생했습니다')
  //   } finally {
  //     setLoading(false)
  //   }
  // }

  return (
    <div className="flex h-screen bg-background">
      {/* 사이드바 - 고객 정보, 고객의 가전 제품, 해당 고객과의 과거 통화 이력 */}
      <Sidebar
        sidebarOpen={sidebarOpen}
        selectedAppliance={selectedAppliance}
        setSelectedAppliance={setSelectedAppliance}
        customerInfo={customerInfo}
        appliances={appliances}
        callHistory={callHistoryPlaceholder}
      />
      {/* Main Content */}
      <div className="flex-1 flex flex-col h-full overflow-hidden">
        {/* Header */}
        <Header sidebarOpen={sidebarOpen} setSidebarOpen={setSidebarOpen} />

        {/* Main Panel */}
        <main className="flex-1 p-4 overflow-hidden">
          {error && <div className="mb-4 p-3 bg-red-50 border border-red-200 text-red-700 rounded">{error}</div>}

          {loading && (
            <div className="mb-4 p-3 bg-blue-50 border border-blue-200 text-blue-700 rounded">
              솔루션을 분석 중입니다...
            </div>
          )}

          {!isConnected && !error && (
            <div className="mb-4 p-3 bg-yellow-50 border border-yellow-200 text-yellow-700 rounded">
              서버에 연결 중입니다...
            </div>
          )}

          {selectedAppliance && applianceData ? (
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 h-full">
              {/* 왼쪽 섹션 - 제품 상태 모니터링 그래프들 */}
              <DeviceStatus applianceData={applianceData} />

              {/* 오른쪽 섹션 - 추천 솔루션(LLM) */}
              <Recommendations applianceData={applianceData} />
            </div>
          ) : (
            <div className="h-full flex items-center justify-center">
              <div className="text-center">
                {customerInfo ? (
                  <>
                    <h2 className="text-xl font-semibold mb-2">가전제품을 선택하세요</h2>
                    <p className="text-muted-foreground">
                      왼쪽 사이드바에서 가전제품을 선택하면 상세 정보가 표시됩니다.
                    </p>
                  </>
                ) : (
                  <h2 className="text-xl font-semibold mb-2">상담 대기 중입니다...</h2>
                )}
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
