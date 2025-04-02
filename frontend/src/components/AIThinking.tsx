'use client'

import { Loader2 } from 'lucide-react'
import { useEffect, useState, useTransition } from 'react'

interface AIThinkingProps {
  message?: string
  className?: string
}

export function AIThinking({
  message = 'AI assistant is thinking',
  className = '',
}: AIThinkingProps) {
  const [dots, setDots] = useState('')
  const [isPending, startTransition] = useTransition()

  useEffect(() => {
    let isMounted = true

    const animateDots = () => {
      if (!isMounted) return

      startTransition(() => {
        setDots((prev) => {
          if (prev.length >= 3) return ''
          return prev + '.'
        })
      })

      setTimeout(animateDots, 500)
    }

    animateDots()

    return () => {
      isMounted = false
    }
  }, [])

  return (
    <div
      className={`flex items-center gap-3 p-4 rounded-lg border bg-muted/50 ${className}`}
    >
      <Loader2 className="h-5 w-5 animate-spin text-primary" />
      <p className="text-sm font-medium">
        {message}
        {dots}
      </p>
    </div>
  )
}
