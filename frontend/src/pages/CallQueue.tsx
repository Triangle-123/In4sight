import { useEffect, useRef, useState } from 'react'
import { useNavigate } from 'react-router-dom'

// Type for a call in the queue
type Call = {
  id: string
  caller: string
  phoneNumber: string
  timestamp: Date
  priority: 'low' | 'medium' | 'high'
  subject: string
}

// Mock data generators
const mockCallers = [
  'John Doe',
  'Jane Smith',
  'Alex Johnson',
  'Sam Wilson',
  'Maria Garcia',
]
const mockSubjects = [
  'Billing inquiry',
  'Technical support',
  'Account question',
  'New service',
  'Complaint',
]
const mockPriorities: ('low' | 'medium' | 'high')[] = ['low', 'medium', 'high']

export default function CallQueue() {
  const navigate = useNavigate()
  const [calls, setCalls] = useState<Call[]>([])
  const [connected, setConnected] = useState(false)
  const [isSimulating, setIsSimulating] = useState(true)
  const simulationIntervalRef = useRef<NodeJS.Timeout | null>(null)

  // Function to generate a random call
  const generateRandomCall = (): Call => {
    return {
      id: Math.random().toString(36).substring(2, 9),
      caller: mockCallers[Math.floor(Math.random() * mockCallers.length)],
      phoneNumber: `+1${Math.floor(Math.random() * 900 + 100)}${Math.floor(Math.random() * 900 + 100)}${Math.floor(
        Math.random() * 9000 + 1000,
      )}`,
      timestamp: new Date(),
      priority:
        mockPriorities[Math.floor(Math.random() * mockPriorities.length)],
      subject: mockSubjects[Math.floor(Math.random() * mockSubjects.length)],
    }
  }

  // Function to add a new call (simulates receiving an SSE event)
  const addNewCall = () => {
    const newCall = generateRandomCall()
    setCalls((prevCalls) => [...prevCalls, newCall])
    console.log('New call received:', newCall)
  }

  // Function to manually add a call (for testing)
  const handleManualAddCall = () => {
    addNewCall()
  }

  // Function to toggle the simulation
  const toggleSimulation = () => {
    setIsSimulating((prev) => !prev)
  }

  // Set up the SSE simulation
  useEffect(() => {
    // Start the simulation
    if (isSimulating) {
      setConnected(true)
      console.log('SSE simulation started')

      // Add an initial call immediately
      setTimeout(addNewCall, 500)

      // Set up interval to add calls periodically
      simulationIntervalRef.current = setInterval(addNewCall, 5000)
    } else {
      // Stop the simulation
      if (simulationIntervalRef.current) {
        clearInterval(simulationIntervalRef.current)
        simulationIntervalRef.current = null
      }
      setConnected(false)
      console.log('SSE simulation stopped')
    }

    // Clean up on unmount
    return () => {
      if (simulationIntervalRef.current) {
        clearInterval(simulationIntervalRef.current)
      }
      setConnected(false)
      console.log('Component unmounted, SSE simulation cleaned up')
    }
  }, [isSimulating])

  // Function to handle taking a call
  const handleTakeCall = (id: string) => {
    setCalls((prevCalls) => prevCalls.filter((call) => call.id !== id))
    console.log('Call taken:', id)
    navigate('/dashboard')
  }

  // Function to get priority badge color
  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high':
        return 'bg-red-100 text-red-800'
      case 'medium':
        return 'bg-yellow-100 text-yellow-800'
      case 'low':
        return 'bg-green-100 text-green-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-6xl mx-auto">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-3xl font-bold">Call Waiting Queue</h1>
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2">
              <div
                className={`w-3 h-3 rounded-full ${connected ? 'bg-green-500' : 'bg-red-500'}`}
              ></div>
              <span>{connected ? 'Connected' : 'Disconnected'}</span>
            </div>
            <button
              onClick={toggleSimulation}
              className={`px-3 py-1 rounded text-white ${isSimulating ? 'bg-red-500 hover:bg-red-600' : 'bg-green-500 hover:bg-green-600'}`}
            >
              {isSimulating ? 'Stop Simulation' : 'Start Simulation'}
            </button>
            <button
              onClick={handleManualAddCall}
              className="px-3 py-1 bg-blue-500 text-white rounded hover:bg-blue-600"
            >
              Add Call Manually
            </button>
          </div>
        </div>

        <div className="bg-white rounded-lg shadow overflow-hidden">
          {calls.length === 0 ? (
            <div className="p-8 text-center">
              <p className="text-gray-500 text-lg">No calls in the queue</p>
              <p className="text-gray-400">
                New calls will appear here when received
              </p>
            </div>
          ) : (
            <div>
              {/* Table header */}
              <div className="grid grid-cols-12 gap-4 p-4 font-medium text-sm text-gray-500 border-b bg-gray-50">
                <div className="col-span-1">Priority</div>
                <div className="col-span-3">Subject</div>
                <div className="col-span-2">Caller</div>
                <div className="col-span-2">Phone Number</div>
                <div className="col-span-2">Time</div>
                <div className="col-span-2 text-right">Action</div>
              </div>

              {/* Call list */}
              <div className="divide-y">
                {calls.map((call) => (
                  <div
                    key={call.id}
                    className="grid grid-cols-12 gap-4 p-4 items-center hover:bg-gray-50"
                  >
                    <div className="col-span-1">
                      <span
                        className={`px-2 py-1 rounded-full text-xs font-medium ${getPriorityColor(call.priority)}`}
                      >
                        {call.priority}
                      </span>
                    </div>
                    <div className="col-span-3 font-medium">{call.subject}</div>
                    <div className="col-span-2 flex items-center gap-2">
                      <svg
                        className="h-4 w-4 text-gray-500"
                        xmlns="http://www.w3.org/2000/svg"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="2"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                      >
                        <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
                        <circle cx="12" cy="7" r="4"></circle>
                      </svg>
                      <span>{call.caller}</span>
                    </div>
                    <div className="col-span-2 flex items-center gap-2">
                      <svg
                        className="h-4 w-4 text-gray-500"
                        xmlns="http://www.w3.org/2000/svg"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="2"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                      >
                        <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path>
                      </svg>
                      <span>{call.phoneNumber}</span>
                    </div>
                    <div className="col-span-2 flex items-center gap-2">
                      <svg
                        className="h-4 w-4 text-gray-500"
                        xmlns="http://www.w3.org/2000/svg"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="2"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                      >
                        <circle cx="12" cy="12" r="10"></circle>
                        <polyline points="12 6 12 12 16 14"></polyline>
                      </svg>
                      <span>{call.timestamp.toLocaleTimeString()}</span>
                    </div>
                    <div className="col-span-2 text-right">
                      <button
                        onClick={() => handleTakeCall(call.id)}
                        className="px-3 py-1 bg-blue-600 text-white text-sm rounded hover:bg-blue-700"
                      >
                        Take Call
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
