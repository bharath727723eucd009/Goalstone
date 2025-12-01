import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { dataAPI } from '../services/api'
import CountUpNumber from '../components/CountUpNumber'
import { useScrollReveal, ScrollReveal, StaggeredReveal } from '../hooks/useScrollReveal'
import { 
  PlusIcon,
  ChartBarIcon,
  TrophyIcon,
  ClockIcon,
  SparklesIcon,
  RocketLaunchIcon
} from '@heroicons/react/24/outline'

const Dashboard = () => {
  const [stats, setStats] = useState({
    total: 0,
    completed: 0,
    in_progress: 0,
    overdue: 0
  })
  const [loading, setLoading] = useState(true)
  const [statsRef, statsVisible] = useScrollReveal({ threshold: 0.2 })

  const fetchGoalsData = async () => {
    try {
      const data = await dataAPI.getGoalsSummary()
      setStats(data)
    } catch (error) {
      console.error('Failed to fetch goals summary:', error)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchGoalsData()
  }, [])
  const [timeFilter, setTimeFilter] = useState('7days')
  const [filterKey, setFilterKey] = useState(0)

  const completionRate = stats.total > 0 ? Math.round((stats.completed / stats.total) * 100) : 0

  const getStatsByFilter = () => {
    if (timeFilter === '7days') return { total: 12, in_progress: 8, completed: 4 }
    if (timeFilter === '30days') return { total: 45, in_progress: 28, completed: 17 }
    return { total: 156, in_progress: 89, completed: 67 }
  }

  const filteredStats = getStatsByFilter()

  const statCards = [
    {
      title: 'Total Goals',
      value: filteredStats.total,
      icon: ChartBarIcon,
      iconBg: 'bg-purple-50',
      iconColor: 'text-purple-500'
    },
    {
      title: 'Completed',
      value: filteredStats.completed,
      icon: TrophyIcon,
      iconBg: 'bg-green-50',
      iconColor: 'text-green-500'
    },
    {
      title: 'In Progress',
      value: filteredStats.in_progress,
      icon: SparklesIcon,
      iconBg: 'bg-blue-50',
      iconColor: 'text-blue-500'
    },
    {
      title: 'Overdue',
      value: stats.overdue,
      icon: ClockIcon,
      iconBg: 'bg-red-50',
      iconColor: 'text-red-500'
    }
  ]

  const recentActivity = [
    {
      id: 1,
      title: 'Completed React Mastery Course',
      description: 'Advanced React patterns and hooks',
      time: '2 hours ago',
      type: 'achievement',
      icon: SparklesIcon,
      color: 'text-purple-500 bg-purple-50'
    },
    {
      id: 2,
      title: 'Started ML Engineering Path',
      description: 'Machine Learning specialization track',
      time: '1 day ago',
      type: 'started',
      icon: RocketLaunchIcon,
      color: 'text-pink-500 bg-pink-50'
    },
    {
      id: 3,
      title: 'Fitness Goal Milestone',
      description: 'Reached 75% of weight loss target',
      time: '3 days ago',
      type: 'progress',
      icon: TrophyIcon,
      color: 'text-purple-500 bg-purple-50'
    }
  ]

  const quickActions = [
    {
      title: 'Career Agent',
      description: 'Get personalized career guidance',
      icon: '💼',
      href: '/agents?type=career',
      color: 'bg-gradient-to-r from-indigo-500 to-purple-600'
    },
    {
      title: 'Finance Planner',
      description: 'Optimize your financial strategy',
      icon: '💰',
      href: '/agents?type=finance',
      color: 'bg-gradient-to-r from-green-500 to-teal-600'
    },
    {
      title: 'Wellness Coach',
      description: 'Improve your health & fitness',
      icon: '🏃‍♂️',
      href: '/agents?type=wellness',
      color: 'bg-gradient-to-r from-orange-500 to-red-600'
    },
    {
      title: 'Learning Path',
      description: 'Discover new skills to master',
      icon: '🎓',
      href: '/agents?type=learning',
      color: 'bg-gradient-to-r from-blue-500 to-cyan-600'
    }
  ]

  return (
    <div className="px-4 sm:px-6 lg:px-8 py-8">
      {/* Hero Section */}
      <ScrollReveal className="max-w-7xl mx-auto mb-8">
        <div className="backdrop-blur-sm bg-white/70 rounded-3xl p-8 shadow-xl border border-white/20">
          <div className="text-center">
            <h1 className="text-4xl font-bold tracking-tight sm:text-5xl md:text-6xl">
              <span className="block text-gray-900">Your AI-Powered</span>
              <span className="block bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
                Life Goals Dashboard
              </span>
            </h1>
            <p className="mx-auto mt-6 max-w-2xl text-lg text-gray-600">
              Track progress, get AI insights, and achieve your dreams with personalized guidance
            </p>
            <div className="mt-8 flex flex-col sm:flex-row justify-center gap-4">
              <Link
                to="/agents"
                className="inline-flex items-center justify-center rounded-full bg-gradient-to-r from-purple-600 to-pink-600 px-6 py-3 text-base font-semibold text-white shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200"
              >
                <PlusIcon className="mr-2 h-5 w-5" />
                Create New Goal
              </Link>
              <button className="inline-flex items-center justify-center rounded-full backdrop-blur-sm bg-white/50 border border-white/20 px-6 py-3 text-base font-semibold text-gray-700 shadow-lg hover:bg-white/70 transform hover:scale-105 transition-all duration-200">
                <ChartBarIcon className="mr-2 h-5 w-5" />
                View Analytics
              </button>
            </div>
          </div>
        </div>
      </ScrollReveal>

      {/* Stats Grid */}
      <ScrollReveal className="max-w-7xl mx-auto mb-8" delay={200}>
        <div ref={statsRef} className="backdrop-blur-sm bg-white/70 rounded-3xl p-8 shadow-xl border border-white/20">
          <h2 className="text-3xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent mb-6">Your Progress Overview</h2>
          <div className="flex flex-wrap gap-3 mb-8">
            {['7days', '30days', 'all'].map((filter) => (
              <button
                key={filter}
                onClick={() => { setTimeFilter(filter); setFilterKey(prev => prev + 1) }}
                className={`px-4 py-2 rounded-full text-sm font-medium transition-all duration-200 ${
                  timeFilter === filter
                    ? 'bg-gradient-to-r from-purple-600 to-pink-600 text-white shadow-lg'
                    : 'backdrop-blur-sm bg-white/50 text-gray-600 hover:bg-white/70 border border-white/20'
                }`}
              >
                {filter === '7days' ? 'Last 7 days' : filter === '30days' ? 'Last 30 days' : 'All time'}
              </button>
            ))}
          </div>

          <StaggeredReveal staggerDelay={150} className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
            {statCards.map((stat, index) => (
              <div
                key={stat.title}
                className="relative overflow-hidden rounded-3xl backdrop-blur-sm bg-white/70 border border-white/20 p-6 shadow-xl hover:shadow-2xl hover:bg-white/80 transition-all duration-300 transform hover:scale-105"
              >
                <div className="flex items-center justify-between">
                  <div className={`rounded-xl p-3 ${stat.iconBg}`}>
                    <stat.icon className={`h-6 w-6 ${stat.iconColor}`} />
                  </div>
                  {loading && (
                    <div className="animate-pulse bg-gray-200 rounded-full h-6 w-12"></div>
                  )}
                </div>
                <div className="mt-4">
                  <p className="text-sm font-medium text-gray-600">{stat.title}</p>
                  <p className="text-3xl font-bold text-gray-900">
                    <CountUpNumber 
                      key={filterKey}
                      endValue={stat.value} 
                      durationMs={900} 
                      startOnVisible={true}
                    />
                  </p>
                </div>
              </div>
            ))}
          </StaggeredReveal>
        </div>
      </ScrollReveal>

      {/* Quick Actions */}
      <ScrollReveal className="max-w-7xl mx-auto mb-8" delay={400}>
        <div className="backdrop-blur-sm bg-white/70 rounded-3xl p-8 shadow-xl border border-white/20">
          <h2 className="text-3xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent mb-8">AI Agents Ready to Help</h2>
          <StaggeredReveal staggerDelay={150} className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4 auto-rows-fr">
            {quickActions.map((action, index) => (
              <Link
                key={action.title}
                to={action.href}
                className="group relative overflow-hidden rounded-3xl p-6 text-white shadow-xl hover:shadow-2xl transition-all duration-300 transform hover:scale-105 h-full flex flex-col"
              >
                <div className="absolute inset-0 bg-gradient-to-r from-purple-400 to-pink-400 group-hover:from-purple-300 group-hover:to-pink-300 transition-all duration-300"></div>
                <div className="relative flex flex-col h-full">
                  <div className="w-12 h-12 bg-white/20 rounded-xl flex items-center justify-center mb-4 text-2xl">
                    {action.icon}
                  </div>
                  <h3 className="text-xl font-bold mb-2">{action.title}</h3>
                  <p className="text-white/90 text-sm flex-1">{action.description}</p>
                  <div className="mt-4 inline-flex items-center text-sm font-semibold">
                    Get Started
                    <svg className="ml-2 h-4 w-4 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                    </svg>
                  </div>
                </div>
              </Link>
            ))}
          </StaggeredReveal>
        </div>
      </ScrollReveal>

      {/* Recent Activity */}
      <ScrollReveal className="max-w-7xl mx-auto mb-8" delay={600}>
        <div className="backdrop-blur-sm bg-white/70 rounded-3xl p-8 shadow-xl border border-white/20">
          <div className="flex items-center justify-between mb-8">
            <h2 className="text-3xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">Recent Activity</h2>
            <Link to="/progress" className="text-purple-600 hover:text-purple-700 font-semibold text-sm">
              View All Activity →
            </Link>
          </div>
          <StaggeredReveal staggerDelay={100} className="space-y-4">
            {recentActivity.map((activity, index) => (
              <div
                key={activity.id}
                className="backdrop-blur-sm bg-white/70 rounded-3xl border border-white/20 p-6 shadow-lg hover:shadow-xl hover:bg-white/80 transition-all duration-300 transform hover:scale-[1.02]"
              >
                <div className="flex items-start space-x-4">
                  <div className={`rounded-xl p-3 ${activity.color}`}>
                    <activity.icon className="h-6 w-6" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <h3 className="text-lg font-semibold text-gray-900">{activity.title}</h3>
                    <p className="text-gray-600 mt-1 text-sm">{activity.description}</p>
                    <div className="flex items-center mt-2 text-xs text-gray-500">
                      <ClockIcon className="h-4 w-4 mr-1" />
                      {activity.time}
                    </div>
                  </div>
                  <button className="text-purple-600 hover:text-purple-700 font-medium text-sm transition-colors duration-200">
                    View Details
                  </button>
                </div>
              </div>
            ))}
          </StaggeredReveal>
        </div>
      </ScrollReveal>

      {/* Motivational Footer */}
      <ScrollReveal className="max-w-7xl mx-auto" delay={800}>
        <div className="relative overflow-hidden rounded-3xl bg-gradient-to-r from-purple-600 via-pink-600 to-indigo-600 p-8 text-center text-white shadow-xl">
          <div className="absolute inset-0 bg-black/20"></div>
          <div className="relative">
            <h2 className="text-3xl font-bold mb-4">Ready to Achieve More?</h2>
            <p className="text-xl mb-8 opacity-90">
              Let our AI agents guide you to success in every area of your life
            </p>
            <Link
              to="/agents"
              className="inline-flex items-center rounded-full bg-white px-8 py-4 text-lg font-semibold text-purple-600 shadow-lg hover:bg-gray-50 transform hover:scale-105 transition-all duration-200 animate-float"
            >
              <SparklesIcon className="mr-2 h-6 w-6" />
              Start Your Journey
            </Link>
          </div>
        </div>
      </ScrollReveal>
    </div>
  )
}

export default Dashboard