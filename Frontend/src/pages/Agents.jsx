import { useState } from 'react'
import AgentForm from '../components/AgentForm'
import CareerAgentForm from '../components/CareerAgentForm'
import FinanceAgentForm from '../components/FinanceAgentForm'
import WellnessAgentForm from '../components/WellnessAgentForm'
import LearningAgentForm from '../components/LearningAgentForm'
import { 
  BriefcaseIcon, 
  BanknotesIcon, 
  HeartIcon, 
  AcademicCapIcon 
} from '@heroicons/react/24/outline'

const agents = [
  {
    id: 'career',
    name: 'Career Agent',
    description: 'Get personalized job recommendations, skill analysis, and career guidance',
    icon: BriefcaseIcon,
    color: 'bg-purple-400'
  },
  {
    id: 'finance',
    name: 'Finance Agent',
    description: 'Receive budget analysis, investment advice, and financial planning',
    icon: BanknotesIcon,
    color: 'bg-pink-400'
  },
  {
    id: 'wellness',
    name: 'Wellness Agent',
    description: 'Get fitness plans, nutrition advice, and health assessments',
    icon: HeartIcon,
    color: 'bg-indigo-400'
  },
  {
    id: 'learning',
    name: 'Learning Agent',
    description: 'Find courses, analyze skill gaps, and create learning paths',
    icon: AcademicCapIcon,
    color: 'bg-violet-400'
  }
]

const Agents = () => {
  const [selectedAgent, setSelectedAgent] = useState(null)
  const [results, setResults] = useState({})

  const handleAgentResult = (agentId, result) => {
    setResults(prev => ({
      ...prev,
      [agentId]: result
    }))
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Page Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent mb-2">
          {selectedAgent ? agents.find(a => a.id === selectedAgent)?.name : 'AI Agents'}
        </h1>
        <p className="text-gray-600">
          {selectedAgent 
            ? agents.find(a => a.id === selectedAgent)?.description
            : 'Choose an AI agent to get personalized recommendations and guidance'
          }
        </p>
      </div>

      {/* Main Content Card */}
      <div className="backdrop-blur-sm bg-white/70 rounded-3xl shadow-xl border border-white/20">
        {!selectedAgent ? (
          /* Agent Selection */
          <div className="p-8">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {agents.map((agent) => {
                const Icon = agent.icon
                const hasResult = results[agent.id]
                
                return (
                  <div
                    key={agent.id}
                    onClick={() => setSelectedAgent(agent.id)}
                    className="border border-gray-200 rounded-2xl p-6 hover:shadow-md hover:border-purple-300 cursor-pointer transition-all duration-200 hover:scale-[1.02] relative bg-white/50"
                  >
                    {hasResult && (
                      <div className="absolute top-4 right-4">
                        <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                      </div>
                    )}
                    
                    <div className="flex items-start space-x-4">
                      <div className={`p-3 rounded-xl ${agent.color}`}>
                        <Icon className="h-8 w-8 text-white" />
                      </div>
                      <div className="flex-1">
                        <h3 className="text-lg font-semibold text-gray-900 mb-2">
                          {agent.name}
                        </h3>
                        <p className="text-gray-600 text-sm mb-4">
                          {agent.description}
                        </p>
                        <div className="flex items-center text-purple-600 text-sm font-medium">
                          <span>Get Started</span>
                          <svg className="ml-2 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                          </svg>
                        </div>
                      </div>
                    </div>
                  </div>
                )
              })}
            </div>
            
            {/* Results Summary */}
            {Object.keys(results).length > 0 && (
              <div className="mt-12 pt-8 border-t border-gray-200">
                <h2 className="text-xl font-semibold text-gray-900 mb-6">Recent Results</h2>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {Object.entries(results).map(([agentId, result]) => {
                    const agent = agents.find(a => a.id === agentId)
                    const Icon = agent.icon
                    
                    return (
                      <div key={agentId} className="border border-gray-200 rounded-xl p-4 bg-gray-50">
                        <div className="flex items-center mb-3">
                          <div className={`p-2 rounded-lg ${agent.color} mr-3`}>
                            <Icon className="h-4 w-4 text-white" />
                          </div>
                          <div>
                            <h3 className="font-medium text-gray-900 text-sm">{agent.name}</h3>
                            <p className="text-xs text-gray-500">Status: {result.status}</p>
                          </div>
                        </div>
                        
                        <div className="flex justify-between items-center">
                          <button
                            onClick={() => setSelectedAgent(agentId)}
                            className="text-purple-600 hover:text-purple-700 text-sm font-medium"
                          >
                            Run Again
                          </button>
                          <button
                            onClick={() => {
                              const newResults = { ...results }
                              delete newResults[agentId]
                              setResults(newResults)
                            }}
                            className="text-gray-400 hover:text-gray-600 text-sm"
                          >
                            Clear
                          </button>
                        </div>
                      </div>
                    )
                  })}
                </div>
              </div>
            )}
          </div>
        ) : (
          /* Selected Agent */
          <div className="p-8">
            {/* Back Link */}
            <button
              onClick={() => setSelectedAgent(null)}
              className="flex items-center text-purple-600 hover:text-purple-700 font-medium mb-6 transition-colors duration-200"
            >
              <svg className="mr-2 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
              </svg>
              Back to Agents
            </button>
            
            {/* Agent Form */}
            {selectedAgent === 'career' ? (
              <CareerAgentForm
                onResult={(result) => handleAgentResult(selectedAgent, result)}
              />
            ) : selectedAgent === 'finance' ? (
              <FinanceAgentForm
                onResult={(result) => handleAgentResult(selectedAgent, result)}
              />
            ) : selectedAgent === 'wellness' ? (
              <WellnessAgentForm
                onResult={(result) => handleAgentResult(selectedAgent, result)}
              />
            ) : selectedAgent === 'learning' ? (
              <LearningAgentForm
                onResult={(result) => handleAgentResult(selectedAgent, result)}
              />
            ) : (
              <AgentForm
                agentType={selectedAgent}
                onResult={(result) => handleAgentResult(selectedAgent, result)}
              />
            )}
          </div>
        )}
      </div>
    </div>
  )
}

export default Agents