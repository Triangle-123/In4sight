import { Card, CardContent } from '@/components/ui/card'
// import { sensorDataPlaceholder } from '@/lib/placeholder-data'
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
  // const setSensorData = useStore((state) => state.setSensorData)

  // setSensorData(sensorDataPlaceholder)

  useEffect(() => {
    if (sensorData) {
      console.log('sensorData', sensorData)
    }
  }, [sensorData])

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
              icon="Thermometer"
              data={[]}
              type="line"
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
        {/* <StatusBadge status={applianceData.status} /> */}
      </div>

      {/* <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
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
      </div> */}

      <div className="grid grid-cols-1 md:grid-cols-3 gap-2">
        {sensorData.sensorData.map((sensor: Sensor) => (
          <DataChart
            key={uuidv4()}
            title={sensor.title}
            icon={sensor.icon}
            data={sensor.data}
            type="line"
            isNormal={sensor.normal}
            valueFormatter={(value) => `${value}${sensor.unit}`}
          />
        ))}
      </div>
    </div>
  )
}
