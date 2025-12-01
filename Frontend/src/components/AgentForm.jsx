import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { agentAPI } from '../services/api'
import toast from 'react-hot-toast'
import AgentResponse from './AgentResponse'
import { 
  BriefcaseIcon, 
  BanknotesIcon, 
  HeartIcon, 
  AcademicCapIcon,
  PlayIcon
} from '@heroicons/react/24/outline'

const agentConfig = {
  career: {
    icon: BriefcaseIcon,
    title: 'Career Agent',
    description: 'Get job recommendations and career guidance',
    taskTypes: [
      { value: 'job_search', label: 'Job Search' },
      { value: 'skill_analysis', label: 'Skill Analysis' }
    ],
    fields: [
      { name: 'skills', label: 'Skills', type: 'tags', placeholder: 'Python, JavaScript, etc.' },
      { name: 'experience_years', label: 'Years of Experience', type: 'number' },
      { name: 'location', label: 'Location', type: 'text', placeholder: 'San Francisco, CA' }
    ]
  },
  finance: {
    icon: BanknotesIcon,
    title: 'Finance Agent',
    description: 'Get financial planning and investment advice',
    taskTypes: [
      { value: 'budget_analysis', label: 'Budget Analysis' },
      { value: 'investment_advice', label: 'Investment Advice' }
    ],
    fields: [
      { name: 'income', label: 'Annual Income', type: 'number', placeholder: '75000' },
      { name: 'expenses', label: 'Monthly Expenses', type: 'number', placeholder: '4000' },
      { name: 'age', label: 'Age', type: 'number' },
      { name: 'financial_goals', label: 'Financial Goals', type: 'tags', placeholder: 'retirement, house' }
    ]
  },
  wellness: {
    icon: HeartIcon,
    title: 'Wellness Agent',
    description: 'Get fitness plans and health recommendations',
    taskTypes: [
      { value: 'fitness_plan', label: 'Fitness Plan' },
      { value: 'nutrition_advice', label: 'Nutrition Advice' },
      { value: 'health_assessment', label: 'Health Assessment' }
    ],
    fields: [
      { name: 'age', label: 'Age', type: 'number' },
      { name: 'weight', label: 'Weight (kg)', type: 'number' },
      { name: 'height', label: 'Height (cm)', type: 'number' },
      { name: 'activity_level', label: 'Activity Level', type: 'select', options: [
        { value: 'low', label: 'Low' },
        { value: 'moderate', label: 'Moderate' },
        { value: 'high', label: 'High' }
      ]},
      { name: 'health_goals', label: 'Health Goals', type: 'tags', placeholder: 'weight_loss, muscle_gain' }
    ]
  },
  learning: {
    icon: AcademicCapIcon,
    title: 'Learning Agent',
    description: 'Get course recommendations and learning paths',
    taskTypes: [
      { value: 'course_recommendation', label: 'Course Recommendation' },
      { value: 'skill_gap_analysis', label: 'Skill Gap Analysis' },
      { value: 'learning_path', label: 'Learning Path' }
    ],
    fields: [
      { name: 'current_skills', label: 'Current Skills', type: 'tags', placeholder: 'Python, SQL' },
      { name: 'interests', label: 'Interests', type: 'tags', placeholder: 'Machine Learning, AI' },
      { name: 'learning_style', label: 'Learning Style', type: 'select', options: [
        { value: 'visual', label: 'Visual' },
        { value: 'hands_on', label: 'Hands-on' },
        { value: 'reading', label: 'Reading' }
      ]},
      { name: 'time_commitment', label: 'Time Commitment', type: 'select', options: [
        { value: '5_hours_week', label: '5 hours/week' },
        { value: '10_hours_week', label: '10 hours/week' },
        { value: '20_hours_week', label: '20+ hours/week' }
      ]}
    ]
  }
}

const AgentForm = ({ agentType, onResult }) => {
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const { register, handleSubmit, watch, setValue, formState: { errors } } = useForm()
  
  const config = agentConfig[agentType]
  const Icon = config.icon
  const selectedTaskType = watch('task_type')

  const onSubmit = async (data) => {
    setLoading(true)
    setResult(null)
    
    try {
      // Process form data
      const userData = {}
      const parameters = {}
      
      config.fields.forEach(field => {
        if (data[field.name]) {
          if (field.type === 'tags') {
            userData[field.name] = data[field.name].split(',').map(s => s.trim()).filter(Boolean)
          } else if (field.type === 'number') {
            userData[field.name] = Number(data[field.name])
          } else {
            userData[field.name] = data[field.name]
          }
        }
      })

      const payload = {
        user_data: userData,
        task_type: data.task_type,
        parameters
      }

      const response = await agentAPI[agentType](payload)
      setResult(response)
      onResult?.(response)
      toast.success(`${config.title} completed successfully!`)
    } catch (error) {
      toast.error(error.response?.data?.detail || `${config.title} failed`)
      console.error('Agent error:', error)
    } finally {
      setLoading(false)
    }
  }

  const renderField = (field) => {
    const fieldProps = {
      ...register(field.name, { 
        required: field.required !== false,
        ...(field.type === 'number' && { valueAsNumber: true })
      }),
      className: 'input-field',
      placeholder: field.placeholder
    }

    switch (field.type) {
      case 'select':
        return (
          <select {...fieldProps}>
            <option value="">Select {field.label}</option>
            {field.options.map(option => (
              <option key={option.value} value={option.value}>
                {option.label}
              </option>
            ))}
          </select>
        )
      case 'tags':
        return (
          <input
            {...fieldProps}
            type="text"
            placeholder={`${field.placeholder} (comma-separated)`}
          />
        )
      case 'number':
        return <input {...fieldProps} type="number" />
      default:
        return <input {...fieldProps} type="text" />
    }
  }

  return (
    <div className="card">
      <div className="flex items-center mb-6">
        <Icon className="h-8 w-8 text-primary-600 mr-3" />
        <div>
          <h3 className="text-lg font-semibold text-gray-900">{config.title}</h3>
          <p className="text-sm text-gray-600">{config.description}</p>
        </div>
      </div>

      <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
        {/* Task Type Selection */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Task Type
          </label>
          <select
            {...register('task_type', { required: true })}
            className="input-field"
          >
            <option value="">Select a task</option>
            {config.taskTypes.map(task => (
              <option key={task.value} value={task.value}>
                {task.label}
              </option>
            ))}
          </select>
          {errors.task_type && (
            <p className="mt-1 text-sm text-danger-600">Task type is required</p>
          )}
        </div>

        {/* Dynamic Fields */}
        {selectedTaskType && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {config.fields.map(field => (
              <div key={field.name}>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  {field.label}
                </label>
                {renderField(field)}
                {errors[field.name] && (
                  <p className="mt-1 text-sm text-danger-600">
                    {field.label} is required
                  </p>
                )}
              </div>
            ))}
          </div>
        )}

        {/* Submit Button */}
        <div className="flex justify-end pt-4">
          <button
            type="submit"
            disabled={loading || !selectedTaskType}
            className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
          >
            {loading ? (
              <>
                <div className="loading-spinner mr-2"></div>
                Processing...
              </>
            ) : (
              <>
                <PlayIcon className="h-4 w-4 mr-2" />
                Run {config.title}
              </>
            )}
          </button>
        </div>
      </form>

      {/* Results */}
      {result && <AgentResponse result={result} agentType={agentType} />}
    </div>
  )
}

export default AgentForm