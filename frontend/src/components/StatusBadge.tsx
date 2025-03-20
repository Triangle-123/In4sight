import { AlertTriangle, CheckCircle, CircleUserRound, XCircle } from 'lucide-react'

interface StatusBadgeProps {
  status: string
}

export function StatusBadge({ status }: StatusBadgeProps) {
  switch (status) {
    case 'normal':
      return (
        <div className="flex items-center space-x-2 text-green-600">
          <CheckCircle className="w-5 h-5" />
          <span>정상</span>
        </div>
      )
    case 'warning':
      return (
        <div className="flex items-center space-x-2 text-yellow-600">
          <AlertTriangle className="w-5 h-5" />
          <span>주의</span>
        </div>
      )
    case 'error':
      return (
        <div className="flex items-center space-x-2 text-red-600">
          <XCircle className="w-5 h-5" />
          <span>오류</span>
        </div>
      )
    case 'user':
      return (
        <div className="flex items-center space-x-2 text-blue-600">
          <CircleUserRound className="w-5 h-5" />
          <span>질문</span>
        </div>
      )
    default:
      return (
        <div className="flex items-center space-x-2 text-gray-600">
          <XCircle className="w-5 h-5" />
          <span>알 수 없음</span>
        </div>
      )
  }
}
