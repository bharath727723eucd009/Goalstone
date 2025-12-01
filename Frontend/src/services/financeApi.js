import { agentAPI } from './api'

export const getFinancePlan = async (formData) => {
  try {
    const userData = {
      monthly_income: parseInt(formData.monthly_income) || 0,
      fixed_expenses: parseInt(formData.fixed_expenses) || 0,
      variable_expenses: parseInt(formData.variable_expenses) || 0,
      existing_savings: parseInt(formData.existing_savings) || 0,
      financial_priority: formData.financial_priority,
      extra_notes: formData.extra_notes || ''
    }
    
    const response = await agentAPI.finance({
      user_data: userData,
      task_type: 'financial_planning',
      parameters: {}
    })
    
    // Parse and structure the response
    return parseFinanceResponse(response, userData)
  } catch (error) {
    console.error('Finance API error:', error)
    throw error
  }
}

const parseFinanceResponse = (response, userData) => {
  // If backend already returns structured data, use it
  if (response.monthlySummary) {
    return response
  }
  
  // Otherwise, create structured data from the input and response
  const { monthly_income, fixed_expenses, variable_expenses } = userData
  const totalExpenses = fixed_expenses + variable_expenses
  const suggestedSavings = Math.floor(monthly_income * 0.2)
  const safeToSpend = Math.max(monthly_income - totalExpenses - suggestedSavings, 0)
  
  return {
    monthlySummary: {
      income: monthly_income,
      totalExpenses,
      suggestedSavings,
      safeToSpend
    },
    allocation: {
      essentials: Math.min(Math.round((fixed_expenses / monthly_income) * 100), 100),
      lifestyle: Math.min(Math.round((variable_expenses / monthly_income) * 100), 100),
      savings: Math.min(Math.round((suggestedSavings / monthly_income) * 100), 100),
      buffer: Math.max(Math.round(((monthly_income - totalExpenses - suggestedSavings) / monthly_income) * 100), 0)
    },
    insights: generateInsights(userData, totalExpenses, suggestedSavings),
    goals: generateGoals(userData, totalExpenses),
    rawResponse: response
  }
}

const generateInsights = (userData, totalExpenses, suggestedSavings) => {
  const insights = []
  const { monthly_income, fixed_expenses, variable_expenses, financial_priority } = userData
  
  // Expense ratio insights
  const expenseRatio = (totalExpenses / monthly_income) * 100
  if (expenseRatio > 80) {
    insights.push("Your expenses are quite high relative to income. Consider reviewing variable expenses for savings opportunities.")
  } else if (expenseRatio < 50) {
    insights.push("Great job keeping expenses low! You have good potential for increased savings and investments.")
  }
  
  // Savings insights
  const savingsRatio = (suggestedSavings / monthly_income) * 100
  if (savingsRatio < 10) {
    insights.push("Try to save at least 10-15% of your income for financial security.")
  } else if (savingsRatio >= 20) {
    insights.push("Excellent savings rate! Consider diversifying into different investment options.")
  }
  
  // Priority-based insights
  switch (financial_priority) {
    case 'emergency_fund':
      insights.push("Focus on building an emergency fund covering 3-6 months of expenses before other investments.")
      break
    case 'debt_payoff':
      insights.push("Prioritize high-interest debt repayment to save on interest costs long-term.")
      break
    case 'save_for_goal':
      insights.push("Set up automatic transfers to a dedicated savings account for your specific goal.")
      break
    case 'increase_investments':
      insights.push("Consider systematic investment plans (SIPs) in mutual funds for long-term wealth building.")
      break
  }
  
  return insights.slice(0, 3) // Limit to 3 insights
}

const generateGoals = (userData, totalExpenses) => {
  const goals = []
  const { monthly_income, financial_priority, existing_savings } = userData
  
  // Emergency fund goal
  const emergencyFundTarget = totalExpenses * 6
  if (existing_savings < emergencyFundTarget) {
    goals.push(`Build emergency fund of ₹${emergencyFundTarget}`)
  }
  
  // Savings increase goal
  const currentSavingsRate = ((monthly_income - totalExpenses) / monthly_income) * 100
  if (currentSavingsRate < 25) {
    goals.push("Increase monthly savings rate by 5%")
  }
  
  // Priority-specific goals
  switch (financial_priority) {
    case 'debt_payoff':
      goals.push("Create a debt repayment plan with timeline")
      break
    case 'save_for_goal':
      goals.push("Set up dedicated savings account for your goal")
      break
    case 'increase_investments':
      goals.push("Start systematic investment plan (SIP)")
      break
    default:
      goals.push("Track expenses for better budgeting")
  }
  
  return goals.slice(0, 3) // Limit to 3 goals
}