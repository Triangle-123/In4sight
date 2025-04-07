'use client'

// import { solutionPlaceholder } from '@/lib/placeholder-data'
import { SolutionItem } from '@/lib/types'
import useStore from '@/store/store'
import { AnimatePresence, motion } from 'framer-motion'
import { useRef, useEffect, useMemo } from 'react'

import { AIThinking } from './AIThinking'
import SolutionCard from './SolutionCard'

export function Recommendations() {
  const lastCardRef = useRef<HTMLDivElement>(null)
  const solutionData = useStore((state) => state.solutionData) as
    | SolutionItem[]
    | undefined
  const selectedAppliance = useStore((state) => state.selectedAppliance)
  const applianceSerialNumber = selectedAppliance?.serialNumber

  const statusPriority: Record<string, number> = {
    '고장': 1,
    '주의': 2,
    '정상': 3
  }

  const filteredSolutionData = useMemo(() => {
    return solutionData
      ?.filter((item: SolutionItem) => item.result.serialNumber === applianceSerialNumber)
      ?.sort((a, b) => {
        // 상태 우선순위에 따른 정렬
        const statusA = statusPriority[a.result.data.solutions.personalizedSolution[0].status]
        const statusB = statusPriority[b.result.data.solutions.personalizedSolution[0].status]
        
        if (statusA !== statusB) {
          return statusA - statusB
        }
        
        // 상태가 같으면 failure 문자열로 알파벳 순 정렬
        return a.result.data.failure.localeCompare(b.result.data.failure)
      })
  }, [solutionData, applianceSerialNumber])

  // solutionData가 변경될 때마다 스크롤을 맨 위로 이동
  useEffect(() => {
    if (lastCardRef.current) {
      lastCardRef.current.scrollIntoView({ behavior: 'smooth' })
    }
  }, [filteredSolutionData])

  return (
    <div className="h-full overflow-y-auto overflow-x-hidden [&::-webkit-scrollbar]:hidden [-ms-overflow-style:none] [scrollbar-width:none]">
      <div className="flex justify-between items-center sticky top-0 bg-white z-10 pb-4">
        <h2 className="text-xl font-semibold">권장 해결책</h2>
      </div>

      <div className="space-y-3">
        {!filteredSolutionData || filteredSolutionData.length === 0 ? (
          <AIThinking message="AI 어시스턴트가 해결책을 찾고 있습니다" />
        ) : (
          <AnimatePresence>
            {filteredSolutionData.map((item: SolutionItem, index: number) => {
              const isLastItem = index === filteredSolutionData.length - 1

              return (
                <motion.div
                  key={`${index}-${item.result.data.failure}`}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, height: 0 }}
                  transition={{ duration: 0.3 }}
                  ref={isLastItem ? lastCardRef : null}
                  className="overflow-hidden"
                >
                  <SolutionCard data={item} />
                </motion.div>
              )
            })}
          </AnimatePresence>
        )}
      </div>
    </div>
  )
}
