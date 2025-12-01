import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { agentAPI } from '../services/api'
import toast from 'react-hot-toast'
import { 
  CheckCircleIcon,
  ClockIcon,
  LinkIcon
} from '@heroicons/react/24/outline'

const RoadmapTaskCard = ({ task, isCompleted, onToggle, colorScheme }) => (
  <div className="roadmap-task-card h-full min-h-[180px] bg-white rounded-xl p-4 border border-gray-100 shadow-sm hover:shadow-md transition-shadow flex flex-col justify-between">
    <div className="flex items-start space-x-3 mb-3">
      <button
        onClick={() => onToggle(task.id)}
        className={`mt-1 w-5 h-5 rounded border-2 flex items-center justify-center transition-colors ${
          isCompleted
            ? colorScheme === 'purple' ? 'bg-purple-500 border-purple-500' :
              colorScheme === 'pink' ? 'bg-pink-500 border-pink-500' :
              'bg-indigo-500 border-indigo-500'
            : `border-gray-300 hover:border-${colorScheme}-400`
        }`}
      >
        {isCompleted && (
          <svg className="w-3 h-3 text-white" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
          </svg>
        )}
      </button>
      <div className="flex-1">
        <h5 className={`font-semibold mb-2 ${
          isCompleted
            ? 'line-through text-gray-500'
            : 'text-gray-900'
        }`}>{task.title}</h5>
        <p className={`text-sm leading-relaxed ${
          isCompleted
            ? 'text-gray-400'
            : 'text-gray-600'
        }`}>{task.explanation}</p>
      </div>
    </div>
    <div className="mt-auto">
      <div className={`flex items-center text-xs text-${colorScheme}-600 bg-${colorScheme}-50 px-2 py-1 rounded-full w-fit`}>
        <ClockIcon className="w-3 h-3 mr-1" />
        {task.timeframe}
      </div>
    </div>
  </div>
)

