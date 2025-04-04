import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
// import { sensorDataPlaceholder } from '@/lib/placeholder-data'
import { SensorItem } from '@/lib/types'
import useStore from '@/store/store'
// import { StatusBadge } from './StatusBadge'
// import * as LucideIcons from 'lucide-react'
// import { LucideIcon } from 'lucide-react'
import { useEffect } from 'react'
import Chart from 'react-apexcharts'
import { v4 as uuidv4 } from 'uuid'

// 스켈레톤 컴포넌트
const SkeletonCard = () => (
  <Card>
    {/* <CardHeader className="pb-2">
      <div className="h-5 bg-gray-200 rounded animate-pulse w-1/3"></div>
    </CardHeader> */}
    <CardContent>
      <div className="h-[200px] bg-gray-200 rounded animate-pulse"></div>
    </CardContent>
  </Card>
)

export function DeviceStatus() {
  const sensorData = useStore((state) => state.sensorData)
  const selectedAppliance = useStore((state) => state.selectedAppliance)
  // const setSensorData = useStore((state) => state.setSensorData)

  // setSensorData(sensorDataPlaceholder)

  const isSensorDataReady =
    sensorData != null &&
    Object.keys(sensorData).length > 0 &&
    sensorData.sensorData != null

  useEffect(() => {
    if (sensorData) {
      console.log('sensorData', sensorData)
    }
  }, [sensorData])

  return (
    <div className="lg:col-span-2 space-y-4 h-full overflow-y-auto overflow-x-hidden">
      <div className="flex items-center justify-between sticky top-0 bg-white z-10 pb-4">
        {selectedAppliance != null ? (
          <div>
            <h2 className="text-xl font-semibold">
              {selectedAppliance.modelName}
            </h2>
            <p className="text-sm text-muted-foreground">
              {selectedAppliance.modelSuffix}
            </p>
          </div>
        ) : (
          <>
            <div className="h-6 bg-gray-200 rounded animate-pulse w-48 mb-2" />
            <div className="h-4 bg-gray-200 rounded animate-pulse w-32" />
          </>
        )}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
        {!isSensorDataReady
          ? [...Array(6)].map((_, index) => <SkeletonCard key={index} />)
          : sensorData.sensorData.map((sensor: SensorItem) => (
              <Card key={uuidv4()} className="overflow-hidden p-2">
                <CardContent className="p-0">
                  <div className="w-full h-[200px]">
                    <Chart
                      type="line"
                      width="100%"
                      height="100%"
                      series={[
                        { name: sensor.measurement, data: sensor.data.value },
                      ]}
                      options={{
                        title: { text: sensor.title, align: 'left' },
                        chart: { zoom: { enabled: true } },
                        colors: ['#4B5563'],
                        dataLabels: { enabled: false },
                        stroke: { width: 2, curve: 'monotoneCubic' },
                        xaxis: {
                          type: 'datetime',
                          categories: sensor.data.time,
                        },
                        yaxis: {
                          title: {
                            text: `${sensor.measurement} (${sensor.unit})`,
                          },
                          min: sensor.criteria.lowerLimit,
                          max: sensor.criteria.upperLimit,
                        },
                        annotations: {
                          yaxis: [
                            {
                              y: sensor.criteria.threshold.warning,
                              y2: sensor.criteria.threshold.critical,
                              borderColor: '#000',
                              fillColor: '#FF9800',
                              opacity: 0.1,
                              label: {
                                text: '주의',
                                position: 'right',
                                style: {
                                  color: '#FF9800',
                                  background: '#fff',
                                  
                                  padding: {
                                    left: 5,
                                    right: 5,
                                    top: 2,
                                    bottom: 2
                                  }
                                }
                              },
                            },
                            {
                              y: sensor.criteria.threshold.critical,
                              y2: sensor.criteria.upperLimit,
                              borderColor: '#D32F2F',
                              fillColor: '#D32F2F',
                              opacity: 0.1,
                              label: {
                                text: '위험',
                                position: 'right',
                                style: {
                                  color: '#D32F2F',
                                  background: '#fff',
                                  padding: {
                                    left: 5,
                                    right: 5,
                                    top: 2,
                                    bottom: 2
                                  }
                                }
                              },
                            },
                          ],
                        },
                        tooltip: {
                          x: { format: 'M월 d일 H시 mm분' },
                          y: { formatter: (value) => `${value} ${sensor.unit}` },
                        },
                      }}
                    />
                  </div>
                </CardContent>
              </Card>
            ))}
      </div>
    </div>
  )
}
