'use client'

// import { solutionPlaceholder } from '@/lib/placeholder-data'
import { SolutionItem } from '@/lib/types'
import useStore from '@/store/store'
import { AnimatePresence, motion } from 'framer-motion'
import { useRef } from 'react'

import { AIThinking } from './AIThinking'
import SolutionCard from './SolutionCard'

export function Recommendations() {
  const lastCardRef = useRef<HTMLDivElement>(null)
  const solutionData = useStore((state) => state.solutionData) as
    | SolutionItem[]
    | undefined
  const selectedAppliance = useStore((state) => state.selectedAppliance)
  const applianceSerialNumber = selectedAppliance?.serialNumber
  const filteredSolutionData = solutionData?.filter(
    (item: SolutionItem) => item.result.serialNumber === applianceSerialNumber,
  )

  return (
    <div className="h-full overflow-y-auto overflow-x-hidden">
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