const CareerAgentForm = ({ onResult }) => {
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [completedTasks, setCompletedTasks] = useState(new Set())
  const [savingPlan, setSavingPlan] = useState(false)
  const [updatingPlan, setUpdatingPlan] = useState(false)
  const [loadingProgress, setLoadingProgress] = useState(false)
  const [savingProgress, setSavingProgress] = useState(false)
  const [hasUnsavedChanges, setHasUnsavedChanges] = useState(false)
  const [completedCourses, setCompletedCourses] = useState(new Set())
  const [showBlast, setShowBlast] = useState(false)
  
  const { register, handleSubmit, watch, formState: { errors } } = useForm()
  const taskType = watch('task_type')

  const onSubmit = async (data) => {
    setLoading(true)
    try {
      let userData = {}
      
      if (data.task_type === 'skill_development') {
        userData = {
          skill_level: data.skill_level,
          target_area: data.target_area,
          weekly_hours: data.weekly_hours,
          time_horizon: data.time_horizon,
          technologies: data.technologies || '',
          skills: data.technologies || data.target_area || '',
          experience_years: data.skill_level === 'Beginner' ? 0 : data.skill_level === 'Intermediate' ? 2 : 5,
          location: 'Remote',
          goal: `Learn ${data.target_area} in ${data.time_horizon} with ${data.weekly_hours} weekly commitment`
        }
      } else {
        userData = {
          skills: data.skills,
          experience_years: parseInt(data.experience_years),
          location: data.location,
          goal: data.goal || ''
        }
      }
      
      const response = await agentAPI.career({
        user_data: userData,
        task_type: data.task_type,
        parameters: {}
      })
      
      setResult(response.data)
      onResult(response)
      
      // Load existing progress
      await loadProgress()
      await loadCourseProgress()
    } catch (error) {
      console.error('Career agent error:', error)
      if (error.response?.status === 401) {
        toast.error('Please login to use the Career Agent')
      } else {
        toast.error('Failed to run Career Agent. Please try again.')
      }
    } finally {
      setLoading(false)
    }
  }

  const loadProgress = async () => {
    setLoadingProgress(true)
    try {
      const response = await agentAPI.getRoadmapProgress()
      setCompletedTasks(new Set(response.completed_task_ids))
    } catch (error) {
      console.error('Failed to load progress:', error)
    } finally {
      setLoadingProgress(false)
    }
  }

  const loadCourseProgress = async () => {
    try {
      const response = await agentAPI.getCourseProgress()
      setCompletedCourses(new Set(response.completed_course_ids))
    } catch (error) {
      console.error('Failed to load course progress:', error)
    }
  }

  const handleCourseToggle = async (courseTitle) => {
    const isCompleted = completedCourses.has(courseTitle)
    const newCompleted = new Set(completedCourses)
    
    if (isCompleted) {
      newCompleted.delete(courseTitle)
    } else {
      newCompleted.add(courseTitle)
      toast.success('Course completed! 🎉')
    }
    
    setCompletedCourses(newCompleted)
    
    try {
      await agentAPI.updateCourseProgress(courseTitle, !isCompleted)
    } catch (error) {
      console.error('Failed to save course progress:', error)
    }
  }

  const handleTaskToggle = (taskId) => {
    const isCompleted = completedTasks.has(taskId)
    const newCompleted = new Set(completedTasks)
    
    if (isCompleted) {
      newCompleted.delete(taskId)
    } else {
      newCompleted.add(taskId)
    }
    
    setCompletedTasks(newCompleted)
    setHasUnsavedChanges(true)
  }

  const handleSaveProgress = async () => {
    setSavingProgress(true)
    try {
      // Save all completed tasks to backend
      const promises = Array.from(completedTasks).map(taskId => 
        agentAPI.updateRoadmapProgress(taskId, true)
      )
      
      // Also save uncompleted tasks (tasks that were previously completed but now unchecked)
      const allTaskIds = []
      if (result?.roadmap) {
        result.roadmap.foundation?.forEach(task => allTaskIds.push(task.id))
        result.roadmap.advancement?.forEach(task => allTaskIds.push(task.id))
        result.roadmap.market_ready?.forEach(task => allTaskIds.push(task.id))
      }
      
      const uncompletedTasks = allTaskIds.filter(id => !completedTasks.has(id))
      const uncompletedPromises = uncompletedTasks.map(taskId => 
        agentAPI.updateRoadmapProgress(taskId, false)
      )
      
      await Promise.all([...promises, ...uncompletedPromises])
      
      setHasUnsavedChanges(false)
      toast.success('Progress saved successfully!')
    } catch (error) {
      console.error('Save progress error:', error)
      toast.error('Failed to save progress')
    } finally {
      setSavingProgress(false)
    }
  }

  const handleSavePlan = async () => {
    setSavingPlan(true)
    try {
      await agentAPI.saveCareerPlan({ tasks: result.tasks })
      toast.success('Career plan saved as goals successfully!')
    } catch (error) {
      console.error('Save plan error:', error)
      toast.error('Failed to save plan')
    } finally {
      setSavingPlan(false)
    }
  }

  const handleReplan = async () => {
    setUpdatingPlan(true)
    try {
      const response = await agentAPI.replanCareer(Array.from(completedTasks))
      const updatedTasks = [...result.tasks.filter(t => !completedTasks.has(t.id)), ...response.data.tasks]
      setResult({ ...result, tasks: updatedTasks })
      setCompletedTasks(new Set())
      toast.success(response.data.message)
    } catch (error) {
      console.error('Update plan error:', error)
      toast.error('Failed to update plan')
    } finally {
      setUpdatingPlan(false)
    }
  }

  const groupTasksByPhase = (tasks) => {
    const phases = {
      'Foundation Building': [],
      'Skill Advancement': [],
      'Market Ready': []
    }
    
    tasks.forEach(task => {
      if (phases[task.phase]) {
        phases[task.phase].push(task)
      }
    })
    
    return phases
  }

  const getCategoryColor = (category) => {
    const colors = {
      'Skill Building': 'bg-blue-100 text-blue-800 border-blue-200',
      'Projects': 'bg-green-100 text-green-800 border-green-200',
      'Job Search': 'bg-purple-100 text-purple-800 border-purple-200',
      'Interview Prep': 'bg-pink-100 text-pink-800 border-pink-200'
    }
    return colors[category] || 'bg-gray-100 text-gray-800 border-gray-200'
  }

  return (
    <div className="space-y-8">
      {/* Input Form */}
      <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Task Type
            </label>
            <select
              {...register('task_type', { required: 'Task type is required' })}
              className="w-full px-4 py-3 bg-white/50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500"
            >
              <option value="general">General Career Guidance</option>
              <option value="job_search">Job Search Strategy</option>
              <option value="skill_development">Skill Development</option>
            </select>
            {errors.task_type && (
              <p className="text-sm text-red-600 mt-1">{errors.task_type.message}</p>
            )}
          </div>

          {taskType === 'skill_development' ? (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Current Skill Level
              </label>
              <select
                {...register('skill_level', { required: 'Skill level is required' })}
                className="w-full px-4 py-3 bg-white/50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500"
              >
                <option value="">Select your level</option>
                <option value="Beginner">Beginner</option>
                <option value="Intermediate">Intermediate</option>
                <option value="Advanced">Advanced</option>
              </select>
              {errors.skill_level && (
                <p className="text-sm text-red-600 mt-1">{errors.skill_level.message}</p>
              )}
            </div>
          ) : (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Years of Experience
              </label>
              <input
                {...register('experience_years', { required: 'Experience is required' })}
                type="number"
                min="0"
                max="50"
                className="w-full px-4 py-3 bg-white/50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500"
                placeholder="e.g., 3"
              />
              {errors.experience_years && (
                <p className="text-sm text-red-600 mt-1">{errors.experience_years.message}</p>
              )}
            </div>
          )}
        </div>

        {taskType === 'skill_development' ? (
          <>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Target Skill Area
              </label>
              <input
                {...register('target_area', { required: 'Target area is required' })}
                type="text"
                className="w-full px-4 py-3 bg-white/50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500"
                placeholder="e.g., Backend with Java, Frontend with React, Cloud, Data Engineering"
              />
              {errors.target_area && (
                <p className="text-sm text-red-600 mt-1">{errors.target_area.message}</p>
              )}
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Weekly Time Commitment
                </label>
                <select
                  {...register('weekly_hours', { required: 'Time commitment is required' })}
                  className="w-full px-4 py-3 bg-white/50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500"
                >
                  <option value="">Select hours per week</option>
                  <option value="3-5 hrs">3-5 hours</option>
                  <option value="5-8 hrs">5-8 hours</option>
                  <option value="8-12 hrs">8-12 hours</option>
                  <option value="12+ hrs">12+ hours</option>
                </select>
                {errors.weekly_hours && (
                  <p className="text-sm text-red-600 mt-1">{errors.weekly_hours.message}</p>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Time Horizon
                </label>
                <select
                  {...register('time_horizon', { required: 'Time horizon is required' })}
                  className="w-full px-4 py-3 bg-white/50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500"
                >
                  <option value="">Select timeline</option>
                  <option value="1 month">1 month</option>
                  <option value="3 months">3 months</option>
                  <option value="6 months">6 months</option>
                </select>
                {errors.time_horizon && (
                  <p className="text-sm text-red-600 mt-1">{errors.time_horizon.message}</p>
                )}
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Specific Technologies (Optional)
              </label>
              <input
                {...register('technologies')}
                type="text"
                className="w-full px-4 py-3 bg-white/50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500"
                placeholder="e.g., React, Node.js, Docker, AWS"
              />
            </div>
          </>
        ) : (
          <>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Skills (comma-separated)
              </label>
              <input
                {...register('skills', { required: 'Skills are required' })}
                type="text"
                className="w-full px-4 py-3 bg-white/50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500"
                placeholder="e.g., JavaScript, React, Node.js, Python"
              />
              {errors.skills && (
                <p className="text-sm text-red-600 mt-1">{errors.skills.message}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Location
              </label>
              <input
                {...register('location', { required: 'Location is required' })}
                type="text"
                className="w-full px-4 py-3 bg-white/50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500"
                placeholder="e.g., San Francisco, CA"
              />
              {errors.location && (
                <p className="text-sm text-red-600 mt-1">{errors.location.message}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Career Goal (Optional)
              </label>
              <textarea
                {...register('goal')}
                rows="3"
                className="w-full px-4 py-3 bg-white/50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500"
                placeholder="Describe your career aspirations..."
              />
            </div>
          </>
        )}

        <div className="flex justify-end">
          <button
            type="submit"
            disabled={loading}
            className="px-8 py-3 bg-gradient-to-r from-purple-600 to-pink-600 text-white font-semibold rounded-xl hover:from-purple-700 hover:to-pink-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 shadow-lg hover:shadow-xl transform hover:scale-105"
          >
            {loading ? (
              <div className="flex items-center">
                <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
                Analyzing...
              </div>
            ) : (
              'Run Career Agent'
            )}
          </button>
        </div>
      </form>



      {/* Results */}
      {result && (
        <div className="space-y-8">
          {/* Skills Analysis */}
          <div className="bg-gradient-to-r from-purple-50 to-pink-50 rounded-2xl p-6 border border-purple-200">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Career Analysis Results</h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
              <div>
                <h4 className="font-medium text-gray-900 mb-3">Current Skills</h4>
                <div className="flex flex-wrap gap-2">
                  {result.current_skills?.map((skill, index) => (
                    <span key={index} className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm">
                      {skill}
                    </span>
                  ))}
                </div>
              </div>
              
              <div>
                <h4 className="font-medium text-gray-900 mb-3">Priority Skills to Learn</h4>
                <div className="flex flex-wrap gap-2">
                  {result.priority_skills?.map((skill, index) => (
                    <span key={index} className="px-3 py-1 bg-orange-100 text-orange-800 rounded-full text-sm">
                      {skill}
                    </span>
                  ))}
                </div>
              </div>
            </div>
            
            {/* Target Roles */}
            <div>
              <h4 className="font-medium text-gray-900 mb-3">Recommended Roles</h4>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {result.recommended_roles?.map((role, index) => (
                  <div key={index} className="bg-white rounded-xl p-4 border border-white/50">
                    <h3 className="font-semibold text-gray-900 mb-2">{role.title}</h3>
                    <p className="text-sm text-gray-600">{role.description}</p>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* 30/60/90 Day Roadmap */}
          <div className="space-y-6">
            <div className="flex items-center justify-between">
              <h3 className="text-2xl font-semibold text-gray-900">Career Development Roadmap</h3>
              {result && (
                <button
                  onClick={handleSaveProgress}
                  disabled={savingProgress || !hasUnsavedChanges}
                  className={`px-6 py-2 rounded-xl font-medium transition-all duration-200 ${
                    hasUnsavedChanges
                      ? 'bg-gradient-to-r from-purple-600 to-pink-600 text-white hover:from-purple-700 hover:to-pink-700 shadow-lg hover:shadow-xl transform hover:scale-105'
                      : 'bg-gray-100 text-gray-400 cursor-not-allowed'
                  }`}
                >
                  {savingProgress ? (
                    <div className="flex items-center">
                      <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
                      Saving...
                    </div>
                  ) : (
                    'Save Changes'
                  )}
                </button>
              )}
            </div>
            
            {/* Unified roadmap grid with equal-height cards */}
            <div className="space-y-8">
              {/* Phase Headers - Hidden for Skill Development */}
              {taskType !== 'skill_development' && (
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                  <div className="flex items-center">
                    <div className="w-8 h-8 bg-purple-100 rounded-full flex items-center justify-center mr-3">
                      <span className="text-purple-600 font-bold text-sm">1</span>
                    </div>
                    <h4 className="text-lg font-bold text-gray-900">Foundation Building</h4>
                  </div>
                  <div className="flex items-center">
                    <div className="w-8 h-8 bg-pink-100 rounded-full flex items-center justify-center mr-3">
                      <span className="text-pink-600 font-bold text-sm">2</span>
                    </div>
                    <h4 className="text-lg font-bold text-gray-900">Skill Advancement</h4>
                  </div>
                  <div className="flex items-center">
                    <div className="w-8 h-8 bg-indigo-100 rounded-full flex items-center justify-center mr-3">
                      <span className="text-indigo-600 font-bold text-sm">3</span>
                    </div>
                    <h4 className="text-lg font-bold text-gray-900">Market Ready</h4>
                  </div>
                </div>
              )}

              {/* Normalized task cards grid */}
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 auto-rows-fr">
                {/* Foundation tasks */}
                {result.roadmap?.foundation?.map((task, index) => (
                  <RoadmapTaskCard
                    key={task.id || `f-${index}`}
                    task={task}
                    isCompleted={completedTasks.has(task.id)}
                    onToggle={handleTaskToggle}
                    colorScheme="purple"
                  />
                ))}
                
                {/* Advancement tasks */}
                {result.roadmap?.advancement?.map((task, index) => (
                  <RoadmapTaskCard
                    key={task.id || `a-${index}`}
                    task={task}
                    isCompleted={completedTasks.has(task.id)}
                    onToggle={handleTaskToggle}
                    colorScheme="pink"
                  />
                ))}
                
                {/* Market ready tasks */}
                {result.roadmap?.market_ready?.map((task, index) => (
                  <RoadmapTaskCard
                    key={task.id || `m-${index}`}
                    task={task}
                    isCompleted={completedTasks.has(task.id)}
                    onToggle={handleTaskToggle}
                    colorScheme="indigo"
                  />
                ))}
              </div>
            </div>
          </div>

          {/* Recommended Courses */}
          {result.recommended_courses && (
            <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-2xl p-6 border border-blue-200">
              <h3 className="text-2xl font-semibold text-gray-900 mb-6">Recommended Learning Resources</h3>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {result.recommended_courses.map((course, index) => (
                  <div key={index} className="bg-white rounded-xl p-4 border border-blue-100 shadow-sm hover:shadow-md transition-shadow">
                    <div className="flex items-start justify-between mb-3">
                      <h4 className="font-semibold text-gray-900 text-sm">{course.title}</h4>
                      <span className="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded-full">{course.platform}</span>
                    </div>
                    <p className="text-sm text-gray-600 mb-3 leading-relaxed">{course.why_relevant}</p>
                    <div className="flex items-center justify-between">
                      <a
                        href={course.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-flex items-center text-sm font-medium text-blue-600 hover:text-blue-700 transition-colors"
                      >
                        <LinkIcon className="w-4 h-4 mr-1" />
                        View Course
                      </a>
                      <button
                        onClick={() => handleCourseToggle(course.title)}
                        className={`px-3 py-1 text-xs font-medium rounded-full transition-all ${
                          completedCourses.has(course.title)
                            ? 'bg-green-100 text-green-700 hover:bg-green-200'
                            : 'bg-gradient-to-r from-purple-500 to-pink-500 text-white hover:from-purple-600 hover:to-pink-600 transform hover:scale-105'
                        }`}
                      >
                        {completedCourses.has(course.title) ? '✓ Completed' : 'Complete'}
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Job Search Links */}
          {result.recommended_links && (
            <div className="bg-gradient-to-r from-blue-50 to-indigo-50 rounded-2xl p-6 border border-blue-200">
              <h3 className="text-2xl font-semibold text-gray-900 mb-6">Job Search Resources</h3>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {result.recommended_links.map((link, index) => {
                  const getTypeColor = (type) => {
                    switch(type) {
                      case 'job_board': return 'bg-blue-100 text-blue-700'
                      case 'company_careers': return 'bg-purple-100 text-purple-700'
                      case 'linkedin_profile': return 'bg-green-100 text-green-700'
                      default: return 'bg-gray-100 text-gray-700'
                    }
                  }
                  
                  return (
                    <div key={index} className="bg-white rounded-xl p-4 border border-green-100 shadow-sm hover:shadow-md transition-shadow">
                      <div className="flex items-start justify-between mb-3">
                        <h4 className="font-semibold text-gray-900 text-sm">{link.title}</h4>
                        <span className={`text-xs px-2 py-1 rounded-full ${getTypeColor(link.type)}`}>
                          {link.type.replace('_', ' ')}
                        </span>
                      </div>
                      <p className="text-sm text-gray-600 mb-3 leading-relaxed">{link.why_relevant}</p>
                      <a
                        href={link.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-flex items-center text-sm font-medium text-blue-600 hover:text-blue-700 transition-colors"
                      >
                        <LinkIcon className="w-4 h-4 mr-1" />
                        Visit Site
                      </a>
                    </div>
                  )
                })}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default CareerAgentForm