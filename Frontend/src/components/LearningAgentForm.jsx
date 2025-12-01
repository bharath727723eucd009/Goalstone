import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { agentAPI } from '../services/api'
import toast from 'react-hot-toast'
import { ScrollReveal, StaggeredReveal } from '../hooks/useScrollReveal'
import { 
  AcademicCapIcon,
  ClockIcon,
  LinkIcon,
  CheckCircleIcon
} from '@heroicons/react/24/outline'

const FALLBACK_COURSES = [
  { title: 'Introduction to Programming', platform: 'Coursera', level: 'Beginner', duration: '4 weeks', url: 'https://www.coursera.org/learn/programming-fundamentals', free: true },
  { title: 'Data Structures Fundamentals', platform: 'Udemy', level: 'Beginner', duration: '6 weeks', url: 'https://www.udemy.com/course/data-structures-and-algorithms/', free: false },
  { title: 'Web Development Bootcamp', platform: 'Udemy', level: 'Beginner', duration: '8 weeks', url: 'https://www.udemy.com/course/the-web-developer-bootcamp/', free: false },
  { title: 'JavaScript Essentials', platform: 'freeCodeCamp', level: 'Beginner', duration: '5 weeks', url: 'https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures/', free: true },
  { title: 'React Complete Guide', platform: 'Udemy', level: 'Intermediate', duration: '10 weeks', url: 'https://www.udemy.com/course/react-the-complete-guide/', free: false },
  { title: 'Node.js Backend Development', platform: 'Coursera', level: 'Intermediate', duration: '6 weeks', url: 'https://www.coursera.org/learn/server-side-nodejs', free: false },
  { title: 'Database Design & SQL', platform: 'Udacity', level: 'Intermediate', duration: '4 weeks', url: 'https://www.udacity.com/course/sql-for-data-analysis--ud198', free: false },
  { title: 'Python for Data Science', platform: 'Coursera', level: 'Intermediate', duration: '8 weeks', url: 'https://www.coursera.org/learn/python-for-applied-data-science-ai', free: true },
  { title: 'Advanced Algorithms', platform: 'MIT OpenCourseWare', level: 'Advanced', duration: '12 weeks', url: 'https://ocw.mit.edu/courses/6-046j-design-and-analysis-of-algorithms-spring-2015/', free: true },
  { title: 'System Design Masterclass', platform: 'Educative', level: 'Advanced', duration: '6 weeks', url: 'https://www.educative.io/courses/grokking-the-system-design-interview', free: false },
  { title: 'Cloud Architecture AWS', platform: 'AWS Training', level: 'Advanced', duration: '8 weeks', url: 'https://aws.amazon.com/training/', free: true },
  { title: 'Machine Learning Specialization', platform: 'Coursera', level: 'Advanced', duration: '12 weeks', url: 'https://www.coursera.org/specializations/machine-learning-introduction', free: false },
  { title: 'DevOps Engineering', platform: 'Udemy', level: 'Intermediate', duration: '7 weeks', url: 'https://www.udemy.com/course/devops-bootcamp/', free: false },
  { title: 'Mobile App Development', platform: 'Udacity', level: 'Intermediate', duration: '10 weeks', url: 'https://www.udacity.com/course/android-basics-nanodegree-by-google--nd803', free: false }
]

