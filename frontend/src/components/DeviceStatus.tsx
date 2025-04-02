import { Card, CardContent } from '@/components/ui/card'
import { sensorDataPlaceholder } from '@/lib/placeholder-data'
import useStore from '@/store/store'
import { useEffect } from 'react'
import { v4 as uuidv4 } from 'uuid'

// import { StatusBadge } from './StatusBadge'
import { DataChart } from './charts/DataChart'

interface Sensor {
  title: string
  icon: string
  unit: string
  normal: boolean
  data: Array<{ time: string; value: number }>
}

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
  const selectedAppliance = useStore((state) => state.selectedAppliance)
  const setSensorData = useStore((state) => state.setSensorData)

  // setSensorData(sensorDataPlaceholder)

  useEffect(() => {
    if (sensorData) {
      console.log('sensorData', sensorData)
    }
  }, [sensorData])

  if (sensorData === undefined || Object.keys(sensorData).length === 0 || !sensorData.sensorData) {
    return (
      <div className="lg:col-span-2 space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <div className="h-6 bg-gray-200 rounded animate-pulse w-48 mb-2" />
            <div className="h-4 bg-gray-200 rounded animate-pulse w-32" />
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-2">
          {[...Array(6)].map((_, index) => (
            <DataChart
              key={index}
              title="로딩 중..."
              icon="Thermometer"
              data={[]}
              isNormal={false}
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
          <h2 className="text-xl font-semibold">
            {selectedAppliance?.modelName}
          </h2>
          <p className="text-sm text-muted-foreground">
            {selectedAppliance?.modelSuffix}
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-2">
        {sensorData.sensorData && sensorData.sensorData.map((sensor: Sensor) => (
          <DataChart
            key={uuidv4()}
            title={sensor.title}
            icon={sensor.icon}
            data={sensor.data}
            isNormal={sensor.normal}
            valueFormatter={(value) => `${value}${sensor.unit}`}
          />
        ))}
      </div>
    </div>
  )
}
