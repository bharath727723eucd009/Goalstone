import { 
  CheckCircleIcon, 
  LightBulbIcon, 
  ListBulletIcon,
  ChartBarIcon,
  CalendarDaysIcon,
  BookOpenIcon,
  CurrencyDollarIcon
} from '@heroicons/react/24/outline'

const AgentResponse = ({ result, agentType }) => {
  if (!result || !result.data) return null

  const { data } = result

  const renderRecommendation = () => (
    <div className="bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 rounded-lg p-6 mb-6">
      <div className="flex items-start">
        <LightBulbIcon className="h-6 w-6 text-blue-600 mt-1 mr-3 flex-shrink-0" />
        <div>
          <h3 className="text-lg font-semibold text-blue-900 mb-2">AI Recommendation</h3>
          <p className="text-blue-800 leading-relaxed">{data.recommendation}</p>
        </div>
      </div>
    </div>
  )

  const renderActionItems = () => {
    if (!data.action_items || !Array.isArray(data.action_items)) return null
    
    return (
      <div className="bg-white border border-gray-200 rounded-lg p-6 mb-6">
        <div className="flex items-center mb-4">
          <ListBulletIcon className="h-5 w-5 text-green-600 mr-2" />
          <h4 className="text-md font-semibold text-gray-900">Action Items</h4>
        </div>
        <ul className="space-y-3">
          {data.action_items.map((item, index) => (
            <li key={index} className="flex items-start">
              <CheckCircleIcon className="h-5 w-5 text-green-500 mt-0.5 mr-3 flex-shrink-0" />
              <span className="text-gray-700">{item}</span>
            </li>
          ))}
        </ul>
      </div>
    )
  }

  const renderBudgetBreakdown = () => {
    if (!data.budget_breakdown) return null
    
    return (
      <div className="bg-white border border-gray-200 rounded-lg p-6 mb-6">
        <div className="flex items-center mb-4">
          <ChartBarIcon className="h-5 w-5 text-purple-600 mr-2" />
          <h4 className="text-md font-semibold text-gray-900">Budget Breakdown</h4>
        </div>
        <div className="grid grid-cols-3 gap-4">
          {Object.entries(data.budget_breakdown).map(([category, percentage]) => (
            <div key={category} className="text-center p-4 bg-gray-50 rounded-lg">
              <div className="text-2xl font-bold text-purple-600">{percentage}</div>
              <div className="text-sm text-gray-600 capitalize">{category.replace('_', ' ')}</div>
            </div>
          ))}
        </div>
      </div>
    )
  }

  const renderWeeklyPlan = () => {
    if (!data.weekly_plan || !Array.isArray(data.weekly_plan)) return null
    
    return (
      <div className="bg-white border border-gray-200 rounded-lg p-6 mb-6">
        <div className="flex items-center mb-4">
          <CalendarDaysIcon className="h-5 w-5 text-orange-600 mr-2" />
          <h4 className="text-md font-semibold text-gray-900">Weekly Plan</h4>
        </div>
        <div className="space-y-3">
          {data.weekly_plan.map((day, index) => (
            <div key={index} className="flex items-center p-3 bg-orange-50 rounded-lg">
              <div className="w-2 h-2 bg-orange-500 rounded-full mr-3"></div>
              <span className="text-gray-700">{day}</span>
            </div>
          ))}
        </div>
      </div>
    )
  }

  const renderCourseSuggestions = () => {
    if (!data.course_suggestions || !Array.isArray(data.course_suggestions)) return null
    
    return (
      <div className="bg-white border border-gray-200 rounded-lg p-6 mb-6">
        <div className="flex items-center mb-4">
          <BookOpenIcon className="h-5 w-5 text-indigo-600 mr-2" />
          <h4 className="text-md font-semibold text-gray-900">Course Suggestions</h4>
        </div>
        <div className="space-y-3">
          {data.course_suggestions.map((course, index) => (
            <div key={index} className="flex items-start p-4 bg-indigo-50 rounded-lg border border-indigo-200">
              <div className="w-8 h-8 bg-indigo-100 rounded-full flex items-center justify-center mr-3 flex-shrink-0">
                <span className="text-indigo-600 font-semibold text-sm">{index + 1}</span>
              </div>
              <div>
                <span className="text-gray-800 font-medium">{course}</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    )
  }

  return (
    <div className="mt-8">
      <div className="flex items-center mb-6">
        <div className="w-10 h-10 bg-green-100 rounded-full flex items-center justify-center mr-3">
          <CheckCircleIcon className="h-6 w-6 text-green-600" />
        </div>
        <div>
          <h3 className="text-xl font-bold text-gray-900">Analysis Complete!</h3>
          <p className="text-gray-600">Here's your personalized recommendation</p>
        </div>
      </div>

      {renderRecommendation()}
      {renderActionItems()}
      {renderBudgetBreakdown()}
      {renderWeeklyPlan()}
      {renderCourseSuggestions()}

      <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
        <p className="text-sm text-gray-600 text-center">
          💡 Tip: Save this recommendation and track your progress in the dashboard
        </p>
      </div>
    </div>
  )
}

export default AgentResponse