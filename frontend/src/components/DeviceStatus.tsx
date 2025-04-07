import { Card, CardContent } from '@/components/ui/card'
import { SensorItem } from '@/lib/types'
import useStore from '@/store/store'
import { useEffect, useState } from 'react'
import Chart from 'react-apexcharts'
import { v4 as uuidv4 } from 'uuid'
import { Badge } from '@/components/ui/badge'

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
  categories: string[]
  targets: string[]
}) => {
  const [chartKey, setChartKey] = useState(0);

  useEffect(() => {
    setChartKey(prev => prev + 1);
  }, [series, categories]);

  if (!series || !categories || series.length === 0 || categories.length === 0) {
    return (
      <Card className="col-span-2">
        <CardContent>
          <div className="h-[150px] flex items-center justify-center text-gray-500">데이터가 없습니다.</div>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card className="col-span-2">
      <CardContent>
        <Chart
          key={chartKey}
          type="area"
          height={150}
          series={series}
          options={{
            chart: {
              id: 'masterChart',
              type: 'area',
              height: 150,
              brush: { enabled: true, targets, autoScaleYaxis: true },
              selection: {
                enabled: true,
                xaxis: { min: undefined, max: undefined },
                fill: { color: '#ccc', opacity: 0.2 },
                stroke: { color: '#888' },
              },
              animations: { enabled: false },
            },
            xaxis: { type: 'datetime', categories: categories, labels: { datetimeUTC: false } },
            stroke: { width: 2, curve: 'smooth' },
            dataLabels: { enabled: false },
            tooltip: { x: { format: 'M월 d일 H시 mm분' } },
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
    <div className="lg:col-span-2 space-y-4 h-full overflow-y-auto overflow-x-hidden [&::-webkit-scrollbar]:hidden [-ms-overflow-style:none] [scrollbar-width:none]">
      <div className="flex items-center sticky top-0 bg-white z-10">
        {selectedAppliance != null ? (
          <div>
            <h2 className="text-xl font-semibold mb-1">{selectedAppliance.modelName}</h2>
            <p className="text-sm flex items-center gap-2">
              <Badge className="bg-gray-200 text-black">모델명: {selectedAppliance.modelSuffix}</Badge>
              <Badge className="bg-gray-200 text-black">S/N: {selectedAppliance.serialNumber}</Badge>
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
        {isSensorDataReady && selectedSensors.length > 0 && (
          <BrushChart
            series={selectedSensors.map((sensor) => ({ name: sensor.title, data: sensor.data?.value || [] }))}
            categories={selectedSensors[0]?.data?.time || []}
            targets={selectedSensors.map((_, index) => `sensor-${index}`)}
          />
        )}
        {!isSensorDataReady || selectedSensors.length === 0
          ? [...Array(6)].map((_, index) => <SkeletonCard key={index} />)
          : selectedSensors.map((sensor: SensorItem, index: number) => {
              if (!sensor.data?.time || !sensor.data?.value) {
                return (
                  <Card key={uuidv4()} className="overflow-hidden p-2">
                    <CardContent className="p-0">
                      <div className="w-full h-[240px] flex items-center justify-center text-gray-500">
                        데이터가 없습니다.
                      </div>
                    </CardContent>
                  </Card>
                )
              }
              return (
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
                          chart: {
                            id: `sensor-${index}`,
                            zoom: { enabled: true },
                            // brush: {
                            //   enabled: true,
                            //   target: 'masterChart',
                            //   autoScaleYaxis: true
                            // },
                            animations: { enabled: false },
                          },
                          colors: ['#4B5563'],
                          dataLabels: { enabled: false },
                          stroke: { width: 2, curve: 'monotoneCubic' },
                          xaxis: { type: 'datetime', categories: sensor.data.time },
                          yaxis: {
                            title: { text: `${sensor.measurement} (${sensor.unit})` },
                            min: Math.min(sensor.criteria.lowerLimit, Math.min(...sensor.data.value)),
                            max: Math.max(sensor.criteria.upperLimit, Math.max(...sensor.data.value)),
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
              )
            })}
      </div>
    </div>
  )
}
