import CallQueue from '@/pages/CallQueue'
import Dashboard from '@/pages/Dashboard'
import Login from '@/pages/Login'
import { BrowserRouter, Route, Routes } from 'react-router-dom'

export default function Home() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/call-queue" element={<CallQueue />} />
        <Route path="/dashboard" element={<Dashboard />} />
      </Routes>
    </BrowserRouter>
  )
}
