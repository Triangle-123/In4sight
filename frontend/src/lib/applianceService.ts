/* 예시 데이터 */
import type { ApplianceDataType } from './types'

export function getApplianceData(selectedAppliance: string | null): ApplianceDataType | null {
  if (selectedAppliance === 'refrigerator') {
    return {
      name: '냉장고',
      model: '삼성 RS27T5561SR',
      status: 'normal',
      metrics: [
        { name: '온도', value: '3°C', status: 'normal' },
        { name: '습도', value: '42%', status: 'normal' },
        { name: '전력 소비', value: '120W', status: 'normal' },
        { name: '도어 열림', value: '8회/일', status: 'normal' },
      ],
      recommendations: [
        { title: '정기 점검 안내', description: '다음 정기 점검은 30일 후 예정되어 있습니다.', status: 'normal' },
        { title: '필터 교체 안내', description: '정수 필터 교체까지 45일 남았습니다.', status: 'normal' },
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
        { name: '00:00', value: 110 },
        { name: '04:00', value: 105 },
        { name: '08:00', value: 130 },
        { name: '12:00', value: 145 },
        { name: '16:00', value: 125 },
        { name: '20:00', value: 115 },
        { name: '현재', value: 120 },
      ],
      usageData: [
        { name: '냉장실', value: 65 },
        { name: '냉동실', value: 35 },
      ],
    }
  } else if (selectedAppliance === 'washer') {
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
          title: '물 사���량 경고',
          description: '최근 세탁 시 물 사용량이 평소보다 20% 증가했습니다.',
          status: 'warning',
        },
        { title: '세제 부족', description: '세제가 곧 소진될 예정입니다. 보충이 필요합니다.', status: 'warning' },
        { title: '정기 청소 권장', description: '드럼 청소가 3개월 동안 실행되지 않았습니다.', status: 'normal' },
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
  } else if (selectedAppliance === 'aircon') {
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
        { title: '필터 교체 필요', description: '필터가 심하게 오염되어 즉시 교체가 필요합니다.', status: 'error' },
        {
          title: '냉각 성능 저하',
          description: '설정 온도에 도달하지 못하고 있습니다. 점검이 필요합니다.',
          status: 'error',
        },
        { title: '전력 소비 증가', description: '지난 주 대비 전력 소비가 30% 증가했습니다.', status: 'warning' },
      ],
      temperatureData: [
        { name: '00:00', value: 26 },
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
  } else if (selectedAppliance === 'tv') {
    return {
      name: 'TV',
      model: '삼성 QN90A',
      status: 'normal',
      metrics: [
        { name: '상태', value: '켜짐', status: 'normal' },
        { name: '볼륨', value: '15', status: 'normal' },
        { name: '밝기', value: '80%', status: 'normal' },
        { name: '사용 시간', value: '3.5시간/일', status: 'normal' },
      ],
      recommendations: [
        { title: '소프트웨어 업데이트', description: '새로운 소프트웨어 업데이트가 가능합니다.', status: 'normal' },
        {
          title: '에너지 절약 모드',
          description: '에너지 절약 모드를 활성화하여 전력 소비를 줄일 수 있습니다.',
          status: 'normal',
        },
      ],
      usageData: [
        { name: '월', value: 4.2 },
        { name: '화', value: 3.1 },
        { name: '수', value: 2.8 },
        { name: '목', value: 3.5 },
        { name: '금', value: 5.2 },
        { name: '토', value: 6.1 },
        { name: '일', value: 5.8 },
      ],
      appUsageData: [
        { name: '넷플릭스', value: 45 },
        { name: '유튜브', value: 30 },
        { name: '케이블TV', value: 15 },
        { name: '기타', value: 10 },
      ],
    }
  } else if (selectedAppliance === 'oven') {
    return {
      name: '오븐',
      model: 'LG DIOS 광파오븐',
      status: 'normal',
      metrics: [
        { name: '상태', value: '대기 중', status: 'normal' },
        { name: '마지막 사용', value: '2일 전', status: 'normal' },
        { name: '청소 상태', value: '양호', status: 'normal' },
        { name: '전력 소비', value: '0W', status: 'normal' },
      ],
      recommendations: [
        { title: '정기 청소 안내', description: '다음 정기 청소는 15일 후 예정되어 있습니다.', status: 'normal' },
        {
          title: '레시피 추천',
          description: '고객의 사용 패턴에 맞는 새로운 레시피가 추가되었습니다.',
          status: 'normal',
        },
      ],
      usageData: [
        { name: '구이', value: 35 },
        { name: '베이킹', value: 25 },
        { name: '데우기', value: 30 },
        { name: '기타', value: 10 },
      ],
      temperatureData: [
        { name: '구이', value: 220 },
        { name: '베이킹', value: 180 },
        { name: '데우기', value: 120 },
        { name: '해동', value: 80 },
      ],
    }
  }

  return null
}

export const appliances = [
  { id: 'refrigerator', name: '냉장고', status: 'normal' },
  { id: 'washer', name: '세탁기', status: 'warning' },
  { id: 'aircon', name: '에어컨', status: 'error' },
  { id: 'tv', name: 'TV', status: 'normal' },
  { id: 'oven', name: '오븐', status: 'normal' },
]

export const callHistory = [
  { date: '2023-11-15', time: '14:30', topic: '냉장고 온도 문제' },
  { date: '2023-10-22', time: '11:15', topic: '세탁기 작동 오류' },
  { date: '2023-09-05', time: '09:45', topic: '에어컨 소음 문제' },
]
