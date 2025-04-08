import useStore from '@/store/store'
import { useNavigate } from 'react-router-dom'

export default function Login() {
  const createSseConnection = useStore((state) => state.createSseConnection)
  const navigate = useNavigate()

  const handleSubmit = (e: React.MouseEvent<HTMLButtonElement>) => {
    e.preventDefault()
    // SSE 연결 후 큐 페이지로 이동
    createSseConnection()
    navigate('/call-queue')
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-[#f5f7fb] p-0.5">
      <div className="flex w-full max-w-[90vw] gap-1">
        {/* 로그인 폼 */}
        <div className="w-1/4 bg-white rounded-lg shadow-lg p-3 flex flex-col h-[800px]">
          {/* 상단 로고 */}
          <div className="flex flex-col items-center space-y-2 mt-16">
            <img
              src="/image/logo.png"
              alt="삼성전자서비스 로고"
              className="h-28"
            />
          </div>

          {/* 중간 요약 내용 */}
          <div className="flex-1 flex flex-col justify-center items-center text-center space-y-4">
            <h2 className="text-2xl font-bold text-gray-800">고객 데이터 기반 상담 보조 서비스</h2>
            <div className="space-y-3">
              <p className="text-lg text-gray-600">실시간 기기 데이터를 통한 분석</p>
              <p className="text-lg text-gray-600">개인화된 증상 진단</p>
              <p className="text-lg text-gray-600">최적의 해결책과 상담 제안</p>
            </div>
          </div>

          {/* 하단 버튼 */}
          <div className="mt-auto">
            <button
              type="submit"
              onClick={handleSubmit}
              className="w-full py-3 px-4 bg-[#1428a0] text-white rounded-md hover:bg-[#1a237e] transition-colors duration-200 font-medium"
            >
              시작하기
            </button>
          </div>
        </div>

        {/* GIF 영역 */}
        <div className="w-3/4 flex items-center justify-center">
          <img
            src="/image/main.gif"
            alt="로그인 애니메이션"
            className="w-full h-[800px] object-cover rounded-lg shadow-lg"
          />
        </div>
      </div>
    </div>
  )
}
