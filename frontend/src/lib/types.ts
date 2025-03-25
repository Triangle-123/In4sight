export interface ApplianceType {
  serialNumber: string
  productType: string
  modelSuffix: string

  modelName: string
  status: string
  launchDate: string
}

export interface CustomerType {
  customerId: number
  customerName: string
  phoneNumber: string
  address: string
}

export interface MetricType {
  name: string
  value: string
  status: string
}

export interface RecommendationType {
  title: string
  summary: string
  description: string
  status: string
}

export interface ChartDataPoint {
  name: string
  value: number
}

export interface ApplianceDataType {
  name: string
  model: string
  status: string
  metrics: MetricType[]
  recommendations: RecommendationType[]
  temperatureData?: ChartDataPoint[]
  powerData?: ChartDataPoint[]
  usageData?: ChartDataPoint[]
  cycleData?: ChartDataPoint[]
  waterUsageData?: ChartDataPoint[]
  efficiencyData?: ChartDataPoint[]
  appUsageData?: ChartDataPoint[]
}
