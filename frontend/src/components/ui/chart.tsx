'use client'

import {
  Bar,
  CartesianGrid,
  Cell,
  Line,
  Pie,
  BarChart as RechartsBarChart,
  LineChart as RechartsLineChart,
  PieChart as RechartsPieChart,
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
              return date
                .toLocaleString('ko-KR', {
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

export function BarChart({
  data,
  categories = ['value'],
  index,
  colors = ['#2563eb'],
  valueFormatter = (value: number) => `${value}`,
  className,
}: ChartProps) {
  return (
    <div className={className}>
      <ResponsiveContainer width="100%" height="100%">
        <RechartsBarChart
          data={data}
          margin={{ top: 5, right: 5, left: 5, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey={index} />
          <YAxis />
          <Tooltip
            formatter={(value: number) => [valueFormatter(value), '']}
            labelFormatter={(label) => `${label}`}
          />
          {categories.map((category, i) => (
            <Bar
              key={category}
              dataKey={category}
              fill={colors[i % colors.length]}
              barSize={20}
            />
          ))}
        </RechartsBarChart>
      </ResponsiveContainer>
    </div>
  )
}

export function DonutChart({
  data,
  category = 'value',
  index,
  valueFormatter = (value: number) => `${value}`,
  className,
}: ChartProps) {
  const COLORS = [
    '#0088FE',
    '#00C49F',
    '#FFBB28',
    '#FF8042',
    '#8884d8',
    '#82ca9d',
  ]
  const RADIAN = Math.PI / 180

  const renderCustomizedLabel = ({
    cx,
    cy,
    midAngle,
    innerRadius,
    outerRadius,
    percent,
  }: any) => {
    const radius = innerRadius + (outerRadius - innerRadius) * 0.5
    const x = cx + radius * Math.cos(-midAngle * RADIAN)
    const y = cy + radius * Math.sin(-midAngle * RADIAN)

    return (
      <text
        x={x}
        y={y}
        fill="white"
        textAnchor={x > cx ? 'start' : 'end'}
        dominantBaseline="central"
      >
        {`${(percent * 100).toFixed(0)}%`}
      </text>
    )
  }

  return (
    <div className={className}>
      <ResponsiveContainer width="100%" height="100%">
        <RechartsPieChart margin={{ top: 5, right: 5, left: 5, bottom: 5 }}>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            labelLine={false}
            label={renderCustomizedLabel}
            outerRadius={80}
            innerRadius={40}
            fill="#8884d8"
            dataKey={category}
          >
            {data.map((entry, index) => (
              <Cell
                key={`cell-${index}`}
                fill={COLORS[index % COLORS.length]}
              />
            ))}
          </Pie>
          <Tooltip
            formatter={(value: number) => [valueFormatter(value), '']}
            labelFormatter={(label) => `${label}`}
          />
        </RechartsPieChart>
      </ResponsiveContainer>
    </div>
  )
}
