import { ApplianceType, CustomerType } from '@/lib/types'
import { resetSelectedAppliance } from '@/pages/Dashboard'
import { create } from 'zustand'

// SSE 관련 타입 정의
interface CustomerInfo {
  // 고객 정보 타입 정의
}

interface ApplianceInfo {
  // 기기 정보 타입 정의
}

interface SensorData {
  // 센서 데이터 타입 정의
}

interface EventData {
  // 이벤트 데이터 타입 정의
}

// 상태 타입 정의
interface State {
  // SSE 연결 상태
  isConnected: boolean
  error: string | null
  reconnectCount: number
  taskId: string | null

  // 데이터 상태
  customerInfo: CustomerType | null
  appliances: ApplianceType[]
  sensorData: any | null // 실제 센서 데이터 타입으로 교체 필요
  eventData: any | null // 실제 이벤트 데이터 타입으로 교체 필요
  selectedAppliance: ApplianceType | null
  solutionData: any | null // 실제 솔루션 데이터 타입으로 교체 필요
}

// 액션 타입 정의
interface Actions {
  // SSE 연결 관리
  createSseConnection: (taskId: string) => void
  closeSseConnection: () => void
  setTaskId: (taskId: string) => void

  // 데이터 업데이트
  setCustomerInfo: (data: CustomerType) => void
  setAppliances: (data: ApplianceType[]) => void
  setSensorData: (data: any) => void
  setEventData: (data: any) => void
  setSelectedAppliance: (appliance: ApplianceType | null) => void

  // 상태 업데이트
  setIsConnected: (isConnected: boolean) => void
  setError: (error: string | null) => void
  setReconnectCount: (count: number) => void
  reset: () => void
}

// 전체 store 타입
type Store = State & Actions

const MAX_RECONNECT_ATTEMPTS = 5
const API_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8080'

if (!import.meta.env.VITE_API_BASE_URL) {
  console.warn(
    '⚠️ VITE_API_BASE_URL이 설정되지 않았습니다. 기본값을 사용합니다.',
  )
}

// store 생성
const useStore = create<Store>((set, get) => {
  console.log('⚡️Zustand store 초기화')
  let eventSourceRef: EventSource | null = null
  let reconnectTimeoutRef: ReturnType<typeof setTimeout> | null = null

  const createSseConnection = (taskId: string) => {
    const { reconnectCount } = get()

    if (eventSourceRef) {
      eventSourceRef.close()
    }

    console.log(
      `SSE 연결을 시도합니다: ${reconnectCount + 1} of ${MAX_RECONNECT_ATTEMPTS}`,
    )

    const eventSource = new EventSource(`${API_URL}/counseling`)
    eventSourceRef = eventSource

    eventSource.onopen = () => {
      console.log('SSE 연결 성공')
      set({ isConnected: true, error: null, reconnectCount: 0 })
    }

    eventSource.onmessage = (event) => {
      try {
        console.log('SSE 데이터 수신:', event.data)
      } catch (err) {
        console.error('SSE 데이터 파싱 에러:', event.data, err)
      }
    }

    eventSource.onerror = (error) => {
      console.error('SSE 연결 에러:', error)
      set({ isConnected: false })

      eventSource.close()

      if (reconnectCount < MAX_RECONNECT_ATTEMPTS) {
        const nextReconnectDelay = Math.min(
          1000 * Math.pow(1.5, reconnectCount),
          10000,
        )
        console.log(`재연결 시도 중... ${nextReconnectDelay}ms`)

        set({
          error: `SSE 연결이 끊어졌습니다. 재연결을 시도합니다... (${reconnectCount + 1}/${MAX_RECONNECT_ATTEMPTS})`,
        })

        if (reconnectTimeoutRef) {
          clearTimeout(reconnectTimeoutRef)
        }

        reconnectTimeoutRef = setTimeout(() => {
          set((state) => ({ reconnectCount: state.reconnectCount + 1 }))
          createSseConnection(taskId)
        }, nextReconnectDelay)
      } else {
        set({
          error:
            'SSE 연결에 반복적으로 실패했습니다. 페이지를 새로고침 해주세요.',
        })
      }
    }

    eventSource.addEventListener('customer-info', (event) => {
      try {
        console.log('고객 정보 수신:', event.data)
        const customerData = JSON.parse(event.data)
        set({ customerInfo: customerData })
      } catch (err) {
        console.error('고객 정보 파싱 에러:', event.data, err)
      }
    })

    eventSource.addEventListener('device-info', (event) => {
      try {
        console.log('기기 정보 수신:', event.data)
        const applianceData = JSON.parse(event.data)
        set({ appliances: applianceData })
      } catch (err) {
        console.error('기기 정보 파싱 에러:', event.data, err)
      }
    })

    eventSource.addEventListener('sensor-data', (event) => {
      try {
        console.log('센서 정보 수신:', event.data)
        const sensorData = JSON.parse(event.data)
        set({ sensorData })
      } catch (err) {
        console.error('센서 정보 파싱 에러:', event.data, err)
      }
    })

    eventSource.addEventListener('event-data', (event) => {
      try {
        console.log('이벤트 정보 수신:', event.data)
        const eventData = JSON.parse(event.data)
        set({ eventData })
      } catch (err) {
        console.error('이벤트 정보 파싱 에러:', event.data, err)
      }
    })

    // TODO: 이벤트 이름 수정(solution -> solution-data)
    eventSource.addEventListener('solution', (event) => {
      try {
        console.log('솔루션 정보 수신:', event.data)
        const solutionData = JSON.parse(event.data)
        set((state) => ({ solutionData: [...state.solutionData, solutionData] }))
      } catch (err) {
        console.error('솔루션 정보 파싱 에러:', event.data, err)
      }
    })

    eventSource.addEventListener('customer_disconnect', (event) => {
      try {
        console.log('고객 연결 끊김:', event.data)
        get().reset()
        resetSelectedAppliance(null)
      } catch (err) {
        console.error('고객 연결 끊김 파싱 에러:', event.data, err)
      }
    })


    return eventSource
  }

  const closeSseConnection = () => {
    if (reconnectTimeoutRef) {
      clearTimeout(reconnectTimeoutRef)
    }
    if (eventSourceRef) {
      eventSourceRef.close()
    }
  }

  return {
    // 초기 상태
    isConnected: false,
    error: null,
    reconnectCount: 0,
    taskId: null,
    customerInfo: null,
    appliances: [],
    sensorData: {
      taskId: null,
      serialNumber: null,
      sensor_data: [],
    },
    eventData: null,
    solutionData: [],
    selectedAppliance: null,

    // 액션
    createSseConnection,
    closeSseConnection,
    setTaskId: (taskId) => set({ taskId }),
    setCustomerInfo: (data) => set({ customerInfo: data }),
    setAppliances: (data) => set({ appliances: data }),
    setSensorData: (data) => set({ sensorData: data }),
    setEventData: (data) => set({ eventData: data }),
    setSolutionData: (data) => set({ solutionData: data }),
    setSelectedAppliance: (appliance) => {
      set({ selectedAppliance: appliance })
      console.log('선택된 기기:', appliance)
    },
    setIsConnected: (isConnected) => set({ isConnected }),
    setError: (error) => set({ error }),
    setReconnectCount: (count) => set({ reconnectCount: count }),
    reset: () =>
      set({
        error: null,
        reconnectCount: 0,
        taskId: null,
        customerInfo: null,
        appliances: [],
        sensorData: null,
        eventData: null,
        selectedAppliance: null,
        solutionData: [],
      }),
  }
})

export default useStore
