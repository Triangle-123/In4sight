'use client'

import {
  CartesianGrid,
  Line,
  LineChart as RechartsLineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'

interface ChartProps {
  data: any[]
  categories?: string[]
  index: string
  colors?: string[]
  valueFormatter?: (value: number) => string
  className?: string
}

export function LineChart({
  data,
  categories = ['value'],
  index,
  colors,
  valueFormatter = (value: number) => `${value}`,
  className,
}: ChartProps) {
  return (
    <div className={className}>
      <ResponsiveContainer width="100%" height="100%">
        <RechartsLineChart
          data={data}
          margin={{ top: 5, right: 10, left: 0, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="1 1" vertical={false} />
          <XAxis
            dataKey={index}
            tickFormatter={(value) => {
              const date = new Date(value)
              const hours = date.getHours()
              // 정시(0시)일 때만 MM/DD 표시
              if (hours === 0) {
                return `${date.getMonth() + 1}/${date.getDate()}`
              }
              // 그 외에는 시간만 표시
              return `${hours}시`
            }}
          />
          <YAxis
            tickCount={3}
            type="number"
            domain={([dataMin, dataMax]) => {
              const range = Math.abs(dataMax - dataMin)
              let min, max

              if (range < 1) {
                // range가 1 미만일 때 소수점 1자리까지 표시
                min = Number((dataMin - range * 0.2).toFixed(1))
                max = Number((dataMax + range * 0.2).toFixed(1))
              } else {
                min = Math.floor(dataMin - range * 0.2)
                max = Math.ceil(dataMax + range * 0.2)
              }

              return [min, max]
            }}
          />
          <Tooltip
            formatter={(value: number) => [valueFormatter(value), '']}
            labelFormatter={(label) => {
              const date = new Date(label)
              return date.toLocaleString('ko-KR', {
                year: '2-digit',
                month: 'long',
                day: 'numeric',
                hour: 'numeric',
                minute: 'numeric',
                hour12: false,
              })
            }}
          />
          {categories.map((category, i) => (
            <Line
              key={category}
              type="monotone"
              dataKey={category}
              stroke={colors![i % colors!.length]}
              strokeWidth={2}
              dot={false}
              activeDot={{ r: 6 }}
            />
          ))}
        </RechartsLineChart>
      </ResponsiveContainer>
    </div>
  )
}
