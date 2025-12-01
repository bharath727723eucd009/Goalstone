import { useState, useEffect, useRef } from 'react'
import { Link, useNavigate, useLocation } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { useAuth } from '../hooks/useAuth'
import { ScrollReveal, StaggeredReveal } from '../hooks/useScrollReveal'
import CountUpNumber from '../components/CountUpNumber'
import Header from '../components/Header'
import Footer from '../components/Footer'
import { 
  SparklesIcon, 
  RocketLaunchIcon, 
  ChartBarIcon,
  EyeIcon,
  EyeSlashIcon,
  ArrowRightIcon,
  CheckIcon
} from '@heroicons/react/24/outline'

const Home = () => {
  const [showPassword, setShowPassword] = useState(false)
  const [showLoginPrompt, setShowLoginPrompt] = useState(false)
  const [selectedFeature, setSelectedFeature] = useState('')
  const [loginError, setLoginError] = useState('')
  const { login, loading, isAuthenticated } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()
  const emailRef = useRef(null)
  const { register, handleSubmit, formState: { errors }, setFocus } = useForm()

  useEffect(() => {
    // Only show login prompt if explicitly redirected from a protected route
    if (location.state?.requiresLogin && location.state?.fromProtectedRoute) {
      setShowLoginPrompt(true)
      setSelectedFeature('Dashboard')
      setTimeout(() => {
        setFocus('email')
      }, 100)
    }
    
    // Clear the state after handling to prevent modal from showing on refresh
    if (location.state?.requiresLogin) {
      window.history.replaceState({}, document.title)
    }
  }, [location.state, setFocus])



  const onSubmit = async (data) => {
    try {
      setLoginError('')
      await login(data)
      if (showLoginPrompt) {
        setShowLoginPrompt(false)
        const feature = features.find(f => f.title === selectedFeature)
        if (feature) {
          navigate(feature.route)
        } else if (selectedFeature === 'Dashboard') {
          navigate('/dashboard')
        }
      } else {
        navigate('/dashboard')
      }
    } catch (error) {
      const errorMessage = error.response?.data?.detail || 'Login failed'
      setLoginError(errorMessage)
    }
  }

  const features = [
    {
      icon: SparklesIcon,
      title: 'AI-Powered Insights',
      description: 'Get personalized recommendations from our advanced AI agents',
      route: '/agents'
    },
    {
      icon: RocketLaunchIcon,
      title: 'Goal Acceleration',
      description: 'Achieve your dreams faster with structured milestone tracking',
      route: '/milestones'
    },
    {
      icon: ChartBarIcon,
      title: 'Progress Analytics',
      description: 'Visualize your journey with detailed progress reports',
      route: '/progress'
    }
  ]

  const handleFeatureClick = (feature) => {
    if (isAuthenticated) {
      navigate(feature.route)
    } else {
      setSelectedFeature(feature.title)
      setShowLoginPrompt(true)
      setLoginError('')
      setTimeout(() => {
        setFocus('email')
      }, 100)
    }
  }

  const handleDashboardClick = (e) => {
    if (!isAuthenticated) {
      e.preventDefault()
      setSelectedFeature('Dashboard')
      setShowLoginPrompt(true)
      setLoginError('')
      setTimeout(() => {
        setFocus('email')
      }, 100)
    }
  }

  const steps = [
    { number: '01', title: 'Set Your Goals', description: 'Define what you want to achieve in life' },
    { number: '02', title: 'Get AI Guidance', description: 'Receive personalized strategies from our AI agents' },
    { number: '03', title: 'Track Progress', description: 'Monitor your journey and celebrate milestones' }
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-pink-50">
      <Header />

      {/* Hero Section */}
      <section className="relative overflow-hidden pt-24 pb-8 lg:pt-32 lg:pb-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            {/* Left Content */}
            <div className="space-y-8">
              <ScrollReveal delay={100}>
                <div className="space-y-6">
                  <h1 className="text-5xl lg:text-6xl font-bold leading-tight">
                    <span className="text-gray-900">Transform Your</span>
                    <br />
                    <span className="bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
                      Dreams Into Reality
                    </span>
                  </h1>
                  <p className="text-xl text-gray-600 leading-relaxed max-w-lg">
                    Harness the power of AI to set, track, and achieve your life goals. 
                    Get personalized guidance for career, finance, wellness, and learning.
                  </p>
                </div>
              </ScrollReveal>
              
              <ScrollReveal delay={300}>
                <div className="flex flex-col sm:flex-row gap-4">
                  <Link
                    to="/dashboard"
                    className="inline-flex items-center justify-center px-8 py-4 bg-gradient-to-r from-purple-600 to-pink-600 text-white font-semibold rounded-2xl hover:from-purple-700 hover:to-pink-700 transform hover:scale-105 transition-all duration-200 shadow-lg animate-float"
                  >
                    Get Started Free
                    <ArrowRightIcon className="ml-2 w-5 h-5" />
                  </Link>
                  <Link
                    to="/dashboard"
                    onClick={handleDashboardClick}
                    className="inline-flex items-center justify-center px-8 py-4 bg-white text-gray-700 font-semibold rounded-2xl border-2 border-gray-200 hover:border-purple-300 hover:text-purple-600 transition-all duration-200"
                  >
                    Upgrade to Pro
                  </Link>
                </div>
              </ScrollReveal>
            </div>

            {/* Right Login Panel */}
            <ScrollReveal delay={200}>
              <div className="lg:ml-8">
                <div className="bg-white/70 backdrop-blur-lg rounded-3xl p-8 shadow-2xl border border-white/20 min-h-[480px] flex flex-col">
                <div className="text-center mb-8">
                  <h2 className="text-2xl font-bold text-gray-900 mb-2">Welcome</h2>
                  <p className="text-gray-600">Sign in to continue your journey</p>
                </div>

                <form onSubmit={handleSubmit(onSubmit)} className="space-y-6 flex-1 flex flex-col">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Email Address
                    </label>
                    <input
                      {...register('email', { required: 'Email is required' })}
                      type="email"
                      className="w-full px-4 py-3 bg-white/50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200"
                      placeholder="Enter your email"
                    />
                    <div className="h-6 mt-1">
                      {errors.email && (
                        <p className="text-sm text-red-600 animate-fade-in">{errors.email.message}</p>
                      )}
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Password
                    </label>
                    <div className="relative">
                      <input
                        {...register('password', { required: 'Password is required' })}
                        type={showPassword ? 'text' : 'password'}
                        className="w-full px-4 py-3 bg-white/50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200 pr-12"
                        placeholder="Enter your password"
                      />
                      <button
                        type="button"
                        onClick={() => setShowPassword(!showPassword)}
                        className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
                      >
                        {showPassword ? (
                          <EyeSlashIcon className="w-5 h-5" />
                        ) : (
                          <EyeIcon className="w-5 h-5" />
                        )}
                      </button>
                    </div>
                    <div className="h-6 mt-1">
                      {errors.password && (
                        <p className="text-sm text-red-600 animate-fade-in">{errors.password.message}</p>
                      )}
                    </div>

                  {loginError && (
                    <div className="bg-red-50 border border-red-200 rounded-xl p-3">
                      <p className="text-sm text-red-600">{loginError}</p>
                    </div>
                  )}
                  </div>

                  <div className="mt-auto space-y-4">
                    <button
                      type="submit"
                      disabled={loading}
                      className="w-full bg-gradient-to-r from-purple-600 to-pink-600 text-white font-semibold py-3 rounded-xl hover:from-purple-700 hover:to-pink-700 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
                    >
                      {loading ? (
                        <div className="flex items-center justify-center">
                          <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
                          Signing in...
                        </div>
                      ) : (
                        'Sign In'
                      )}
                    </button>

                    <div className="text-center">
                      <p className="text-sm text-gray-600">
                        Don't have an account?{' '}
                        <Link to="/register" className="text-purple-600 hover:text-purple-700 font-medium">
                          Register
                        </Link>
                      </p>
                    </div>
                  </div>
                </form>
                </div>
              </div>
            </ScrollReveal>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-white/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <ScrollReveal>
            <div className="text-center mb-16">
              <h2 className="text-4xl font-bold text-gray-900 mb-4">
                Powered by Advanced AI
              </h2>
              <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                Our intelligent agents provide personalized guidance across all areas of your life
              </p>
            </div>
          </ScrollReveal>

          <StaggeredReveal staggerDelay={120} className="grid md:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <div
                key={index}
                onClick={() => handleFeatureClick(feature)}
                className="bg-white/70 backdrop-blur-sm rounded-2xl p-8 shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-2 border border-white/20 cursor-pointer group"
              >
                <div className="w-12 h-12 bg-gradient-to-r from-purple-100 to-pink-100 rounded-xl flex items-center justify-center mb-6 group-hover:from-purple-200 group-hover:to-pink-200 transition-all duration-300">
                  <feature.icon className="w-6 h-6 text-purple-600" />
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-4 group-hover:text-purple-600 transition-colors duration-300">{feature.title}</h3>
                <p className="text-gray-600 leading-relaxed">{feature.description}</p>
                <div className="mt-4 text-purple-600 font-medium opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                  Click to explore →
                </div>
              </div>
            ))}
          </StaggeredReveal>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <ScrollReveal>
            <div className="text-center mb-16">
              <h2 className="text-4xl font-bold text-gray-900 mb-4">
                How It Works
              </h2>
              <p className="text-xl text-gray-600">
                Three simple steps to transform your life
              </p>
            </div>
          </ScrollReveal>

          <div className="grid md:grid-cols-3 gap-8">
            {steps.map((step, index) => {
              const directions = ['left', 'up', 'right'];
              return (
                <ScrollReveal key={index} delay={index * 100 + 150} direction={directions[index]} type="fade">
                  <div className="text-center">
                    <ScrollReveal delay={index * 100 + 300} type="scale">
                      <div className="w-16 h-16 bg-gradient-to-r from-purple-600 to-pink-600 rounded-full flex items-center justify-center text-white font-bold text-xl mx-auto mb-6">
                        {step.number}
                      </div>
                    </ScrollReveal>
                    <h3 className="text-xl font-semibold text-gray-900 mb-4">{step.title}</h3>
                    <p className="text-gray-600 leading-relaxed">{step.description}</p>
                  </div>
                </ScrollReveal>
              );
            })}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-purple-600 to-pink-600">
        <ScrollReveal>
          <div className="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
            <h2 className="text-4xl font-bold text-white mb-6">
              Ready to Achieve Your Dreams?
            </h2>
            <p className="text-xl text-purple-100 mb-8">
              Join thousands of users who are already transforming their lives with AI guidance
            </p>
            <Link
              to="/dashboard"
              onClick={handleDashboardClick}
              className="inline-flex items-center px-8 py-4 bg-white text-purple-600 font-semibold rounded-2xl hover:bg-gray-50 transform hover:scale-105 transition-all duration-200 shadow-lg animate-float"
            >
              Start Your Journey Today
              <ArrowRightIcon className="ml-2 w-5 h-5" />
            </Link>
          </div>
        </ScrollReveal>
      </section>

      {/* Login Prompt Modal */}
      {showLoginPrompt && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm">
          <div className="bg-white rounded-2xl p-8 max-w-md w-full mx-4 shadow-2xl">
            <div className="text-center mb-6">
              <h3 className="text-2xl font-bold text-gray-900 mb-2">Login Required</h3>
              <p className="text-gray-600">
                Please sign in to access <span className="font-semibold text-purple-600">{selectedFeature}</span>
              </p>
            </div>

            {loginError && (
              <div className="bg-red-50 border border-red-200 rounded-xl p-3 mb-4">
                <p className="text-sm text-red-600">{loginError}</p>
              </div>
            )}
            
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
              <div>
                <input
                  {...register('email', { required: 'Email is required' })}
                  type="email"
                  className="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500"
                  placeholder="Enter your email"
                />
                {errors.email && (
                  <p className="text-sm text-red-600 mt-1">{errors.email.message}</p>
                )}
              </div>
              
              <div>
                <input
                  {...register('password', { required: 'Password is required' })}
                  type="password"
                  className="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500"
                  placeholder="Enter your password"
                />
                {errors.password && (
                  <p className="text-sm text-red-600 mt-1">{errors.password.message}</p>
                )}
              </div>
              
              <div className="flex space-x-3 pt-4">
                <button
                  type="button"
                  onClick={() => setShowLoginPrompt(false)}
                  className="flex-1 px-4 py-3 border border-gray-200 text-gray-700 rounded-xl hover:bg-gray-50 transition-colors duration-200"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={loading}
                  className="flex-1 px-4 py-3 bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-xl hover:from-purple-700 hover:to-pink-700 disabled:opacity-50 transition-all duration-200"
                >
                  {loading ? 'Signing in...' : 'Sign In'}
                </button>
              </div>
            </form>
            
            <div className="text-center mt-4">
              <p className="text-sm text-gray-600">
                Don't have an account?{' '}
                <Link 
                  to="/register" 
                  className="text-purple-600 hover:text-purple-700 font-medium"
                  onClick={() => setShowLoginPrompt(false)}
                >
                  Sign up
                </Link>
              </p>
            </div>
          </div>
        </div>
      )}
      
      <Footer />
    </div>
  )
}

export default Home