import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { BarChart, DonutChart, LineChart } from '@/components/ui/chart'
import { LucideIcon } from 'lucide-react'

interface DataChartProps {
  title: string
  icon: LucideIcon
  data: Array<{ name: string; value: number }>
  type: 'line' | 'bar' | 'donut'
  color?: string
  valueFormatter: (value: number) => string
  isLoading?: boolean
}

export function DataChart({
  title,
  icon: Icon,
  data,
  type,
  color = '#2563eb',
  valueFormatter,
  isLoading = false,
}: DataChartProps) {
  if (isLoading) {
    return (
      <Card>
        <CardHeader className="pb-2">
          <div className="h-5 bg-gray-200 rounded animate-pulse w-1/3"></div>
        </CardHeader>
        <CardContent>
          <div className="h-[200px] bg-gray-200 rounded animate-pulse"></div>
        </CardContent>
      </Card>
    )
  }

  const ChartComponent = {
    line: LineChart,
    bar: BarChart,
    donut: DonutChart,
  }[type]

  return (
    <Card>
      <CardHeader className="pb-2">
        <CardTitle className="text-sm font-medium flex items-center">
          <Icon className="h-4 w-4 mr-2" />
          {title}
        </CardTitle>
      </CardHeader>
      <CardContent>
        <ChartComponent
          data={data}
          categories={['value']}
          index="name"
          colors={[color]}
          valueFormatter={valueFormatter}
          className="h-[200px]"
        />
      </CardContent>
    </Card>
  )
} 
