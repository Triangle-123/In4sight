/* 예시 데이터 */
import type { ApplianceDataType } from './types'
import type { ApplianceType } from './types'

export function getAppliancePlaceholder(selectedAppliance: ApplianceType): ApplianceDataType | null {
  // 냉장고
  if (selectedAppliance?.productType === 'REF') {
    return {
      name: '냉장고',
      model: selectedAppliance.modelName,
      status: 'normal',
      metrics: [
        { name: '온도', value: '3°C', status: 'normal' },
        { name: '습도', value: '42%', status: 'normal' },
        { name: '전력 소비', value: '120W', status: 'normal' },
        { name: '도어 열림', value: '8회/일', status: 'normal' },
      ],
      recommendations: [
        {
          title: '정기 점검 안내',
          summary: '정기 점검 시점이 다가오고 있습니다.',
          description: '다음 정기 점검은 30일 후 예정되어 있습니다.',
          status: 'normal',
        },
        {
          title: '필터 교체 안내',
          summary: '정기 점검 시점이 다가오고 있습니다.',
          description: '정수 필터 교체까지 45일 남았습니다.',
          status: 'normal',
        },
      ],
      temperatureData: [
        { name: '00:00', value: 3.2 },
        { name: '04:00', value: 3.5 },
        { name: '08:00', value: 4.1 },
        { name: '12:00', value: 3.8 },
        { name: '16:00', value: 3.2 },
        { name: '20:00', value: 3.0 },
        { name: '현재', value: 3.0 },
      ],
      powerData: [
        { name: '00:00', value: 0 },
        { name: '04:00', value: 0 },
        { name: '08:00', value: 0 },
        { name: '12:00', value: 0 },
        { name: '16:00', value: 0 },
        { name: '20:00', value: 0 },
        { name: '현재', value: 0 },
      ],
      usageData: [
        { name: '냉장실', value: 50 },
        { name: '냉동실', value: 50 },
      ],
    }
    // 세탁기
  } else if (selectedAppliance?.productType === 'washer') {
    return {
      name: '세탁기',
      model: 'LG F4V9RWP2E',
      status: 'warning',
      metrics: [
        { name: '상태', value: '대기 중', status: 'normal' },
        { name: '물 사용량', value: '높음', status: 'warning' },
        { name: '진동', value: '정상', status: 'normal' },
        { name: '세제 잔량', value: '15%', status: 'warning' },
      ],
      recommendations: [
        {
          title: '물 사용량 경고',
          summary: '정기 점검 시점이 다가오고 있습니다.',
          description: '최근 세탁 시 물 사용량이 평소보다 20% 증가했습니다.',
          status: 'warning',
        },
        {
          title: '세제 부족',
          summary: '정기 점검 시점이 다가오고 있습니다.',
          description: '세제가 곧 소진될 예정입니다. 보충이 필요합니다.',
          status: 'warning',
        },
        {
          title: '정기 청소 권장',
          summary: '정기 점검 시점이 다가오고 있습니다.',
          description: '드럼 청소가 3개월 동안 실행되지 않았습니다.',
          status: 'normal',
        },
      ],
      cycleData: [
        { name: '표준', value: 12 },
        { name: '울/섬세', value: 3 },
        { name: '스피드워시', value: 8 },
        { name: '타월', value: 2 },
        { name: '이불', value: 1 },
      ],
      waterUsageData: [
        { name: '1주 전', value: 45 },
        { name: '5일 전', value: 48 },
        { name: '3일 전', value: 52 },
        { name: '1일 전', value: 55 },
        { name: '오늘', value: 58 },
      ],
      efficiencyData: [
        { name: '에너지 효율', value: 75 },
        { name: '물 효율', value: 60 },
        { name: '시간 효율', value: 85 },
      ],
    }
    // 에어컨
  } else if (selectedAppliance?.productType === 'aircon') {
    return {
      name: '에어컨',
      model: 'LG DUALCOOL S12EQ',
      status: 'error',
      metrics: [
        { name: '설정 온도', value: '24°C', status: 'normal' },
        { name: '현재 온도', value: '28°C', status: 'error' },
        { name: '필터 상태', value: '교체 필요', status: 'error' },
        { name: '전력 소비', value: '320W', status: 'warning' },
      ],
      recommendations: [
        {
          title: '필터 교체 필요',
          summary: '필터가 오염되어 작동하지 않습니다.',
          description: '필터가 심하게 오염되어 즉시 교체가 필요합니다.',
          status: 'error',
        },
        {
          title: '냉각 성능 저하',
          summary: '기기 온도가 너무 뜨겁습니다.',
          description: '설정 온도에 도달하지 못하고 있습니다. 점검이 필요합니다.',
          status: 'error',
        },
        {
          title: '전력 소비 증가',
          summary: '전력 소비량이 대폭 증가하였습니다.',
          description: '지난 주 대비 전력 소비가 30% 증가했습니다.',
          status: 'warning',
        },
      ],
      temperatureData: [
        { name: '00:00', value: 26 },
        { name: '00:10', value: 25 },
        { name: '00:20', value: 26 },
        { name: '00:30', value: 25 },
        { name: '00:40', value: 26 },
        { name: '00:50', value: 27 },
        { name: '01:00', value: 25 },
        { name: '01:10', value: 25 },
        { name: '01:20', value: 26 },
        { name: '01:30', value: 27 },
        { name: '01:40', value: 28 },
        { name: '01:50', value: 29 },
        { name: '02:00', value: 30 },
        { name: '02:10', value: 32 },
        { name: '02:20', value: 35 },
        { name: '02:30', value: 39 },
        { name: '02:40', value: 49 },
        { name: '02:50', value: 25 },
        { name: '03:00', value: 25 },
        { name: '03:10', value: 25 },
        { name: '03:20', value: 25 },
        { name: '03:30', value: 25 },
        { name: '03:40', value: 25 },
        { name: '03:50', value: 25 },
        { name: '04:00', value: 25 },
        { name: '08:00', value: 26 },
        { name: '12:00', value: 27 },
        { name: '16:00', value: 28 },
        { name: '20:00', value: 28 },
        { name: '현재', value: 28 },
      ],
      powerData: [
        { name: '00:00', value: 280 },
        { name: '04:00', value: 260 },
        { name: '08:00', value: 290 },
        { name: '12:00', value: 310 },
        { name: '16:00', value: 320 },
        { name: '20:00', value: 320 },
        { name: '현재', value: 320 },
      ],
      efficiencyData: [
        { name: '정상 작동', value: 35 },
        { name: '비효율 작동', value: 65 },
      ],
    }
  }

  return null
}

export const appliancesPlaceholder = [
  { id: 'refrigerator', name: '냉장고', status: 'normal' },
  { id: 'washer', name: '세탁기', status: 'warning' },
  { id: 'aircon', name: '에어컨', status: 'error' },
]

export const callHistoryPlaceholder = [
  { date: '2023-11-15', time: '14:30', topic: '냉장고 온도 문제' },
  { date: '2023-10-22', time: '11:15', topic: '세탁기 작동 오류' },
  { date: '2023-09-05', time: '09:45', topic: '에어컨 소음 문제' },
]

export const customerRequestPlaceholder = {
  customerName: '최싸피',
  phoneNumber: '010-1234-0004',
}
