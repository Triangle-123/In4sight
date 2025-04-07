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

export interface ApplianceFailureData {
  // 복수형 변수명은 array를 의미함
  results: {
    taskId: string
    metadata: {
      userInfo: {
        // 과거 상담 이력
        pastSupportRecords: {
          cause: string
          date: string
          issue: string
          resolved: boolean
        }[]
      }
      appliance: {
        type: string // 제품 타입: REF(냉장고), WM(세탁기), AC(에어컨)
        serialNumber: string // 제품 시리얼 번호
      }
    }
    data: {
      symptom: string // 증상; 구 failure
      causes: string[] // 원인들
      sensors: string[] // 관련 센서들
      solutions: {
        severity: string // 심각도
        personalizedContext: string // <- 이 친구의 역할을 잘 모르겠달까...
        solution: string
      }[]
      supportGuides: string[] // 지원 가이드
    }
  }[]
}

export interface SensorDataPoint {
  time: string
  value: number
}

export interface SensorItem {
  title: string
  measurement: string
  icon: string
  unit: string
  criteria: {
    lowerLimit: number
    upperLimit: number
    threshold: {
      warning: number
      critical: number
    }
  }
  sensorName: string
  data: {
    time: string[]
    value: number[]
  }
}

export interface SensorData {
  serialNumber: string
  sensorData: SensorItem[]
}

export interface SolutionItem {
  result: {
    serialNumber: string;
    data: {
      failure: string;
      cause: string[];
      sensor: string[];
      relatedSensorEn: string[];
      solutions: {
        historicalContext: {
          previousIssues: any[];
        };
        personalizedSolution: {
          personalizedContext: string;
          recommendedSolution: string;
          status: string;
        }[];
        preventativeAdvice: string[];
      };
    };
  };
}