const LearningAgentForm = ({ onResult }) => {
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const { register, handleSubmit, formState: { errors } } = useForm()

  const onSubmit = async (data) => {
    setLoading(true)
    try {
      const contentTypes = []
      if (data.content_video) contentTypes.push('Video')
      if (data.content_articles) contentTypes.push('Articles')
      if (data.content_projects) contentTypes.push('Projects')
      if (data.content_docs) contentTypes.push('Documentation')

      const userData = {
        target_skill: data.target_skill,
        current_level: data.current_level,
        weekly_hours: parseInt(data.weekly_hours),
        content_types: contentTypes.join(', '),
        technologies: data.technologies || ''
      }
      
      const response = await agentAPI.learning({ user_data: userData })
      
      // Process courses and ensure at least 14 unique courses
      let courses = response.data?.courses || []
      
      // Remove duplicates
      const uniqueCourses = Array.from(
        new Map(courses.map(c => [c.title, c])).values()
      )
      
      // Top up with fallback courses if needed
      if (uniqueCourses.length < 14) {
        const needed = 14 - uniqueCourses.length
        const existingTitles = new Set(uniqueCourses.map(c => c.title))
        const additionalCourses = FALLBACK_COURSES
          .filter(c => !existingTitles.has(c.title))
          .slice(0, needed)
        courses = [...uniqueCourses, ...additionalCourses]
      } else {
        courses = uniqueCourses
      }
      
      // Ensure even number
      if (courses.length % 2 !== 0) {
        const lastFallback = FALLBACK_COURSES.find(
          c => !courses.some(existing => existing.title === c.title)
        )
        if (lastFallback) courses.push(lastFallback)
      }
      
      // Sort by level
      const levelOrder = { 'Beginner': 1, 'Intermediate': 2, 'Advanced': 3 }
      courses.sort((a, b) => (levelOrder[a.level] || 2) - (levelOrder[b.level] || 2))
      
      setResult({
        ...response.data,
        courses,
        user_data: userData
      })
      onResult(response)
    } catch (error) {
      console.error('Learning agent error:', error)
      toast.error('Failed to generate learning plan. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const getLevelColor = (level) => {
    switch(level) {
      case 'Beginner': return 'bg-green-100 text-green-700 border-green-200'
      case 'Intermediate': return 'bg-blue-100 text-blue-700 border-blue-200'
      case 'Advanced': return 'bg-purple-100 text-purple-700 border-purple-200'
      default: return 'bg-gray-100 text-gray-700 border-gray-200'
    }
  }

  return (
    <div className="min-h-screen">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Left: Input Card */}
        <ScrollReveal delay={200}>
          <div className="backdrop-blur-sm bg-white/80 rounded-3xl p-8 shadow-xl border border-white/30">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Build your learning path</h2>
            
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
              {/* Target Skill */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Target Role or Skill
                </label>
                <input
                  type="text"
                  {...register('target_skill', { required: 'Target skill is required' })}
                  className="w-full px-4 py-3 bg-white/50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500"
                  placeholder="e.g., Full Stack Developer, Data Science, Cloud Engineering"
                />
                {errors.target_skill && <p className="text-sm text-red-600 mt-1">{errors.target_skill.message}</p>}
              </div>

              {/* Current Level */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Current Level
                </label>
                <select
                  {...register('current_level', { required: 'Level is required' })}
                  className="w-full px-4 py-3 bg-white/50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500"
                >
                  <option value="">Select your level</option>
                  <option value="Beginner">Beginner</option>
                  <option value="Intermediate">Intermediate</option>
                  <option value="Advanced">Advanced</option>
                </select>
                {errors.current_level && <p className="text-sm text-red-600 mt-1">{errors.current_level.message}</p>}
              </div>

              {/* Weekly Study Time */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Weekly Study Time (hours)
                </label>
                <input
                  type="text"
                  {...register('weekly_hours', { required: 'Weekly hours required' })}
                  className="w-full px-4 py-3 bg-white/50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500"
                  placeholder="e.g., 10"
                />
                {errors.weekly_hours && <p className="text-sm text-red-600 mt-1">{errors.weekly_hours.message}</p>}
              </div>

              {/* Preferred Content Type */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-3">
                  Preferred Content Type
                </label>
                <div className="grid grid-cols-2 gap-3">
                  <label className="flex items-center p-3 bg-white/50 rounded-xl border border-gray-200 cursor-pointer hover:border-purple-300 transition-colors">
                    <input type="checkbox" {...register('content_video')} className="mr-3 w-4 h-4 text-purple-600" />
                    <span className="text-sm font-medium">Video</span>
                  </label>
                  <label className="flex items-center p-3 bg-white/50 rounded-xl border border-gray-200 cursor-pointer hover:border-purple-300 transition-colors">
                    <input type="checkbox" {...register('content_articles')} className="mr-3 w-4 h-4 text-purple-600" />
                    <span className="text-sm font-medium">Articles</span>
                  </label>
                  <label className="flex items-center p-3 bg-white/50 rounded-xl border border-gray-200 cursor-pointer hover:border-purple-300 transition-colors">
                    <input type="checkbox" {...register('content_projects')} className="mr-3 w-4 h-4 text-purple-600" />
                    <span className="text-sm font-medium">Projects</span>
                  </label>
                  <label className="flex items-center p-3 bg-white/50 rounded-xl border border-gray-200 cursor-pointer hover:border-purple-300 transition-colors">
                    <input type="checkbox" {...register('content_docs')} className="mr-3 w-4 h-4 text-purple-600" />
                    <span className="text-sm font-medium">Docs</span>
                  </label>
                </div>
              </div>

              {/* Technologies */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Specific Technologies (Optional)
                </label>
                <input
                  type="text"
                  {...register('technologies')}
                  className="w-full px-4 py-3 bg-white/50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500"
                  placeholder="e.g., React, Python, AWS, Docker"
                />
                <p className="text-xs text-gray-500 mt-1">Comma-separated list</p>
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
                  'Generate learning plan'
                )}
              </button>
            </form>
          </div>
        </ScrollReveal>

        {/* Right: Results Card */}
        <ScrollReveal delay={400}>
          <div className="backdrop-blur-sm bg-white/80 rounded-3xl p-8 shadow-xl border border-white/30">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">Your Learning Plan</h2>
            
            {!result ? (
              <div className="text-center py-12">
                <div className="w-16 h-16 bg-gradient-to-br from-purple-100 to-pink-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <AcademicCapIcon className="w-8 h-8 text-purple-600" />
                </div>
                <p className="text-gray-600">Run the Learning Agent to see your personalized recommendations.</p>
              </div>
            ) : (
              <div className="space-y-6">
                {/* Learning Plan Summary */}
                <div className="bg-gradient-to-r from-purple-50 to-pink-50 rounded-2xl p-6 border border-purple-200">
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="text-sm font-semibold text-gray-600">Target Skill</span>
                      <span className="text-sm font-bold text-gray-900">{result.user_data?.target_skill}</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm font-semibold text-gray-600">Duration</span>
                      <span className="text-sm font-bold text-gray-900">3-4 months</span>
                    </div>
                    <div className="flex items-center justify-between">
                      <span className="text-sm font-semibold text-gray-600">Weekly Hours</span>
                      <span className="text-sm font-bold text-gray-900">{result.user_data?.weekly_hours} hrs</span>
                    </div>
                  </div>
                  
                  <div className="mt-4 pt-4 border-t border-purple-200">
                    <h4 className="text-sm font-bold text-gray-900 mb-2">Learning Path</h4>
                    <ul className="space-y-2 text-sm text-gray-700">
                      <li className="flex items-start">
                        <CheckCircleIcon className="w-4 h-4 text-green-600 mr-2 mt-0.5 flex-shrink-0" />
                        <span>Master fundamentals and core concepts</span>
                      </li>
                      <li className="flex items-start">
                        <CheckCircleIcon className="w-4 h-4 text-blue-600 mr-2 mt-0.5 flex-shrink-0" />
                        <span>Build practical projects and portfolio</span>
                      </li>
                      <li className="flex items-start">
                        <CheckCircleIcon className="w-4 h-4 text-purple-600 mr-2 mt-0.5 flex-shrink-0" />
                        <span>Advanced topics and specialization</span>
                      </li>
                    </ul>
                  </div>
                </div>

                {/* Recommended Courses */}
                <div>
                  <h3 className="text-lg font-bold text-gray-900 mb-4">
                    Recommended Courses ({result.courses?.length || 0})
                  </h3>
                  
                  <StaggeredReveal staggerDelay={100} className="grid grid-cols-1 md:grid-cols-2 gap-4 max-h-[600px] overflow-y-auto pr-2">
                    {result.courses?.map((course, index) => (
                      <div
                        key={index}
                        className="backdrop-blur-sm bg-white/70 rounded-xl p-4 border border-white/30 shadow-sm hover:shadow-md transition-all duration-200 hover:scale-[1.02]"
                      >
                        <div className="flex items-start justify-between mb-3">
                          <h4 className="font-semibold text-gray-900 text-sm flex-1 pr-2">{course.title}</h4>
                          {course.free && (
                            <span className="text-xs bg-green-100 text-green-700 px-2 py-1 rounded-full flex-shrink-0">Free</span>
                          )}
                          {course.free === false && (
                            <span className="text-xs bg-orange-100 text-orange-700 px-2 py-1 rounded-full flex-shrink-0">Paid</span>
                          )}
                        </div>
                        
                        <div className="flex items-center gap-2 mb-3">
                          <span className="text-xs text-gray-600">{course.platform}</span>
                          <span className="text-gray-300">•</span>
                          <span className={`text-xs px-2 py-0.5 rounded-full border ${getLevelColor(course.level)}`}>
                            {course.level}
                          </span>
                        </div>
                        
                        <div className="flex items-center text-xs text-gray-500 mb-3">
                          <ClockIcon className="w-3 h-3 mr-1" />
                          {course.duration}
                        </div>
                        
                        {course.url && course.url !== '#' ? (
                          <a
                            href={course.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="inline-flex items-center text-sm font-medium text-purple-600 hover:text-purple-700 transition-colors"
                          >
                            <LinkIcon className="w-4 h-4 mr-1" />
                            Open course
                          </a>
                        ) : (
                          <span className="inline-flex items-center text-sm font-medium text-gray-400">
                            <LinkIcon className="w-4 h-4 mr-1" />
                            No link available
                          </span>
                        )}
                      </div>
                    ))}
                  </StaggeredReveal>
                </div>

                {/* AI Response */}
                {result.response && (
                  <div className="bg-gray-50 rounded-xl p-4 border border-gray-200">
                    <h3 className="text-sm font-bold text-gray-900 mb-2">AI Recommendations</h3>
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

export default LearningAgentForm
