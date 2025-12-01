import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import CountUpNumber from '../components/CountUpNumber'
import { useScrollReveal, ScrollReveal, StaggeredReveal } from '../hooks/useScrollReveal'
import { 
  FlagIcon,
  CheckCircleIcon,
  CalendarIcon,
  ClockIcon
} from '@heroicons/react/24/outline'

// Mock data - replace with API call when available
const MOCK_MILESTONES = [
  { id: 1, title: 'Complete React Course', goal: 'Full Stack Developer', date: '2024-02-15', status: 'completed', progress: 100 },
  { id: 2, title: 'Build Portfolio Website', goal: 'Full Stack Developer', date: '2024-02-28', status: 'completed', progress: 100 },
  { id: 3, title: 'Learn Node.js Basics', goal: 'Backend Development', date: '2024-03-10', status: 'in_progress', progress: 65 },
  { id: 4, title: 'Master TypeScript', goal: 'Full Stack Developer', date: '2024-03-20', status: 'in_progress', progress: 40 },
  { id: 5, title: 'Deploy First App', goal: 'Full Stack Developer', date: '2024-03-25', status: 'upcoming', progress: 0 },
  { id: 6, title: 'Learn Docker Basics', goal: 'DevOps Skills', date: '2024-04-05', status: 'upcoming', progress: 0 },
  { id: 7, title: 'AWS Certification', goal: 'Cloud Engineering', date: '2024-04-15', status: 'upcoming', progress: 0 },
  { id: 8, title: 'Contribute to Open Source', goal: 'Career Growth', date: '2024-04-20', status: 'upcoming', progress: 0 }
]

