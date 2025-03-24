import { DeviceStatus } from '@/components/DeviceStatus'
import { Header } from '@/components/Header'
import { Recommendations } from '@/components/Recommendations'
import { Sidebar } from '@/components/Sidebar'
import { appliances, callHistory, getApplianceData } from '@/lib/applianceService'
import { useEffect, useRef, useState } from 'react'
import { v4 as uuidv4 } from 'uuid'

export default function Dashboard() {
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [selectedAppliance, setSelectedAppliance] = useState<string | null>(null)
  const [micEnabled, setMicEnabled] = useState(true)
  const [volumeEnabled, setVolumeEnabled] = useState(true)
  const [sseData, setSseData] = useState<any>(null)
  const [taskId, setTaskId] = useState<string>('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [reconnectCount, setReconnectCount] = useState(0)
  const [isConnected, setIsConnected] = useState(false)
  const maxReconnectAttempts = 5
  const reconnectTimeoutRef = useRef<NodeJS.Timeout | null>(null)
  const eventSourceRef = useRef<EventSource | null>(null)

  const applianceData = getApplianceData(selectedAppliance)

  const createSseConnection = (currentTaskId: string) => {
    if (eventSourceRef.current) {
      eventSourceRef.current.close()
    }

    console.log(`SSE 연결을 시도합니다: ${reconnectCount + 1} of ${maxReconnectAttempts}`)

    const API_URL = import.meta.env.VITE_API_BASE_URL
    const eventSource = new EventSource(`${API_URL}/counselling/${currentTaskId}`)
    eventSourceRef.current = eventSource

    eventSource.onopen = () => {
      console.log('SSE 연결 성공')
      setIsConnected(true)
      setError(null)
      setReconnectCount(0)
    }

    eventSource.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        console.log('SSE 데이터 수신:', data)
        setSseData(data)
      } catch (err) {
        console.error('SSE 데이터 파싱 에러:', event.data, err)
        setSseData(event.data)
      }
    }

    eventSource.onerror = (error) => {
      console.error('SSE 연결 에러:', error)
      setIsConnected(false)

      eventSource.close()

      if (reconnectCount < maxReconnectAttempts) {
        const nextReconnectDelay = Math.min(1000 * Math.pow(1.5, reconnectCount), 10000)
        console.log(`재 연결 시도 중... ${nextReconnectDelay}ms`)

        setError(`SSE 연결이 끊어졌습니다. 재연결을 시도합니다... (${reconnectCount + 1}/${maxReconnectAttempts})`)

        if (reconnectTimeoutRef.current) {
          clearTimeout(reconnectTimeoutRef.current)
        }

        reconnectTimeoutRef.current = setTimeout(() => {
          setReconnectCount((prev) => prev + 1)
          createSseConnection(currentTaskId)
        }, nextReconnectDelay)
      } else {
        setError('SSE 연결에 반복적으로 실패했습니다. 페이지를 새로고침 해주세요.')
      }
    }

    return eventSource
  }

  useEffect(() => {
    const newTaskId = uuidv4()
    setTaskId(newTaskId)

    const eventSource = createSseConnection(newTaskId)

    return () => {
      console.log('SSE connection 제거')
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current)
      }
      if (eventSource) {
        eventSource.close()
      }
    }
  }, [])

  useEffect(() => {
    if (selectedAppliance && taskId) {
      startCounselling()
    }
  }, [selectedAppliance, taskId])

  const startCounselling = async () => {
    if (!selectedAppliance || !taskId) return

    setLoading(true)
    setError(null)

    try {
      const customerRequestDto = { customerId: '고객ID', applianceId: selectedAppliance }

      const response = await fetch(`/api/counselling/${taskId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(customerRequestDto),
      })

      if (!response.ok) {
        const errorText = await response.text()
        throw new Error(errorText || '솔루션 요청 중 오류가 발생했습니다')
      }

      console.log('상담을 시작합니다...')
    } catch (err) {
      console.error('상담을 시작하지 못했습니다:', err)
      setError(err instanceof Error ? err.message : '솔루션 요청 중 오류가 발생했습니다')
    } finally {
      setLoading(false)
    }
  }

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
