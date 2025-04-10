import useStore from '@/store/store'
import { useEffect } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'

export default function CallQueue() {
  const navigate = useNavigate()
  const removeFromCallQueue = useStore((state) => state.removeFromCallQueue)
  const createSseConnection = useStore((state) => state.createSseConnection)
  const isConnected = useStore((state) => state.isConnected)
  const callQueue = useStore((state) => state.callQueue)
  const API_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8080'

  useEffect(() => {
    if (!isConnected) {
      createSseConnection('')
    }
  }, [isConnected])

  // 고객 전화 연결결
  const handleTakeCall = (phoneNumber: string) => {
    removeFromCallQueue(phoneNumber)
    console.log('Call taken:', phoneNumber)
    fetch(`${API_URL}/counseling/customer/connect`, {
      method: 'POST',
      body: phoneNumber,
    })
    navigate('/dashboard')
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-6xl mx-auto">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-3xl font-bold">고객 요청 대기열</h1>
        </div>

        <div className="bg-white rounded-lg shadow overflow-hidden">
          {callQueue.length === 0 ? (
            <div className="p-8 text-center">
              <p className="text-gray-500 text-lg">현재 대기열에 수신된 전화가 없습니다</p>
              <p className="text-gray-400">
                전화가 수신되면 이 곳에 표시됩니다
              </p>
            </div>
          ) : (
            <div>
              {/* Table header */}
              <div className="grid grid-cols-12 gap-4 p-4 font-medium text-sm text-gray-500 border-b bg-gray-50">
                <div className="col-span-2">이름</div>
                <div className="col-span-2">전화번호</div>
                <div className="col-span-2">전화한 시간</div>
                <div className="col-span-4">주소</div>
                <div className="col-span-2"></div>
              </div>

              {/* Call list */}
              <div className="divide-y">
                {callQueue.map((call) => (
                  <div
                    key={call.phoneNumber}
                    className="grid grid-cols-12 gap-4 p-4 items-center hover:bg-gray-50"
                  >
                    <div className="col-span-2 flex items-center gap-2">
                      <svg
                        className="h-4 w-4 text-gray-500"
                        xmlns="http://www.w3.org/2000/svg"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="2"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                      >
                        <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                        <circle cx="12" cy="7" r="4"></circle>
                      </svg>
                      <span>{call.customerName}</span>
                    </div>
                    <div className="col-span-2 flex items-center gap-2">
                      <svg
                        className="h-4 w-4 text-gray-500"
                        xmlns="http://www.w3.org/2000/svg"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="2"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                      >
                        <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path>
                      </svg>
                      <span>{call.phoneNumber}</span>
                    </div>
                    <div className="col-span-2 flex items-center gap-2">
                      <svg
                        className="h-4 w-4 text-gray-500"
                        xmlns="http://www.w3.org/2000/svg"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="2"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                      >
                        <circle cx="12" cy="12" r="10"></circle>
                        <polyline points="12 6 12 12 16 14"></polyline>
                      </svg>
                      <span>{call.timestamp.toLocaleTimeString()}</span>
                    </div>
                    <div className="col-span-4 font-medium">{call.address}</div>
                    <div className="col-span-2 text-right">
                      <button
                        onClick={() => handleTakeCall(call.phoneNumber)}
                        className="px-3 py-1 bg-blue-600 text-white text-sm rounded hover:bg-blue-700"
                      >
                        상담시작
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
