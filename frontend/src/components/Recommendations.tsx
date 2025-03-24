'use client'

import { Card, CardContent } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { ApplianceDataType } from '@/lib/types'
import { AnimatePresence, motion } from 'framer-motion'
import { Loader, MessageSquarePlus } from 'lucide-react'
import { useEffect, useRef, useState } from 'react'

import { StatusBadge } from './StatusBadge'

interface RecommendationsProps {
  applianceData: ApplianceDataType
}

interface UserQuestion {
  title: string
  summary: string
  description: string
  status: 'user'
  isLoading?: boolean
}

export function Recommendations({ applianceData }: RecommendationsProps) {
  const [expandedCards, setExpandedCards] = useState<Record<number, boolean>>({})
  const [showInput, setShowInput] = useState(false)
  const [inputValue, setInputValue] = useState('')
  const [userQuestions, setUserQuestions] = useState<UserQuestion[]>([])
  const inputRef = useRef<HTMLInputElement>(null)
  const lastCardRef = useRef<HTMLDivElement>(null)

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

  const toggleCard = (index: number) => {
    setExpandedCards((prev) => ({ ...prev, [index]: !prev[index] }))
  }

  const handleDoubleClick = (e: React.MouseEvent) => {
    e.stopPropagation()
    setShowInput(true)
  }

  const handleInputBlur = () => {
    if (inputValue.trim() === '') {
      setShowInput(false)
    }
  }

  const handleInputKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Escape') {
      setShowInput(false)
      setInputValue('')
    } else if (e.key === 'Enter' && inputValue.trim() !== '') {
      addUserQuestion()
    }
  }

  const addUserQuestion = () => {
    const newQuestion: UserQuestion = {
      title: inputValue,
      summary: 'AI 분석 결과입니다.',
      description: '커스텀 문의 입니다.',
      status: 'user',
      isLoading: true,
    }

    setUserQuestions([...userQuestions, newQuestion])
    setInputValue('')
    setShowInput(false)
  }

  setTimeout(() => {
    setUserQuestions((prev) => prev.map((q, i) => (i === prev.length - 1 ? { ...q, isLoading: false } : q)))
  }, 5000)

  const processedRecommendations = applianceData.recommendations.map((rec) => ({
    ...rec,
    summary: rec.summary || rec.description?.substring(0, 100) || rec.description,
  }))

  const allItems = [...processedRecommendations, ...userQuestions]

  return (
    <div className="space-y-4 overflow-y-auto max-h-[calc(100vh-10rem)]">
      <h2 className="text-xl font-semibold">권장 해결책</h2>

      <div className="space-y-3">
        <AnimatePresence>
          {allItems.map((item, index) => {
            const isUserQuestion = item.status === 'user'
            const isLastItem = index === allItems.length - 1

            return (
              <motion.div
                key={`${item.title}-${index}`}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, height: 0 }}
                transition={{ duration: 0.3 }}
                ref={isLastItem ? lastCardRef : null}
              >
                <Card
                  className={`cursor-pointer border-l-4 transition-all ${
                    isUserQuestion
                      ? 'border-l-primary'
                      : item.status === 'normal'
                        ? 'border-l-green-500'
                        : item.status === 'warning'
                          ? 'border-l-yellow-500'
                          : 'border-l-red-500'
                  }`}
                  onClick={() => toggleCard(index)}
                  onDoubleClick={handleDoubleClick}
                >
                  <CardContent className="p-4">
                    <div className="flex justify-between items-start mb-2">
                      <h3 className="font-medium flex items-center">
                        {isUserQuestion && <MessageSquarePlus className="h-4 w-4 mr-1 text-primary" />}
                        {item.title}
                      </h3>
                      <StatusBadge status={item.status} />
                    </div>
                    <p className="text-sm text-muted-foreground">
                      {item.isLoading ? (
                        <span className="flex items-center">
                          <Loader className="h-4 w-4 mr-2 animate-spin text-primary" />
                          AI가 응답을 생성하는 중입니다...
                        </span>
                      ) : (
                        item.summary
                      )}
                    </p>

                    {/* Expanded content */}
                    {expandedCards[index] && (
                      <div className="mt-2 p-2 border-t border-gray-200">
                        <p className="text-sm text-gray-700">{item.description || '추가 정보 없음'}</p>
                      </div>
                    )}
                  </CardContent>
                </Card>
              </motion.div>
            )
          })}
        </AnimatePresence>

        <AnimatePresence>
          {showInput && (
            <motion.div
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0 }}
              transition={{ duration: 0.2 }}
            >
              <Card className="border-l-4 border-l-primary">
                <CardContent className="p-4">
                  <Input
                    ref={inputRef}
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    onBlur={handleInputBlur}
                    onKeyDown={handleInputKeyDown}
                    placeholder="질문을 입력하고 Enter 키를 누르세요..."
                    className="border-none shadow-none focus-visible:ring-0 px-0 h-auto text-sm"
                    autoFocus
                  />
                </CardContent>
              </Card>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  )
}
