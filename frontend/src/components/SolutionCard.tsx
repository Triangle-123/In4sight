'use client'

import { Card, CardContent, CardHeader } from '@/components/ui/card'
import { SolutionItem } from '@/lib/types'
import { cn } from '@/lib/utils'
import { AlertTriangle, Check, ChevronDown, ChevronUp } from 'lucide-react'
import { useState } from 'react'

// Helper function to get status color
const getStatusColor = (status: string) => {
  switch (status) {
    case '정상':
      return {
        accent: '!border-l-green-500',
        icon: 'text-green-500',
        badge: 'bg-green-50 text-green-700 border-green-100',
        dot: 'bg-green-500',
      }
    case '주의':
      return {
        accent: '!border-l-yellow-500',
        icon: 'text-yellow-500',
        badge: 'bg-yellow-50 text-yellow-700 border-yellow-100',
        dot: 'bg-yellow-500',
      }
    case '위험':
      return {
        accent: '!border-l-red-500',
        icon: 'text-red-500',
        badge: 'bg-red-50 text-red-700 border-red-100',
        dot: 'bg-red-500',
      }
    case '고장':
      return {
        accent: '!border-l-red-500',
        icon: 'text-red-500',
        badge: 'bg-red-50 text-red-700 border-red-100',
        dot: 'bg-red-500',
      }
    default:
      return {
        accent: 'border-l-gray-300',
        icon: 'text-gray-500',
        badge: 'bg-gray-50 text-gray-700 border-gray-100',
        dot: 'bg-gray-500',
      }
  }
}

interface SolutionCardProps {
  data: SolutionItem
}

export default function SolutionCard({ data }: SolutionCardProps) {
  const [isExpanded, setIsExpanded] = useState(false)

  const { failure, cause, solutions } = data.result.data
  const personalizedSolution = solutions.personalizedSolution || []
  const preventativeAdvice = solutions.preventativeAdvice || []

  const status = personalizedSolution[0]?.status || 'default'
  const colors = getStatusColor(status)

  return (
    <Card
      className={cn('w-full shadow-lg rounded-lg border-l-4', colors.accent)}
    >
      <div
        className="cursor-pointer bg-white"
        onClick={() => setIsExpanded(!isExpanded)}
      >
        <CardHeader className="flex flex-row items-start justify-between p-5 pb-2">
          <div className="flex items-start gap-3">
            <div className="relative mt-1">
              <AlertTriangle className={cn('h-5 w-5', colors.icon)} />
            </div>
            <div>
              <h2 className="text-lg font-medium text-gray-800">{failure}</h2>
            </div>
          </div>
          <div className="h-8 w-8 rounded-full flex items-center justify-center bg-gray-100">
            {isExpanded ? (
              <ChevronUp className="h-5 w-5 text-gray-500" />
            ) : (
              <ChevronDown className="h-5 w-5 text-gray-500" />
            )}
          </div>
        </CardHeader>

        {/* Causes in collapsed view */}
        <div className="px-5 pb-5 pt-0">
          <div className="pl-8 space-y-2">
            {cause.map((item: string, index: number) => (
              <div key={index} className="flex items-start gap-2">
                <div className="bg-gray-50 rounded-full p-0.5 mt-1">
                  <Check className={cn('h-3 w-3', colors.icon)} />
                </div>
                <span className="text-xs text-gray-600">{item}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {isExpanded && (
        <CardContent className="p-5 pt-0 space-y-6 bg-white">
          {/* Divider */}
          <div className="h-px bg-gray-100 -mx-5" />

          {/* Solutions */}
          <div>
            <h3 className="text-sm font-medium uppercase tracking-wider text-gray-500 mb-3">
              해결 방법
            </h3>
            {personalizedSolution.map(
              (
                solution: {
                  recommendedSolution: string
                  personalizedContext: string
                },
                index: number,
              ) => (
                <div key={index} className="mb-4">
                  <div
                    className={cn(
                      'text-sm font-medium p-3 rounded-md border mb-3',
                      colors.badge,
                    )}
                  >
                    {solution.recommendedSolution}
                  </div>
                  <div className="text-sm text-gray-600 leading-relaxed pl-1">
                    {solution.personalizedContext}
                  </div>
                </div>
              ),
            )}
          </div>

          {/* Preventative Advice */}
          <div>
            <h3 className="text-sm font-medium uppercase tracking-wider text-gray-500 mb-3">
              예방 조치
            </h3>
            <div className="space-y-2 pl-1">
              {preventativeAdvice.map((advice: string, index: number) => (
                <div key={index} className="flex items-start gap-2">
                  <span className="text-gray-400 mt-1">•</span>
                  <span className="text-sm text-gray-700 leading-relaxed">
                    {advice}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </CardContent>
      )}
    </Card>
  )
}
