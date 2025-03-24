import type React from "react"
// This is a placeholder file to simulate the framer-motion package
// In a real project, you would install framer-motion via npm/yarn

export const motion = {
  div: ({ children, ...props }: any) => <div {...props}>{children}</div>,
}

export const AnimatePresence = ({ children }: { children: React.ReactNode }) => <>{children}</>

