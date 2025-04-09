import DashboardSidebar from '@/components/DashboardSidebar'
import { DeviceStatus } from '@/components/DeviceStatus'
import { Recommendations } from '@/components/Recommendations'
import { Separator } from '@/components/ui/separator'
import { SidebarProvider, SidebarTrigger } from '@/components/ui/sidebar'
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card'
import useStore from '@/store/store'
import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { ApplianceType } from '@/lib/types'

export default function Dashboard() {
  const createSseConnection = useStore((state) => state.createSseConnection)
  const isConnected = useStore((state) => state.isConnected)
  const appliances = useStore((state) => state.appliances)
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

  const getGridColsClass = (count: number): string => {
    if (count <= 0) return 'grid-cols-1';
    if (count <= 4) return 'grid-cols-2';
    if (count <= 6) return 'grid-cols-3';
    return 'grid-cols-4';
  };

  const gridColsClass = getGridColsClass(appliances?.length || 0);

  return (
    <SidebarProvider 
      className="h-screen"
      style={{ "--sidebar-width": "22rem" } as React.CSSProperties}
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
          <div className={`h-[95vh] grid ${gridColsClass} gap-4 p-4 overflow-y-auto`}>
             {appliances && appliances.length > 0 ? (
               appliances.map((appliance: ApplianceType) => (
                 <Card key={appliance.serialNumber} className="flex flex-col cursor-pointer hover:shadow-lg transition-shadow" onClick={() => console.log(appliance.serialNumber)}>
                   <CardHeader>
                     <CardTitle className="text-base">{appliance.modelInfo.modelName}</CardTitle>
                   </CardHeader>
                   <CardContent className="flex-grow flex flex-col items-center justify-center text-center">
                     <img
                       src={appliance.modelInfo.modelImage}
                       alt={appliance.modelInfo.modelName}
                       className="max-h-32 w-auto object-contain mb-3"
                     />
                     <p className="text-xs text-muted-foreground mt-auto pt-2">
                       구매일: {new Date(appliance.modelInfo.purchaseDate).toLocaleDateString()}
                     </p>
                   </CardContent>
                 </Card>
               ))
             ) : (
                <div className="col-span-full h-full flex items-center justify-center">
                    <div className="text-center">
                    <h2 className="text-xl font-semibold mb-2">표시할 가전제품이 없습니다.</h2>
                    <p>데이터를 로드 중이거나 등록된 가전제품이 없습니다.</p>
                    </div>
                </div>
             )}
          </div>
        )}
      </main>
    </SidebarProvider>
  )
}
