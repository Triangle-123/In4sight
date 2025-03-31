"use client"

import { useEffect, useState } from "react"
import { Phone, WashingMachine, Refrigerator, Microwave } from "lucide-react"
import { motion, AnimatePresence } from "framer-motion"

export default function WaitingScreen() {
  const [dots, setDots] = useState(".")
  const [currentApplianceIndex, setCurrentApplianceIndex] = useState(0)
  const [waitTime, setWaitTime] = useState(0)

  const appliances = [
    { icon: WashingMachine, color: "text-blue-500" },
    { icon: Refrigerator, color: "text-green-500" },
    { icon: Microwave, color: "text-orange-500" },
  ]

  useEffect(() => {
    // Animate the dots
    const dotsInterval = setInterval(() => {
      setDots((prev) => (prev.length >= 3 ? "." : prev + "."))
    }, 500)

    // Rotate through appliance icons
    const applianceInterval = setInterval(() => {
      setCurrentApplianceIndex((prev) => (prev + 1) % appliances.length)
    }, 3000)

    // Increment wait time
    const waitTimeInterval = setInterval(() => {
      setWaitTime((prev) => prev + 1)
    }, 60000) // every minute

    return () => {
      clearInterval(dotsInterval)
      clearInterval(applianceInterval)
      clearInterval(waitTimeInterval)
    }
  }, [])

  const formatWaitTime = () => {
    if (waitTime === 0) return "1분 미만"
    if (waitTime === 1) return "1분"
    return `${waitTime}분`
  }

  const CurrentApplianceIcon = appliances[currentApplianceIndex].icon
  const currentColor = appliances[currentApplianceIndex].color

  return (
    // <div className="flex min-h-screen flex-col items-center justify-center bg-gray-50 p-4">
      <div className="w-full rounded-xl bg-white p-8 shadow-lg">
        <div className="mb-6 text-center">
          <h1 className="mb-2 text-2xl font-bold text-gray-800">고객 상담 대기중</h1>
          <p className="text-gray-600">고객 상담 대기중입니다. 잠시만 기다려주세요.</p>
        </div>

        <div className="mb-8 flex justify-center">
          <div className="relative">
            {/* Phone with pulsing ring animation */}
            <motion.div
              className="absolute -inset-4 rounded-full bg-gray-200 opacity-75"
              animate={{
                scale: [1, 1.1, 1],
                opacity: [0.5, 0.2, 0.5],
              }}
              transition={{
                duration: 2,
                repeat: Number.POSITIVE_INFINITY,
                ease: "easeInOut",
              }}
            />
            <div className="relative z-10 rounded-full bg-white p-4">
              <Phone className="h-12 w-12 text-blue-600" />
            </div>
          </div>
        </div>

        {/* Rotating appliance icons */}
        <div className="mb-6 flex justify-center">
          <AnimatePresence mode="wait">
            <motion.div
              key={currentApplianceIndex}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.5 }}
              className="flex h-16 w-16 items-center justify-center"
            >
              <CurrentApplianceIcon className={`h-12 w-12 ${currentColor}`} />
            </motion.div>
          </AnimatePresence>
        </div>

        {/* Status indicators */}
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <span className="text-sm text-gray-600">상태:</span>
            <span className="font-medium text-blue-600">대기중{dots}</span>
          </div>

          <div className="flex items-center justify-between">
            <span className="text-sm text-gray-600">대기한 시간:</span>
            <span className="font-medium text-gray-800">{formatWaitTime()}</span>
          </div>

          {/* Progress bar */}
          <div className="mt-4 h-2 w-full overflow-hidden rounded-full bg-gray-200">
            <motion.div
              className="h-full bg-blue-600"
              initial={{ width: "0%" }}
              animate={{ width: "100%" }}
              transition={{
                duration: 3,
                repeat: Number.POSITIVE_INFINITY,
                repeatType: "loop",
                ease: "linear",
                repeatDelay: 0.1,
              }}
            />
          </div>
        </div>
      </div>
    // </div>
  )
}

