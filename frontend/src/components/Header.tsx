'use client'

import { useEffect, useState } from 'react'

export function Header() {
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

  return (
    <header className="min-h-14 border-b flex items-center justify-between px-4">
      <div className="flex items-center">
        {/* <Button variant="ghost" size="icon" onClick={() => setSidebarOpen(!sidebarOpen)} className="mr-2">
          {sidebarOpen ? <ChevronLeft className="h-4 w-4" /> : <ChevronRight className="h-4 w-4" />}
        </Button> */}
        <h1 className="font-semibold text-lg">고객 지원 대시보드</h1>
      </div>
      <div className="flex items-center gap-4">
        <div className="text-sm text-muted-foreground">
          <span className="mr-4">상담사: 김민서 (서울 센터)</span>
          <span>IP: {ip}</span>
        </div>
      </div>
    </header>
  )
}
