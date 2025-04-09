import { Button } from '@/components/ui/button'
import { motion } from 'framer-motion'
import { useEffect, useRef, useState } from 'react'

export default function MarqueeButton({
  children,
  className,
  ...props
}: {
  children: React.ReactNode
  className?: string
  [key: string]: any
}) {
  const textRef = useRef<HTMLSpanElement>(null)
  const containerRef = useRef<HTMLButtonElement>(null)
  const [isOverflow, setIsOverflow] = useState(false)
  const [isHovered, setIsHovered] = useState(false)
  const [textWidth, setTextWidth] = useState(0)

  useEffect(() => {
    if (textRef.current && containerRef.current) {
      const width = textRef.current.scrollWidth
      const containerWidth = containerRef.current.clientWidth
      setIsOverflow(width > containerWidth)
      setTextWidth(width)
    }
  }, [children])

  return (
    <Button
      ref={containerRef}
      className={`overflow-hidden ${className} bg-white shadow-sm border border-black`}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      {...props}
    >
      <div className="relative w-full">
        <motion.span
          ref={textRef}
          className="inline-block whitespace-nowrap"
          animate={
            isOverflow && isHovered
              ? {
                  x: [0, -(textWidth - (containerRef.current?.clientWidth || 0) + 32), 0],
                  transition: { 
                    x: { 
                      repeat: Infinity, 
                      repeatType: 'loop', 
                      duration: 3, 
                      ease: 'linear',
                      times: [0, 0.5, 1]
                    } 
                  },
                }
              : {
                  x: 0,
                  transition: { duration: 0.3 }
                }
          }
        >
          {children}
        </motion.span>
      </div>
    </Button>
  )
}
