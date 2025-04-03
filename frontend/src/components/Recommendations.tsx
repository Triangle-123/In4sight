'use client'

// import { solutionPlaceholder } from '@/lib/placeholder-data'
import { ApplianceFailureData } from '@/lib/types'
import { AnimatePresence, motion } from 'framer-motion'
import { useEffect, useRef, useState } from 'react'
import useStore from '@/store/store'
import { AIThinking } from './AIThinking'

import SolutionCard from './SolutionCard'

interface SolutionItem {
  result: {
    data: {
      failure: string;
    };
  };
}

export function Recommendations() {
  const [showInput, setShowInput] = useState(false)
  const [inputValue, setInputValue] = useState('')
  const [userQuestions, setUserQuestions] = useState<ApplianceFailureData[]>([])
  const [useDummyData, setUseDummyData] = useState(true)
  const inputRef = useRef<HTMLInputElement>(null)
  const lastCardRef = useRef<HTMLDivElement>(null)
  const solutionData = useStore((state) => state.solutionData) as SolutionItem[] | undefined

  useEffect(() => {
    if (showInput && inputRef.current) {
      inputRef.current.focus()
    }
  }, [showInput])

  useEffect(() => {
    if (userQuestions.length > 0 && lastCardRef.current) {
      lastCardRef.current.scrollIntoView({ behavior: 'smooth' })
    }
  }, [userQuestions])

  return (
    <div className="h-full overflow-y-auto overflow-x-hidden">
      <div className="flex justify-between items-center sticky top-0 bg-white z-10 pb-4">
        <h2 className="text-xl font-semibold">권장 해결책</h2>
        {/* <button
          onClick={() => setUseDummyData(!useDummyData)}
          className="text-sm px-2 py-1 bg-gray-100 rounded hover:bg-gray-200"
        >
          {useDummyData ? '실제 데이터 보기' : '더미 데이터 보기'}
        </button> */}
      </div>

      <div className="space-y-3">
        {!solutionData || solutionData.length === 0 ? (
          <AIThinking message="AI 어시스턴트가 해결책을 찾고 있습니다" />
        ) : (
          <AnimatePresence>
            {solutionData.map((item: SolutionItem, index: number) => {
              const isLastItem = index === solutionData.length - 1

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

        {/* <AnimatePresence>
          {showInput && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              transition={{ duration: 0.2 }}
            >
              <div className="p-4 border rounded-lg">
                <input
                  ref={inputRef}
                  value={inputValue}
                  onChange={(e) => setInputValue(e.target.value)}
                  onBlur={handleInputBlur}
                  onKeyDown={handleInputKeyDown}
                  placeholder="질문을 입력하고 Enter 키를 누르세요..."
                  className="w-full border-none shadow-none focus-visible:ring-0 px-0 h-auto text-sm"
                  autoFocus
                />
              </div>
            </motion.div>
          )}
        </AnimatePresence> */}
      </div>
    </div>
  )
}
