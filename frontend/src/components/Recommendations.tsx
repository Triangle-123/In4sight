import { Card, CardContent } from '@/components/ui/card'
import type { ApplianceDataType } from '@/lib/types'
import { useState } from 'react'

import { StatusBadge } from './StatusBadge'

interface RecommendationsProps {
  applianceData: ApplianceDataType
}

export function Recommendations({ applianceData }: RecommendationsProps) {
  const [expandedCards, setExpandedCards] = useState<Record<number, boolean>>({})
  const toggleCard = (index: number) => {
    setExpandedCards((prev) => ({
      ...prev,
      [index]: !prev[index], // 클릭한 카드만 토글
    }))
  }

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold">권장 해결책</h2>
      <div className="space-y-3">
        {applianceData.recommendations.map((recommendation, index) => (
          <Card
            key={index}
            onClick={() => toggleCard(index)}
            className={`cursor-pointer border-l-4 transition-all ${
              recommendation.status === 'normal'
                ? 'border-l-green-500'
                : recommendation.status === 'warning'
                  ? 'border-l-yellow-500'
                  : 'border-l-red-500'
            }`}
          >
            <CardContent className="p-4">
              <div className="flex justify-between items-start mb-2">
                <h3 className="font-medium">{recommendation.title}</h3>
                <StatusBadge status={recommendation.status} />
              </div>
              <p className="text-sm text-muted-foreground">{recommendation.summary}</p>

              {/* 추가 정보 (해당 카드가 펼쳐졌을 때만 표시) */}
              {expandedCards[index] && (
                <div className="mt-2 p-2 border-t border-gray-200">
                  <p className="text-sm text-gray-700">{recommendation.description || '추가 정보 없음'}</p>
                </div>
              )}
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )
}
