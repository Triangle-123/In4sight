import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

export default function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [rememberMe, setRememberMe] = useState(false)
  const navigate = useNavigate()

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    // Add authentication logic here
    navigate('/call-queue')
  }

  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-[#f5f7fb] p-4">
      <img
        src="/image/samsung-service.png"
        alt="삼성전자서비스 로고"
        className="h-16 mb-8"
      />
      <div className="w-full max-w-md bg-white rounded-lg shadow-lg p-8">
        <div className="flex flex-col items-center space-y-6 mb-8">
          <h2 className="text-2xl font-bold text-[#1428a0]">로그인</h2>
        </div>
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="space-y-2">
            <label
              htmlFor="email"
              className="block text-sm font-medium text-gray-700"
            >
              이메일
            </label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="name@example.com"
              required
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#1428a0] focus:border-transparent"
            />
          </div>
          <div className="space-y-2">
            <label
              htmlFor="password"
              className="block text-sm font-medium text-gray-700"
            >
              비밀번호
            </label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-[#1428a0] focus:border-transparent"
            />
          </div>
          <div className="flex items-center space-x-2">
            <input
              id="remember"
              type="checkbox"
              checked={rememberMe}
              onChange={(e) => setRememberMe(e.target.checked)}
              className="rounded border-gray-300 text-[#1428a0] focus:ring-[#1428a0]"
            />
            <label
              htmlFor="remember"
              className="text-sm font-normal text-gray-700"
            >
              로그인 상태 유지
            </label>
          </div>
          <button
            type="submit"
            className="w-full py-3 px-4 bg-[#1428a0] text-white rounded-md hover:bg-[#1a237e] transition-colors duration-200 font-medium"
          >
            로그인
          </button>
        </form>
      </div>
    </div>
  )
}
