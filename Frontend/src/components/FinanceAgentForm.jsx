import { useState, useEffect } from 'react'
import { useForm } from 'react-hook-form'
import { getFinancePlan } from '../services/financeApi'
import toast from 'react-hot-toast'

const useScrollReveal = () => {
  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('animate-fade-in-up')
          }
        })
      },
      { threshold: 0.1 }
    )

    const elements = document.querySelectorAll('.scroll-reveal')
    elements.forEach((el) => observer.observe(el))

    return () => observer.disconnect()
  }, [])
}

const FinanceAgentForm = ({ onResult }) => {
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const { register, handleSubmit, formState: { errors } } = useForm()
  
  useScrollReveal()

  const onSubmit = async (data) => {
    setLoading(true)
    setError(null)
    setResult(null)
    
    try {
      const result = await getFinancePlan(data)
      setResult(result)
      onResult(result)
      toast.success('Finance plan generated successfully!')
      
    } catch (error) {
      console.error('Finance agent error:', error)
      const errorMessage = error.response?.status === 401 
        ? 'Please login to use the Finance Agent'
        : 'Could not generate a plan. Please try again.'
      
      setError(errorMessage)
      toast.error(errorMessage)
    } finally {
      setLoading(false)
    }
  }



  return (
    <div className="bg-gradient-to-br from-pink-50 via-white to-purple-50 py-6">
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 max-w-5xl mx-auto px-4">
        
        <div className="scroll-reveal opacity-0 translate-y-8 transition-all duration-700 ease-out">
          <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-6">Financial Information</h2>
            
            <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Monthly Income *
                </label>
                <input
                  {...register('monthly_income', { 
                    required: 'Monthly income is required',
                    min: { value: 1, message: 'Income must be greater than 0' }
                  })}
                  type="number"
                  step="1"
                  min="1"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500 focus:border-transparent"
                  placeholder="50000"
                />
                <p className="text-xs text-gray-500 mt-1">Your total monthly income after taxes - rough estimates are fine</p>
                {errors.monthly_income && (
                  <p className="text-sm text-red-600 mt-1">{errors.monthly_income.message}</p>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Fixed Expenses
                </label>
                <input
                  {...register('fixed_expenses', {
                    min: { value: 0, message: 'Expenses cannot be negative' }
                  })}
                  type="number"
                  step="1"
                  min="0"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500 focus:border-transparent"
                  placeholder="25000"
                />
                <p className="text-xs text-gray-500 mt-1">Rent, EMIs, utilities, insurance - rough estimates are fine</p>
                {errors.fixed_expenses && (
                  <p className="text-sm text-red-600 mt-1">{errors.fixed_expenses.message}</p>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Variable Expenses
                </label>
                <input
                  {...register('variable_expenses', {
                    min: { value: 0, message: 'Expenses cannot be negative' }
                  })}
                  type="number"
                  step="1"
                  min="0"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500 focus:border-transparent"
                  placeholder="15000"
                />
                <p className="text-xs text-gray-500 mt-1">Food, travel, entertainment, shopping - rough estimates are fine</p>
                {errors.variable_expenses && (
                  <p className="text-sm text-red-600 mt-1">{errors.variable_expenses.message}</p>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Existing Savings/Investments
                </label>
                <input
                  {...register('existing_savings', {
                    min: { value: 0, message: 'Savings cannot be negative' }
                  })}
                  type="number"
                  step="1"
                  min="0"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500 focus:border-transparent"
                  placeholder="100000"
                />
                <p className="text-xs text-gray-500 mt-1">Current total savings and investments - rough estimates are fine</p>
                {errors.existing_savings && (
                  <p className="text-sm text-red-600 mt-1">{errors.existing_savings.message}</p>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Top Financial Priority *
                </label>
                <select
                  {...register('financial_priority', { required: 'Financial priority is required' })}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500 focus:border-transparent"
                >
                  <option value="">Select your priority</option>
                  <option value="emergency_fund">Build emergency fund</option>
                  <option value="debt_payoff">Pay off debt</option>
                  <option value="save_for_goal">Save for a goal</option>
                  <option value="increase_investments">Increase investments</option>
                </select>
                {errors.financial_priority && (
                  <p className="text-sm text-red-600 mt-1">{errors.financial_priority.message}</p>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Anything else about your money situation?
                </label>
                <textarea
                  {...register('extra_notes')}
                  rows="3"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-pink-500 focus:border-transparent"
                  placeholder="Any specific goals, concerns, or context..."
                />
                <p className="text-xs text-gray-500 mt-1">Optional - rough estimates are fine</p>
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full px-8 py-4 bg-gradient-to-r from-pink-600 to-purple-600 text-white font-semibold rounded-xl hover:from-pink-700 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 shadow-lg hover:shadow-xl transform hover:scale-105"
              >
                {loading ? (
                  <div className="flex items-center justify-center">
                    <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
                    Generating finance plan...
                  </div>
                ) : (
                  'Generate finance plan'
                )}
              </button>
            </form>
          </div>
        </div>

        <div className="scroll-reveal opacity-0 translate-y-8 transition-all duration-700 ease-out delay-200">
          <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-6">Finance Plan</h2>
            
            {loading ? (
              <div className="space-y-4">
                <div className="animate-pulse">
                  <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
                  <div className="h-4 bg-gray-200 rounded w-1/2 mb-4"></div>
                  <div className="h-20 bg-gray-200 rounded mb-4"></div>
                  <div className="h-4 bg-gray-200 rounded w-2/3"></div>
                </div>
              </div>
            ) : error ? (
              <div className="text-center py-12">
                <div className="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <svg className="w-8 h-8 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
                  </svg>
                </div>
                <p className="text-red-600 font-medium mb-2">Could not generate a plan</p>
                <p className="text-gray-500 text-sm">Please try again or check your inputs</p>
              </div>
            ) : !result ? (
              <div className="text-center py-12">
                <div className="w-16 h-16 bg-gradient-to-r from-pink-100 to-purple-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <svg className="w-8 h-8 text-pink-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1" />
                  </svg>
                </div>
                <p className="text-gray-500">Fill out the form to get your personalized finance plan</p>
              </div>

            ) : (
              <div className="space-y-6">
                {/* Monthly Summary */}
                <div className="bg-gradient-to-r from-green-50 to-blue-50 rounded-2xl p-6 border border-green-200">
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Monthly Summary</h3>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <p className="text-sm text-gray-600">Income</p>
                      <p className="text-xl font-bold text-green-600">₹{result.monthlySummary.income}</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600">Total Expenses</p>
                      <p className="text-xl font-bold text-red-600">₹{result.monthlySummary.totalExpenses}</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600">Suggested Savings</p>
                      <p className="text-xl font-bold text-blue-600">₹{result.monthlySummary.suggestedSavings}</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-600">Safe to Spend</p>
                      <p className="text-xl font-bold text-purple-600">₹{result.monthlySummary.safeToSpend}</p>
                    </div>
                  </div>
                </div>

                {/* Allocation */}
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Recommended Allocation</h3>
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="text-sm font-medium text-gray-700">Essentials</span>
                      <span className="text-sm font-bold text-gray-900">{result.allocation.essentials}%</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div className="bg-red-500 h-2 rounded-full" style={{width: `${result.allocation.essentials}%`}}></div>
                    </div>
                    
                    <div className="flex items-center justify-between">
                      <span className="text-sm font-medium text-gray-700">Lifestyle</span>
                      <span className="text-sm font-bold text-gray-900">{result.allocation.lifestyle}%</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div className="bg-yellow-500 h-2 rounded-full" style={{width: `${result.allocation.lifestyle}%`}}></div>
                    </div>
                    
                    <div className="flex items-center justify-between">
                      <span className="text-sm font-medium text-gray-700">Savings</span>
                      <span className="text-sm font-bold text-gray-900">{result.allocation.savings}%</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div className="bg-green-500 h-2 rounded-full" style={{width: `${result.allocation.savings}%`}}></div>
                    </div>
                  </div>
                </div>

                {/* Insights */}
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Key Insights</h3>
                  <ul className="space-y-2">
                    {result.insights.map((insight, index) => (
                      <li key={index} className="flex items-start">
                        <div className="w-2 h-2 bg-pink-500 rounded-full mt-2 mr-3 flex-shrink-0"></div>
                        <span className="text-sm text-gray-700">{insight}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                {/* Goals */}
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-4">Goal-based Suggestions</h3>
                  <div className="space-y-3">
                    {result.goals.map((goal, index) => (
                      <div key={index} className="bg-purple-50 rounded-xl p-4 border border-purple-200">
                        <p className="text-sm font-medium text-purple-900">{goal}</p>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Raw AI Response */}
                {result.rawResponse && typeof result.rawResponse === 'string' && (
                  <div className="bg-gray-50 rounded-xl p-4 border border-gray-200">
                    <h4 className="font-medium text-gray-900 mb-2">AI Response</h4>
                    <p className="text-sm text-gray-600 whitespace-pre-wrap">{result.rawResponse}</p>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default FinanceAgentForm