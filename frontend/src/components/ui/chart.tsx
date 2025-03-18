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
  colors = ['#2563eb'],
  valueFormatter = (value: number) => `${value}`,
  className,
}: ChartProps) {
  return (
    <div className={className}>
      <ResponsiveContainer width="100%" height="100%">
        <RechartsLineChart data={data} margin={{ top: 5, right: 5, left: 5, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey={index} />
          <YAxis />
          <Tooltip formatter={(value: number) => [valueFormatter(value), '']} labelFormatter={(label) => `${label}`} />
          {categories.map((category, i) => (
            <Line
              key={category}
              type="monotone"
              dataKey={category}
              stroke={colors[i % colors.length]}
              strokeWidth={2}
              dot={{ stroke: colors[i % colors.length], strokeWidth: 2, fill: colors[i % colors.length] }}
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
        <RechartsBarChart data={data} margin={{ top: 5, right: 5, left: 5, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey={index} />
          <YAxis />
          <Tooltip formatter={(value: number) => [valueFormatter(value), '']} labelFormatter={(label) => `${label}`} />
          {categories.map((category, i) => (
            <Bar key={category} dataKey={category} fill={colors[i % colors.length]} barSize={20} />
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
  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8', '#82ca9d']
  const RADIAN = Math.PI / 180

  const renderCustomizedLabel = ({ cx, cy, midAngle, innerRadius, outerRadius, percent }: any) => {
    const radius = innerRadius + (outerRadius - innerRadius) * 0.5
    const x = cx + radius * Math.cos(-midAngle * RADIAN)
    const y = cy + radius * Math.sin(-midAngle * RADIAN)

    return (
      <text x={x} y={y} fill="white" textAnchor={x > cx ? 'start' : 'end'} dominantBaseline="central">
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
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Pie>
          <Tooltip formatter={(value: number) => [valueFormatter(value), '']} labelFormatter={(label) => `${label}`} />
        </RechartsPieChart>
      </ResponsiveContainer>
    </div>
  )
}
