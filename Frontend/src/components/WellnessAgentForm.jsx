import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { agentAPI } from '../services/api'
import toast from 'react-hot-toast'
import CountUpNumber from './CountUpNumber'
import { useScrollReveal, ScrollReveal } from '../hooks/useScrollReveal'
import { 
  HeartIcon,
  MoonIcon,
  FireIcon,
  SparklesIcon
} from '@heroicons/react/24/outline'

const WellnessAgentForm = ({ onResult }) => {
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [statsRef, statsVisible] = useScrollReveal({ threshold: 0.2 })
  const { register, handleSubmit, formState: { errors } } = useForm()

  const onSubmit = async (data) => {
    setLoading(true)
    try {
      const focusAreas = []
      if (data.focus_fitness) focusAreas.push('Fitness')
      if (data.focus_sleep) focusAreas.push('Sleep')
      if (data.focus_nutrition) focusAreas.push('Nutrition')
      if (data.focus_mental) focusAreas.push('Mental health')

      const userData = {
        focus_areas: focusAreas.join(', '),
        sleep_hours: parseInt(data.sleep_hours),
        active_minutes: parseInt(data.active_minutes),
        screen_time: data.screen_time ? parseInt(data.screen_time) : 0,
        available_time: parseInt(data.available_time),
        additional_notes: data.additional_notes || ''
      }
      
      const response = await agentAPI.wellness({ user_data: userData })
      setResult(response.data)
      onResult(response)
    } catch (error) {
      console.error('Wellness agent error:', error)
      toast.error('Failed to generate wellness plan. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Left: Input Card */}
        <ScrollReveal delay={200}>
          <div className="backdrop-blur-sm bg-white/80 rounded-3xl p-8 shadow-xl border border-white/30">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Tell us about your routine</h2>
            
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
              {/* Focus Areas */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-3">
                  Focus Areas
                </label>
                <div className="grid grid-cols-2 gap-3">
                  <label className="flex items-center p-3 bg-white/50 rounded-xl border border-gray-200 cursor-pointer hover:border-purple-300 transition-colors">
                    <input type="checkbox" {...register('focus_fitness')} className="mr-3 w-4 h-4 text-purple-600" />
                    <FireIcon className="w-5 h-5 mr-2 text-orange-500" />
                    <span className="text-sm font-medium">Fitness</span>
                  </label>
                  <label className="flex items-center p-3 bg-white/50 rounded-xl border border-gray-200 cursor-pointer hover:border-purple-300 transition-colors">
                    <input type="checkbox" {...register('focus_sleep')} className="mr-3 w-4 h-4 text-purple-600" />
                    <MoonIcon className="w-5 h-5 mr-2 text-indigo-500" />
                    <span className="text-sm font-medium">Sleep</span>
                  </label>
                  <label className="flex items-center p-3 bg-white/50 rounded-xl border border-gray-200 cursor-pointer hover:border-purple-300 transition-colors">
                    <input type="checkbox" {...register('focus_nutrition')} className="mr-3 w-4 h-4 text-purple-600" />
                    <HeartIcon className="w-5 h-5 mr-2 text-green-500" />
                    <span className="text-sm font-medium">Nutrition</span>
                  </label>
                  <label className="flex items-center p-3 bg-white/50 rounded-xl border border-gray-200 cursor-pointer hover:border-purple-300 transition-colors">
                    <input type="checkbox" {...register('focus_mental')} className="mr-3 w-4 h-4 text-purple-600" />
                    <SparklesIcon className="w-5 h-5 mr-2 text-purple-500" />
                    <span className="text-sm font-medium">Mental Health</span>
                  </label>
                </div>
              </div>

              {/* Sleep Hours */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Average Sleep per Night (hours)
                </label>
                <input
                  type="text"
                  {...register('sleep_hours', { required: 'Sleep hours required' })}
                  className="w-full px-4 py-3 bg-white/50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500"
                  placeholder="e.g., 7"
                />
                <p className="text-xs text-gray-500 mt-1">Rough estimates are fine</p>
                {errors.sleep_hours && <p className="text-sm text-red-600 mt-1">{errors.sleep_hours.message}</p>}
              </div>

              {/* Active Minutes */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Active Minutes per Day
                </label>
                <input
                  type="text"
                  {...register('active_minutes', { required: 'Active minutes required' })}
                  className="w-full px-4 py-3 bg-white/50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500"
                  placeholder="e.g., 30"
                />
                <p className="text-xs text-gray-500 mt-1">Include walking, exercise, sports</p>
                {errors.active_minutes && <p className="text-sm text-red-600 mt-1">{errors.active_minutes.message}</p>}
              </div>

              {/* Screen Time */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Screen Time per Day (hours, optional)
                </label>
                <input
                  type="text"
                  {...register('screen_time')}
                  className="w-full px-4 py-3 bg-white/50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500"
                  placeholder="e.g., 8"
                />
              </div>

              {/* Available Time */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Time Available for Wellness per Day (minutes)
                </label>
                <input
                  type="text"
                  {...register('available_time', { required: 'Available time required' })}
                  className="w-full px-4 py-3 bg-white/50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500"
                  placeholder="e.g., 60"
                />
                {errors.available_time && <p className="text-sm text-red-600 mt-1">{errors.available_time.message}</p>}
              </div>

              {/* Additional Notes */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Anything else we should know?
                </label>
                <textarea
                  {...register('additional_notes')}
                  rows="3"
                  className="w-full px-4 py-3 bg-white/50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500"
                  placeholder="Health conditions, preferences, goals..."
                />
              </div>

              {/* Submit Button */}
              <button
                type="submit"
                disabled={loading}
                className="w-full px-8 py-4 bg-gradient-to-r from-purple-600 to-pink-600 text-white font-semibold rounded-xl hover:from-purple-700 hover:to-pink-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 shadow-lg hover:shadow-xl transform hover:scale-105"
              >
                {loading ? (
                  <div className="flex items-center justify-center">
                    <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
                    Generating plan...
                  </div>
                ) : (
                  'Generate wellness plan'
                )}
              </button>
            </form>
          </div>
        </ScrollReveal>

        {/* Right: Results Card */}
        <ScrollReveal delay={400}>
          <div className="backdrop-blur-sm bg-white/80 rounded-3xl p-8 shadow-xl border border-white/30">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Your AI Wellness Plan</h2>
            
            {!result ? (
              <div className="text-center py-12">
                <div className="w-16 h-16 bg-gradient-to-br from-purple-100 to-pink-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <HeartIcon className="w-8 h-8 text-purple-600" />
                </div>
                <p className="text-gray-600">Run the Wellness Coach to see your personalized plan.</p>
              </div>
            ) : (
              <div className="space-y-6">
                {/* Wellness Snapshot */}
                <div ref={statsRef} className="bg-gradient-to-r from-purple-50 to-pink-50 rounded-2xl p-6 border border-purple-200">
                  <h3 className="text-lg font-bold text-gray-900 mb-4">Wellness Snapshot</h3>
                  <div className="grid grid-cols-3 gap-4">
                    <div className="text-center">
                      <div className="text-3xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">
                        <CountUpNumber endValue={5} durationMs={1000} startOnVisible={statsVisible} />
                      </div>
                      <p className="text-xs text-gray-600 mt-1">Active Days</p>
                    </div>
                    <div className="text-center">
                      <div className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-cyan-600 bg-clip-text text-transparent">
                        <CountUpNumber endValue={result.user_data?.sleep_hours || 7} durationMs={1000} startOnVisible={statsVisible} />
                      </div>
                      <p className="text-xs text-gray-600 mt-1">Avg Sleep</p>
                    </div>
                    <div className="text-center">
                      <div className="text-3xl font-bold bg-gradient-to-r from-green-600 to-emerald-600 bg-clip-text text-transparent">
                        <CountUpNumber endValue={85} durationMs={1000} startOnVisible={statsVisible} />
                      </div>
                      <p className="text-xs text-gray-600 mt-1">Score</p>
                    </div>
                  </div>
                </div>

                {/* Daily Routine */}
                <div>
                  <h3 className="text-lg font-bold text-gray-900 mb-3">Daily Routine</h3>
                  <div className="space-y-3">
                    <div className="bg-orange-50 rounded-xl p-4 border border-orange-200">
                      <h4 className="font-semibold text-orange-900 mb-2 flex items-center">
                        <span className="w-2 h-2 bg-orange-500 rounded-full mr-2"></span>
                        Morning
                      </h4>
                      <ul className="text-sm text-gray-700 space-y-1 ml-4">
                        <li>• 15-min stretching or yoga</li>
                        <li>• Healthy breakfast with protein</li>
                        <li>• 10-min mindfulness practice</li>
                      </ul>
                    </div>
                    <div className="bg-blue-50 rounded-xl p-4 border border-blue-200">
                      <h4 className="font-semibold text-blue-900 mb-2 flex items-center">
                        <span className="w-2 h-2 bg-blue-500 rounded-full mr-2"></span>
                        Daytime
                      </h4>
                      <ul className="text-sm text-gray-700 space-y-1 ml-4">
                        <li>• 30-min workout or brisk walk</li>
                        <li>• Balanced lunch with vegetables</li>
                        <li>• Short breaks every 90 minutes</li>
                      </ul>
                    </div>
                    <div className="bg-purple-50 rounded-xl p-4 border border-purple-200">
                      <h4 className="font-semibold text-purple-900 mb-2 flex items-center">
                        <span className="w-2 h-2 bg-purple-500 rounded-full mr-2"></span>
                        Evening
                      </h4>
                      <ul className="text-sm text-gray-700 space-y-1 ml-4">
                        <li>• Light dinner 3 hours before bed</li>
                        <li>• Screen-free time 1 hour before sleep</li>
                        <li>• Relaxation routine (reading, meditation)</li>
                      </ul>
                    </div>
                  </div>
                </div>

                {/* Weekly Structure */}
                <div>
                  <h3 className="text-lg font-bold text-gray-900 mb-3">Weekly Structure</h3>
                  <div className="bg-gradient-to-r from-green-50 to-emerald-50 rounded-xl p-4 border border-green-200">
                    <ul className="text-sm text-gray-700 space-y-2">
                      <li className="flex items-start">
                        <span className="text-green-600 mr-2">✓</span>
                        3 strength training sessions (Mon, Wed, Fri)
                      </li>
                      <li className="flex items-start">
                        <span className="text-green-600 mr-2">✓</span>
                        2 cardio sessions (Tue, Thu)
                      </li>
                      <li className="flex items-start">
                        <span className="text-green-600 mr-2">✓</span>
                        2 active recovery days (Sat, Sun)
                      </li>
                      <li className="flex items-start">
                        <span className="text-green-600 mr-2">✓</span>
                        Daily 7-8 hours sleep schedule
                      </li>
                      <li className="flex items-start">
                        <span className="text-green-600 mr-2">✓</span>
                        Weekly meal prep on Sunday
                      </li>
                    </ul>
                  </div>
                </div>

                {/* Coach Tips */}
                <div>
                  <h3 className="text-lg font-bold text-gray-900 mb-3">Coach Tips</h3>
                  <div className="space-y-2">
                    <div className="flex items-start p-3 bg-purple-50 rounded-xl border border-purple-200">
                      <SparklesIcon className="w-5 h-5 text-purple-600 mr-3 mt-0.5 flex-shrink-0" />
                      <p className="text-sm text-gray-700">Start small: Focus on one habit at a time for sustainable change</p>
                    </div>
                    <div className="flex items-start p-3 bg-pink-50 rounded-xl border border-pink-200">
                      <SparklesIcon className="w-5 h-5 text-pink-600 mr-3 mt-0.5 flex-shrink-0" />
                      <p className="text-sm text-gray-700">Consistency beats intensity: Regular moderate activity is better than sporadic intense workouts</p>
                    </div>
                    <div className="flex items-start p-3 bg-indigo-50 rounded-xl border border-indigo-200">
                      <SparklesIcon className="w-5 h-5 text-indigo-600 mr-3 mt-0.5 flex-shrink-0" />
                      <p className="text-sm text-gray-700">Track progress: Use a journal or app to monitor your wellness journey</p>
                    </div>
                  </div>
                </div>

                {/* AI Response */}
                {result.response && (
                  <div className="bg-gray-50 rounded-xl p-4 border border-gray-200">
                    <h3 className="text-sm font-bold text-gray-900 mb-2">AI Suggestions</h3>
                    <p className="text-sm text-gray-700 whitespace-pre-wrap">{result.response}</p>
                  </div>
                )}
              </div>
            )}
          </div>
        </ScrollReveal>
      </div>
    </div>
  )
}

export default WellnessAgentForm
