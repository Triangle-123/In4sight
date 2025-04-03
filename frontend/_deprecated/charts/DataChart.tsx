import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { LineChart } from '@/components/ui/chart'
import * as Icons from 'lucide-react'
import { LucideIcon } from 'lucide-react'

interface DataChartProps {
  title: string
  icon: string
  data: Array<{ time: string; value: number }>
  isNormal: boolean
  valueFormatter: (value: number) => string
  isLoading?: boolean
}

export function DataChart({
  title,
  icon,
  data,
  isNormal,
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

  const Icon = (Icons as unknown as Record<string, LucideIcon>)[icon]

  return (
    <Card>
      <CardHeader className="pb-2">
        <CardTitle className="text-sm font-medium flex items-center">
          <Icon className="h-4 w-4 mr-2" />
          {title}
        </CardTitle>
      </CardHeader>
      <CardContent>
        <LineChart
          data={data}
          categories={['value']}
          index="time"
          colors={[isNormal ? '#4caf50' : '#e53935']}
          valueFormatter={valueFormatter}
          className="h-[200px]"
        />
      </CardContent>
    </Card>
  )
}
