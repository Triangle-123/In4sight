import { Card, CardContent } from '@/components/ui/card'
import { SensorData, SensorItem } from '@/lib/types'
import useStore from '@/store/store'
import { useEffect } from 'react'
import Chart from 'react-apexcharts'
import { v4 as uuidv4 } from 'uuid'

const SkeletonCard = () => (
  <Card>
    <CardContent className="p-4">
      <div className="h-[240px] bg-gray-200 rounded animate-pulse"></div>
    </CardContent>
  </Card>
)

const BrushChart = ({
  series,
  targets,
  categories,
}: {
  series: { name: string; data: number[] }[]
  targets: string[]
  categories: string[]
}) => {
  return (
    <Card className="col-span-2">
      <CardContent>
        <Chart
          type="area"
          height={150}
          series={series}
          options={{
            chart: {
              id: 'masterChart',
              type: 'area',
              height: 150,
              brush: { enabled: true, targets: targets },
              selection: { enabled: true, fill: { color: '#ccc', opacity: 0.2 }, stroke: { color: '#888' } },
            },
            xaxis: {
              type: 'datetime',
              categories: categories, // datetime 데이터 배열
            },
            stroke: { width: 2 },
            dataLabels: { enabled: false },
          }}
        />
      </CardContent>
    </Card>
  )
}

export function DeviceStatus() {
  const sensorData = useStore((state) => state.sensorData)
  const selectedAppliance = useStore((state) => state.selectedAppliance)

  const isSensorDataReady = sensorData != null && sensorData.length > 0
  const selectedSensors =
    sensorData?.find((sensor) => sensor.serialNumber === selectedAppliance?.serialNumber)?.sensorData || []

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
            <h2 className="text-xl font-semibold">{selectedAppliance.modelName}</h2>
            <p className="text-sm text-muted-foreground">{selectedAppliance.modelSuffix}</p>
          </div>
        ) : (
          <>
            <div className="h-6 bg-gray-200 rounded animate-pulse w-48 mb-2" />
            <div className="h-4 bg-gray-200 rounded animate-pulse w-32" />
          </>
        )}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
        {/* TODO: 모든 그래프를 제어할 수 있는 Brush chart 추가 */}
        {isSensorDataReady && (
          <BrushChart
            series={selectedSensors.map((sensor) => ({ name: sensor.title, data: sensor.data.value }))}
            targets={selectedSensors.map((_, index) => `sensor-${index}`)}
            categories={selectedSensors[0].data.time}
          />
        )}
        {!isSensorDataReady
          ? [...Array(6)].map((_, index) => <SkeletonCard key={index} />)
          : selectedSensors.map((sensor: SensorItem, index: number) => (
              <Card key={uuidv4()} className="overflow-hidden p-2">
                <CardContent className="p-0">
                  <div className="w-full h-[240px]">
                    <Chart
                      type="line"
                      width="100%"
                      height="100%"
                      series={[{ name: sensor.measurement, data: sensor.data.value }]}
                      options={{
                        title: { text: sensor.title, align: 'left' },
                        chart: { id: `sensor-${index}`, zoom: { enabled: true } },
                        colors: ['#4B5563'],
                        dataLabels: { enabled: false },
                        stroke: { width: 2, curve: 'monotoneCubic' },
                        xaxis: { type: 'datetime', categories: sensor.data.time },
                        yaxis: {
                          title: { text: `${sensor.measurement} (${sensor.unit})` },
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
                                  padding: { left: 5, right: 5, top: 2, bottom: 2 },
                                },
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
                                  padding: { left: 5, right: 5, top: 2, bottom: 2 },
                                },
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
