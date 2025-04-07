import DashboardSidebar from '@/components/DashboardSidebar'
import { DeviceStatus } from '@/components/DeviceStatus'
import { Recommendations } from '@/components/Recommendations'
import { Separator } from '@/components/ui/separator'
import { SidebarProvider, SidebarTrigger } from '@/components/ui/sidebar'
import useStore from '@/store/store'
import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'

export default function Dashboard() {
  const createSseConnection = useStore((state) => state.createSseConnection)
  const isConnected = useStore((state) => state.isConnected)
  const selectedAppliance = useStore((state) => state.selectedAppliance)
  const navigate = useNavigate()
  const setNavigate = useStore((state) => state.setNavigate)
  const [ip, setIp] = useState<string>('확인 중...')

  useEffect(() => {
    const fetchIP = async () => {
      try {
        const response = await fetch('https://api.ipify.org?format=json')
        const data = await response.json()
        setIp(data.ip)
      } catch (error) {
        console.error('IP 주소를 가져오는데 실패했습니다:', error)
        setIp('확인 실패')
      }
    }

    fetchIP()
  }, [])

  useEffect(() => {
    setNavigate(navigate)
  }, [navigate, setNavigate])

  useEffect(() => {
    if (!isConnected) {
      createSseConnection('')
    }
  }, [isConnected, createSseConnection])

  return (
    <SidebarProvider 
      className="h-screen"
      style={{ "--sidebar-width": "18rem" } as React.CSSProperties}
    >
      <DashboardSidebar />
      <main className="flex-1 overflow-hidden">
        <header className="h-[5vh] border-b flex items-center justify-between px-4">
          <div className="flex gap-2">
            <SidebarTrigger />
            <h1 className="font-bold text-lg">고객 지원 대시보드</h1>
          </div>
          <div className="flex items-center gap-4">
            <div className="text-sm">
              <span className="font-semibold">상담사 : </span>
              <span>조현준 (대전 센터)</span>
              <Separator />
              <span className="font-semibold">접속 IP : </span>
              <span>{ip}</span>
            </div>
          </div>
        </header>
        {selectedAppliance != null ? (
          <div className="h-[95vh] grid grid-cols-1 lg:grid-cols-3 gap-4 p-4">
            <DeviceStatus />
            <Recommendations />
          </div>
        ) : (
          <div className="h-[95vh] flex items-center justify-center">
            <div className="text-center">
              <h2 className="text-xl font-semibold mb-2">가전제품을 선택하세요</h2>
              <p>왼쪽 사이드바에서 가전제품을 선택하면 상세 정보가 표시됩니다.</p>
            </div>
          </div>
        )}
      </main>
    </SidebarProvider>
  )
}
