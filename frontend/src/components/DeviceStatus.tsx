import { Badge } from '@/components/ui/badge'
import { Card, CardContent } from '@/components/ui/card'
import { SensorItem } from '@/lib/types'
import useStore from '@/store/store'
import { useEffect, useMemo, useState } from 'react'
import Chart from 'react-apexcharts'
import { v4 as uuidv4 } from 'uuid'

const SkeletonCard = () => (
  <Card className="h-[240px]">
    <CardContent className="p-4 h-full">
      <div className="h-full bg-gray-200 rounded animate-pulse"></div>
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
  const [chartKey, setChartKey] = useState(0)

  useEffect(() => {
    setChartKey((prev) => prev + 1)
  }, [series, categories])

  if (!series || !categories || series.length === 0 || categories.length === 0) {
    return (
      <Card className="col-span-2 h-[200px]">
        <CardContent className="h-full">
          <div className="h-full flex items-center justify-center text-gray-500">데이터가 없습니다.</div>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card className="col-span-2 h-[200px] w-full">
      <CardContent className="h-full">
        <Chart
          key={chartKey}
          type="line"
          height="100%"
          series={series}
          options={{
            chart: {
              id: 'masterChart',
              type: 'line',
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
            legend: { show: true, showForSingleSeries: true },
            xaxis: { type: 'datetime', categories, labels: { datetimeUTC: false } },
            stroke: { width: 1, curve: 'smooth' },
            dataLabels: { enabled: false },
            tooltip: { x: { format: 'M월 d일 H시 mm분' } },
            yaxis: series.map((s, index) => ({
              seriesName: s.name,
              show: true,
              opposite: index % 2 === 0,
              labels: {
                formatter: (value) => {
                  if (Math.abs(value) >= 1000) {
                    return (value / 1000).toFixed(1) + 'k'
                  }
                  return value.toFixed(1)
                },
              },
            })),
          }}
        />
      </CardContent>
    </Card>
  )
}

export function DeviceStatus() {
  const sensorData = useStore((state) => state.sensorData)
  const selectedAppliance = useStore((state) => state.selectedAppliance)
  const selectedSolution = useStore((state) => state.selectedSolution)

  const isSensorDataReady = sensorData != null && sensorData.length > 0
  const selectedSensors = useMemo(
    () => sensorData?.find((sensor) => sensor.serialNumber === selectedAppliance?.serialNumber)?.sensorData || [],
    [sensorData, selectedAppliance?.serialNumber],
  )

  const sortedSensors = useMemo(() => {
    return [...selectedSensors].sort((a, b) => {
      if (selectedSolution?.result?.data?.relatedSensorEn?.includes(a.sensorName)) return -1
      if (selectedSolution?.result?.data?.relatedSensorEn?.includes(b.sensorName)) return 1
      return 0
    })
  }, [selectedSensors, selectedSolution])

  const filteredSensors = useMemo(() => {
    if (!selectedSolution?.result?.data?.relatedSensorEn) return sortedSensors
    return sortedSensors.filter((sensor) => selectedSolution.result.data.relatedSensorEn.includes(sensor.sensorName))
  }, [sortedSensors, selectedSolution])

  useEffect(() => {
    if (sensorData) {
      console.log('sensorData', sensorData)
    }
  }, [sensorData])

  return (
    <div className="lg:col-span-2 space-y-4 h-full overflow-y-auto overflow-x-hidden [&::-webkit-scrollbar]:hidden [-ms-overflow-style:none] [scrollbar-width:none]">
      <div className="sticky top-0 bg-white z-50">
        {selectedAppliance != null ? (
          <div className="mb-4">
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
        {isSensorDataReady && selectedSensors.length > 0 && (
          <BrushChart
            series={filteredSensors.map((sensor) => ({ name: sensor.title, data: sensor.data?.value || [] }))}
            categories={filteredSensors[0]?.data?.time || []}
            targets={filteredSensors.map((_, index) => `sensor-${index}`)}
          />
        )}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
        {!isSensorDataReady || selectedSensors.length === 0
          ? [...Array(6)].map((_, index) => <SkeletonCard key={index} />)
          : sortedSensors.map((sensor: SensorItem, index: number) => {
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
                <Card
                  key={uuidv4()}
                  className={`overflow-hidden p-2 h-[240px] ${selectedSolution && !selectedSolution.result?.data?.relatedSensorEn?.includes(sensor.sensorName) ? 'opacity-50' : ''}`}
                >
                  <CardContent className="p-0 h-full">
                    <div className="w-full h-full">
                      <Chart
                        type="line"
                        width="100%"
                        height="100%"
                        series={[{ name: sensor.measurement, data: sensor.data.value }]}
                        options={{
                          title: { text: sensor.title, align: 'left' },
                          chart: { id: `sensor-${index}`, zoom: { enabled: true }, animations: { enabled: false } },
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
                              ...(sensor.criteria.threshold.warning.upper != null &&
                              sensor.criteria.threshold.critical.upper != null
                                ? [
                                    {
                                      y: sensor.criteria.threshold.warning.upper,
                                      y2: sensor.criteria.threshold.critical.upper,
                                      borderColor: '#000',
                                      fillColor: '#FF9800',
                                      opacity: 0.1,
                                    },
                                    {
                                      y: sensor.criteria.threshold.critical.upper,
                                      y2: Math.max(sensor.criteria.upperLimit, Math.max(...sensor.data.value)),
                                      borderColor: '#D32F2F',
                                      fillColor: '#D32F2F',
                                      opacity: 0.1,
                                    },
                                  ]
                                : []),
                              ...(sensor.criteria.threshold.warning.lower != null &&
                              sensor.criteria.threshold.critical.lower != null
                                ? [
                                    {
                                      y: sensor.criteria.threshold.critical.lower,
                                      y2: sensor.criteria.threshold.warning.lower,
                                      borderColor: '#000',
                                      fillColor: '#FF9800',
                                      opacity: 0.1,
                                    },
                                    {
                                      y: Math.min(sensor.criteria.lowerLimit, Math.min(...sensor.data.value)),
                                      y2: sensor.criteria.threshold.critical.lower,
                                      borderColor: '#D32F2F',
                                      fillColor: '#D32F2F',
                                      opacity: 0.1,
                                    },
                                  ]
                                : []),
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
