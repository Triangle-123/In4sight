import { Card, CardContent } from '@/components/ui/card'
import useStore from '@/store/store'
import { BarChart3, Clock, Gauge, Power, Thermometer } from 'lucide-react'

import { StatusBadge } from './StatusBadge'
import { DataChart } from './charts/DataChart'

// 스켈레톤 컴포넌트들
const SkeletonCard = () => (
  <Card>
    <CardContent className="p-4">
      <div className="h-4 bg-gray-200 rounded animate-pulse w-1/2 mb-2" />
      <div className="h-8 bg-gray-200 rounded animate-pulse w-1/3" />
    </CardContent>
  </Card>
)

export function DeviceStatus() {
  const sensorData = useStore((state) => state.sensorData)
  // TODO: store 사용하여 sensorData 받아오기, props 삭제하기 (isLoading 삭제)
  if (!sensorData) {
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
            <DataChart
              key={index}
              title="로딩 중..."
              icon={Thermometer}
              data={[]}
              type="line"
              valueFormatter={() => ''}
              isLoading={true}
            />
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
          ? applianceData.metrics.map((metric, index) => (
              <Card key={index}>
                <CardContent className="p-4">
                  <p className="text-sm font-medium">{metric.name}</p>
                  <p className={`text-2xl font-bold`}>{metric.value}</p>
                </CardContent>
              </Card>
            ))
          : Array(4)
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
        {applianceData.temperatureData && (
          <DataChart
            title="온도 변화"
            icon={Thermometer}
            data={applianceData.temperatureData}
            type="line"
            color="#2563eb"
            valueFormatter={(value) => `${value}°C`}
          />
        )}

        {applianceData.powerData && (
          <DataChart
            title="전력 소비"
            icon={Power}
            data={applianceData.powerData}
            type="line"
            color="#10b981"
            valueFormatter={(value) => `${value}W`}
          />
        )}

        {applianceData.usageData && (
          <DataChart
            title="사용 분석"
            icon={BarChart3}
            data={applianceData.usageData}
            type="donut"
            valueFormatter={(value) => `${value}%`}
          />
        )}

        {applianceData.cycleData && (
          <DataChart
            title="사이클 사용"
            icon={Clock}
            data={applianceData.cycleData}
            type="bar"
            color="#8b5cf6"
            valueFormatter={(value) => `${value}회`}
          />
        )}

        {applianceData.waterUsageData && (
          <DataChart
            title="물 사용량"
            icon={Gauge}
            data={applianceData.waterUsageData}
            type="bar"
            color="#0ea5e9"
            valueFormatter={(value) => `${value}L`}
          />
        )}
      </div>
    </div>
  )
}