const Milestones = () => {
  const [milestones, setMilestones] = useState([])
  const [statsRef, statsVisible] = useScrollReveal({ threshold: 0.2 })

  useEffect(() => {
    // TODO: Replace with actual API call
    setMilestones(MOCK_MILESTONES)
  }, [])

  const stats = {
    total: milestones.length,
    completed: milestones.filter(m => m.status === 'completed').length,
    upcoming: milestones.filter(m => m.status === 'upcoming' && new Date(m.date).getMonth() === new Date().getMonth()).length
  }

  const sortedMilestones = [...milestones].sort((a, b) => new Date(a.date) - new Date(b.date))
  const upcomingMilestones = milestones.filter(m => m.status === 'upcoming')
  const inProgressMilestones = milestones.filter(m => m.status === 'in_progress')
  const completedMilestones = milestones.filter(m => m.status === 'completed')

  const getStatusColor = (status) => {
    switch(status) {
      case 'completed': return 'bg-green-100 text-green-700 border-green-200'
      case 'in_progress': return 'bg-blue-100 text-blue-700 border-blue-200'
      case 'upcoming': return 'bg-purple-100 text-purple-700 border-purple-200'
      default: return 'bg-gray-100 text-gray-700 border-gray-200'
    }
  }

  const getStatusLabel = (status) => {
    switch(status) {
      case 'completed': return 'Completed'
      case 'in_progress': return 'In Progress'
      case 'upcoming': return 'Upcoming'
      default: return status
    }
  }

  return (
    <div className="px-4 sm:px-6 lg:px-8 py-6">
      {/* Compact Header */}
      <ScrollReveal className="max-w-7xl mx-auto mb-6">
        <div className="mb-2">
          <h1 className="text-3xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
            Milestones
          </h1>
          <p className="text-sm text-gray-600 mt-1">
            Track key checkpoints across all your goals in one clean view.
          </p>
        </div>
      </ScrollReveal>

      {/* Compact Stats Row */}
      <ScrollReveal className="max-w-7xl mx-auto mb-6" delay={100}>
        <div ref={statsRef} className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div className="flex items-center justify-between rounded-2xl bg-white/80 backdrop-blur px-4 py-3 shadow-sm border border-white/40 hover:shadow-md transition-all">
            <div className="flex items-center space-x-3">
              <FlagIcon className="h-5 w-5 text-purple-600" />
              <span className="text-sm font-medium text-gray-700">Total</span>
            </div>
            <span className="text-2xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
              <CountUpNumber endValue={stats.total} durationMs={1000} startOnVisible={statsVisible} />
            </span>
          </div>

          <div className="flex items-center justify-between rounded-2xl bg-white/80 backdrop-blur px-4 py-3 shadow-sm border border-white/40 hover:shadow-md transition-all">
            <div className="flex items-center space-x-3">
              <CheckCircleIcon className="h-5 w-5 text-green-600" />
              <span className="text-sm font-medium text-gray-700">Completed</span>
            </div>
            <span className="text-2xl font-bold bg-gradient-to-r from-green-600 to-emerald-600 bg-clip-text text-transparent">
              <CountUpNumber endValue={stats.completed} durationMs={1000} startOnVisible={statsVisible} />
            </span>
          </div>

          <div className="flex items-center justify-between rounded-2xl bg-white/80 backdrop-blur px-4 py-3 shadow-sm border border-white/40 hover:shadow-md transition-all">
            <div className="flex items-center space-x-3">
              <CalendarIcon className="h-5 w-5 text-blue-600" />
              <span className="text-sm font-medium text-gray-700">This Month</span>
            </div>
            <span className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-cyan-600 bg-clip-text text-transparent">
              <CountUpNumber endValue={stats.upcoming} durationMs={1000} startOnVisible={statsVisible} />
            </span>
          </div>
        </div>
      </ScrollReveal>

      {/* Compact Timeline */}
      <ScrollReveal className="max-w-7xl mx-auto mb-6" delay={200}>
        <div className="backdrop-blur-sm bg-white/80 rounded-2xl p-5 shadow-sm border border-white/40">
          <h2 className="text-lg font-bold text-gray-900 mb-4">
            Milestone Timeline
          </h2>
          
          <div className="max-h-[360px] overflow-y-auto pr-2">
            <div className="relative">
              <div className="absolute left-2 top-0 bottom-0 w-0.5 bg-gradient-to-b from-purple-300 to-pink-300"></div>
              
              <div className="space-y-3">
                {sortedMilestones.map((milestone) => (
                  <div key={milestone.id} className="relative pl-8 group">
                    <div className={`absolute left-0.5 w-3 h-3 rounded-full border-2 ${
                      milestone.status === 'completed' ? 'bg-green-500 border-green-300' :
                      milestone.status === 'in_progress' ? 'bg-blue-500 border-blue-300' :
                      'bg-purple-500 border-purple-300'
                    } group-hover:scale-125 transition-transform`}></div>
                    
                    <div className="bg-white/60 rounded-xl p-3 border border-white/50 hover:bg-white/80 hover:shadow-sm transition-all cursor-pointer">
                      <div className="flex items-start justify-between gap-2">
                        <div className="flex-1 min-w-0">
                          <h3 className="font-semibold text-gray-900 text-sm mb-0.5 truncate">{milestone.title}</h3>
                          <p className="text-xs text-gray-600 mb-1">{milestone.goal}</p>
                          <div className="flex items-center text-xs text-gray-500">
                            <ClockIcon className="w-3 h-3 mr-1" />
                            {new Date(milestone.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                          </div>
                        </div>
                        <span className={`text-xs px-2 py-0.5 rounded-full border flex-shrink-0 ${getStatusColor(milestone.status)}`}>
                          {getStatusLabel(milestone.status)}
                        </span>
                      </div>
                      {milestone.progress > 0 && milestone.progress < 100 && (
                        <div className="mt-2">
                          <div className="w-full bg-gray-200 rounded-full h-1">
                            <div 
                              className="bg-gradient-to-r from-purple-600 to-pink-600 h-1 rounded-full transition-all"
                              style={{ width: `${milestone.progress}%` }}
                            ></div>
                          </div>
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </ScrollReveal>

      {/* Kanban-style Status Board */}
      <ScrollReveal className="max-w-7xl mx-auto" delay={300}>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* Upcoming */}
          <div className="backdrop-blur-sm bg-white/80 rounded-2xl p-4 shadow-sm border border-white/40">
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-sm font-bold text-gray-900 flex items-center">
                <span className="w-2 h-2 bg-purple-500 rounded-full mr-2"></span>
                Upcoming
              </h3>
              <span className="text-xs font-semibold text-gray-500">({upcomingMilestones.length})</span>
            </div>
            <div className="space-y-2">
              {upcomingMilestones.map(milestone => (
                <div 
                  key={milestone.id}
                  className="bg-purple-50 rounded-xl p-3 border border-purple-200 hover:shadow-sm transition-all cursor-pointer"
                >
                  <h4 className="font-semibold text-gray-900 text-sm mb-1">{milestone.title}</h4>
                  <p className="text-xs text-gray-600 mb-1.5">{milestone.goal}</p>
                  <div className="flex items-center text-xs text-gray-500">
                    <CalendarIcon className="w-3 h-3 mr-1" />
                    {new Date(milestone.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                  </div>
                </div>
              ))}
              {upcomingMilestones.length === 0 && (
                <p className="text-xs text-gray-500 text-center py-6">No upcoming</p>
              )}
            </div>
          </div>

          {/* In Progress */}
          <div className="backdrop-blur-sm bg-white/80 rounded-2xl p-4 shadow-sm border border-white/40">
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-sm font-bold text-gray-900 flex items-center">
                <span className="w-2 h-2 bg-blue-500 rounded-full mr-2"></span>
                In Progress
              </h3>
              <span className="text-xs font-semibold text-gray-500">({inProgressMilestones.length})</span>
            </div>
            <div className="space-y-2">
              {inProgressMilestones.map(milestone => (
                <div 
                  key={milestone.id}
                  className="bg-blue-50 rounded-xl p-3 border border-blue-200 hover:shadow-sm transition-all cursor-pointer"
                >
                  <h4 className="font-semibold text-gray-900 text-sm mb-1">{milestone.title}</h4>
                  <p className="text-xs text-gray-600 mb-1.5">{milestone.goal}</p>
                  <div className="flex items-center justify-between text-xs mb-1.5">
                    <div className="flex items-center text-gray-500">
                      <CalendarIcon className="w-3 h-3 mr-1" />
                      {new Date(milestone.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                    </div>
                    <span className="font-semibold text-blue-600">{milestone.progress}%</span>
                  </div>
                  <div className="w-full bg-blue-200 rounded-full h-1">
                    <div 
                      className="bg-blue-600 h-1 rounded-full transition-all"
                      style={{ width: `${milestone.progress}%` }}
                    ></div>
                  </div>
                </div>
              ))}
              {inProgressMilestones.length === 0 && (
                <p className="text-xs text-gray-500 text-center py-6">No in progress</p>
              )}
            </div>
          </div>

          {/* Completed */}
          <div className="backdrop-blur-sm bg-white/80 rounded-2xl p-4 shadow-sm border border-white/40">
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-sm font-bold text-gray-900 flex items-center">
                <span className="w-2 h-2 bg-green-500 rounded-full mr-2"></span>
                Completed
              </h3>
              <span className="text-xs font-semibold text-gray-500">({completedMilestones.length})</span>
            </div>
            <div className="space-y-2">
              {completedMilestones.map(milestone => (
                <div 
                  key={milestone.id}
                  className="bg-green-50 rounded-xl p-3 border border-green-200 hover:shadow-sm transition-all cursor-pointer"
                >
                  <h4 className="font-semibold text-gray-900 text-sm mb-1 flex items-center">
                    <CheckCircleIcon className="w-3.5 h-3.5 text-green-600 mr-1.5 flex-shrink-0" />
                    <span className="truncate">{milestone.title}</span>
                  </h4>
                  <p className="text-xs text-gray-600 mb-1.5">{milestone.goal}</p>
                  <div className="flex items-center text-xs text-gray-500">
                    <CalendarIcon className="w-3 h-3 mr-1" />
                    {new Date(milestone.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                  </div>
                </div>
              ))}
              {completedMilestones.length === 0 && (
                <p className="text-xs text-gray-500 text-center py-6">No completed</p>
              )}
            </div>
          </div>
        </div>
      </ScrollReveal>
    </div>
  )
}

export default Milestones
