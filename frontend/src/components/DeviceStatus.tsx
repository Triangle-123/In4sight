import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { BarChart, DonutChart, LineChart } from '@/components/ui/chart'
import type { ApplianceDataType } from '@/lib/types'
import { BarChart3, Clock, Gauge, Power, Thermometer } from 'lucide-react'
import { Area, AreaChart, CartesianGrid, XAxis } from 'recharts'

import { StatusBadge } from './StatusBadge'

interface DeviceStatusProps {
  applianceData?: ApplianceDataType
  isLoading?: boolean
}

// 스켈레톤 컴포넌트들
const SkeletonLine = () => <div className="h-4 bg-gray-200 rounded animate-pulse w-full" />

const SkeletonCard = () => (
  <Card>
    <CardContent className="p-4">
      <div className="h-4 bg-gray-200 rounded animate-pulse w-1/2 mb-2" />
      <div className="h-8 bg-gray-200 rounded animate-pulse w-1/3" />
    </CardContent>
  </Card>
)

const SkeletonChart = () => (
  <Card>
    <CardHeader className="pb-2">
      <div className="flex items-center">
        <div className="h-4 w-4 bg-gray-200 rounded animate-pulse mr-2" />
        <div className="h-4 bg-gray-200 rounded animate-pulse w-1/3" />
      </div>
    </CardHeader>
    <CardContent>
      <div className="h-[200px] bg-gray-200 rounded animate-pulse w-full" />
    </CardContent>
  </Card>
)

export function DeviceStatus({ applianceData, isLoading = false }: DeviceStatusProps) {
  if (isLoading || !applianceData) {
    return (
      <div className="lg:col-span-2 space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <div className="h-6 bg-gray-200 rounded animate-pulse w-48 mb-2" />
            <div className="h-4 bg-gray-200 rounded animate-pulse w-32" />
          </div>
          <div className="h-6 w-20 bg-gray-200 rounded-full animate-pulse" />
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[...Array(4)].map((_, index) => (
            <SkeletonCard key={index} />
          ))}
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {[...Array(4)].map((_, index) => (
            <SkeletonChart key={index} />
          ))}
        </div>
      </div>
    )
  }

  return (
    <div className="lg:col-span-2 space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-semibold">{applianceData.name}</h2>
          <p className="text-sm text-muted-foreground">{applianceData.model}</p>
        </div>
        <StatusBadge status={applianceData.status} />
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {applianceData.metrics
          ? // metrics가 있으면 실제 데이터 표시
            applianceData.metrics.map((metric, index) => (
              <Card key={index}>
                <CardContent className="p-4">
                  <p className="text-sm font-medium">{metric.name}</p>
                  <p className={`text-2xl font-bold`}>{metric.value}</p>
                </CardContent>
              </Card>
            ))
          : // metrics가 null이면 스켈레톤 UI 표시
            // 4개의 스켈레톤 카드 생성 (md:grid-cols-4에 맞춰서)
            Array(4)
              .fill(0)
              .map((_, index) => (
                <Card key={index}>
                  <CardContent className="p-4">
                    <div className="h-4 bg-gray-200 rounded animate-pulse mb-2"></div>
                    <div className="h-8 bg-gray-200 rounded animate-pulse w-2/3"></div>
                  </CardContent>
                </Card>
              ))}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {applianceData.temperatureData ? (
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium flex items-center">
                <Thermometer className="h-4 w-4 mr-2" />
                온도 변화
              </CardTitle>
            </CardHeader>
            <CardContent>
              <LineChart
                data={applianceData.temperatureData}
                categories={['value']}
                index="name"
                colors={['#2563eb']}
                valueFormatter={(value: number) => `${value}°C`}
                className="h-[200px]"
              />
            </CardContent>
          </Card>
        ) : (
          <Card>
            <CardHeader className="pb-2">
              <div className="h-5 bg-gray-200 rounded animate-pulse w-1/3"></div>
            </CardHeader>
            <CardContent>
              <div className="h-[200px] bg-gray-200 rounded animate-pulse"></div>
            </CardContent>
          </Card>
        )}

        {applianceData.powerData && (
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium flex items-center">
                <Power className="h-4 w-4 mr-2" />
                전력 소비
              </CardTitle>
            </CardHeader>
            <CardContent>
              <LineChart
                data={applianceData.powerData}
                categories={['value']}
                index="name"
                colors={['#10b981']}
                valueFormatter={(value: number) => `${value}W`}
                className="h-[200px]"
              />
            </CardContent>
          </Card>
        )}

        {applianceData.usageData && (
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium flex items-center">
                <BarChart3 className="h-4 w-4 mr-2" />
                사용 분석
              </CardTitle>
            </CardHeader>
            <CardContent>
              <DonutChart
                data={applianceData.usageData}
                categories={['value']}
                index="name"
                valueFormatter={(value: number) => `${value}%`}
                className="h-[200px]"
              />
            </CardContent>
          </Card>
        )}

        {applianceData.cycleData && (
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium flex items-center">
                <Clock className="h-4 w-4 mr-2" />
                사이클 사용
              </CardTitle>
            </CardHeader>
            <CardContent>
              <BarChart
                data={applianceData.cycleData}
                categories={['value']}
                index="name"
                colors={['#8b5cf6']}
                valueFormatter={(value: number) => `${value}회`}
                className="h-[200px]"
              />
            </CardContent>
          </Card>
        )}

        {applianceData.waterUsageData && (
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium flex items-center">
                <Gauge className="h-4 w-4 mr-2" />물 사용량
              </CardTitle>
            </CardHeader>
            <CardContent>
              <BarChart
                data={applianceData.waterUsageData}
                categories={['value']}
                index="name"
                colors={['#0ea5e9']}
                valueFormatter={(value: number) => `${value}L`}
                className="h-[200px]"
              />
            </CardContent>
          </Card>
        )}
      </div>
    </div>
  )
}
