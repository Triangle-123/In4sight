'use client'

// import { solutionPlaceholder } from '@/lib/placeholder-data'
import { SolutionItem } from '@/lib/types'
import useStore from '@/store/store'
import { AnimatePresence, motion } from 'framer-motion'
import { useEffect, useMemo, useRef, useState } from 'react'

import { AIThinking } from './AIThinking'
import SolutionCard from './SolutionCard'

export function Recommendations() {
  const [showAllGreen, setShowAllGreen] = useState(false)
  const lastCardRef = useRef<HTMLDivElement>(null)
  const solutionData = useStore((state) => state.solutionData) as SolutionItem[] | undefined
  const selectedAppliance = useStore((state) => state.selectedAppliance)
  const selectedSolution = useStore((state) => state.selectedSolution)
  const setSelectedSolution = useStore((state) => state.setSelectedSolution)
  
  const applianceSerialNumber = selectedAppliance?.serialNumber

  const statusPriority: Record<string, number> = { 고장: 1, 주의: 2, 정상: 3 }

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

  useEffect(() => {
    if (!filteredSolutionData || filteredSolutionData.length === 0) {
      const timer = setTimeout(() => {
        setShowAllGreen(true)
      }, 14000)

      return () => clearTimeout(timer)
    } else {
      setShowAllGreen(false)
    }
  }, [filteredSolutionData])

  return (
    <div className="h-full overflow-y-auto overflow-x-hidden [&::-webkit-scrollbar]:hidden [-ms-overflow-style:none] [scrollbar-width:none]">
      <div className="flex justify-between items-center sticky top-0 bg-white z-10 pb-4">
        <h2 className="text-xl font-semibold">권장 해결책</h2>
      </div>

      <div className="space-y-3">
        {!filteredSolutionData || filteredSolutionData.length === 0 ? (
          showAllGreen ? (
            <div className="bg-green-50 border border-green-200 rounded-lg p-6 text-center">
              <div className="text-green-600 text-2xl mb-2">✓</div>
              <h3 className="text-green-800 font-semibold mb-1">기기의 모든 기능이 정상입니다</h3>
              <p className="text-green-600 text-sm">현재 선택된 기기에서 발견된 문제가 없습니다.</p>
            </div>
          ) : (
            <AIThinking message="AI 어시스턴트가 해결책을 찾고 있습니다" />
          )
        ) : (
          <AnimatePresence>
            {filteredSolutionData.map((solution: SolutionItem, index: number) => {
              const isLastItem = index === filteredSolutionData.length - 1

              return (
                <motion.div
                  key={`${index}-${solution.result.data.failure}`}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, height: 0 }}
                  transition={{ duration: 0.3 }}
                  ref={isLastItem ? lastCardRef : null}
                  className="overflow-hidden"
                >
                  <SolutionCard
                    data={solution}
                    isExpanded={solution === selectedSolution}
                    onExpand={() => {
                      setSelectedSolution(solution === selectedSolution ? null : solution)
                    }}
                  />
                </motion.div>
              )
            })}
          </AnimatePresence>
        )}
      </div>
    </div>
  )
}
