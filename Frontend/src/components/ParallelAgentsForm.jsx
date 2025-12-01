import React, { useState } from 'react';
import { agentAPI } from '../services/api';
import { useAuth } from '../hooks/useAuth';
import { useNavigate } from 'react-router-dom';

const ErrorSection = ({ errors }) => {
  const [showErrors, setShowErrors] = useState(false);
  
  if (!errors || Object.keys(errors).length === 0) return null;
  
  return (
    <div className="bg-red-50/80 border border-red-200 rounded-2xl shadow-lg backdrop-blur-sm">
      <button
        onClick={() => setShowErrors(!showErrors)}
        className="w-full p-4 text-left flex items-center justify-between hover:bg-red-100/50 transition-colors rounded-2xl"
      >
        <span className="text-red-700 font-medium">Agent Errors (for debugging)</span>
        <span className="text-red-500">{showErrors ? '−' : '+'}</span>
      </button>
      {showErrors && (
        <div className="px-4 pb-4 space-y-2">
          {Object.entries(errors).map(([agent, error]) => (
            <div key={agent} className="bg-white/60 p-3 rounded-lg border border-red-200/30">
              <div className="text-red-800 font-mono text-xs">
                <strong className="text-red-900">{agent}:</strong> {error}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

const ParallelAgentsForm = () => {
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();
  
  React.useEffect(() => {
    if (!isAuthenticated) {
      navigate('/');
    }
  }, [isAuthenticated, navigate]);
  
  const [formData, setFormData] = useState({
    user_goals: [''],
    user_data: {
      skills: [],
      experience_years: '',
      current_role: '',
      age: '',
      interests: [],
      income: '',
      expenses: '',
      activity_level: 'moderate',
      learning_style: 'hands_on'
    },
    task_types: {
      career: 'milestone_analysis',
      wellness: 'goal_planning',
      learning: 'skill_development'
    },
    parameters: {
      time_horizon: '6_months',
      priority: 'high'
    }
  });

  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [validationErrors, setValidationErrors] = useState({});
  const [currentStep, setCurrentStep] = useState(1);

  const validateForm = () => {
    const errors = {};
    
    const validGoals = formData.user_goals.filter(goal => goal.trim() !== '');
    if (validGoals.length === 0) {
      errors.goals = 'Please add at least one goal';
    }
    
    if (!formData.user_data.age || formData.user_data.age < 16 || formData.user_data.age > 100) {
      errors.age = 'Please enter a valid age (16-100)';
    }
    if (!formData.user_data.current_role?.trim()) {
      errors.current_role = 'Please enter your current role';
    }
    if (!formData.user_data.experience_years || formData.user_data.experience_years < 0) {
      errors.experience_years = 'Please enter years of experience';
    }
    if (!formData.user_data.income || formData.user_data.income < 0) {
      errors.income = 'Please enter your annual income';
    }
    if (!formData.user_data.expenses || formData.user_data.expenses < 0) {
      errors.expenses = 'Please enter your monthly expenses';
    }
    
    return errors;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    const errors = validateForm();
    setValidationErrors(errors);
    
    if (Object.keys(errors).length > 0) {
      setError('Please fill in all required fields correctly');
      return;
    }
    
    setLoading(true);
    setError('');
    
    try {
      const response = await agentAPI.parallel(formData);
      setResults(response);
      setCurrentStep(2);
    } catch (err) {
      setError(err.message || 'Failed to run parallel agents');
    } finally {
      setLoading(false);
    }
  };

  const updateGoal = (index, value) => {
    const newGoals = [...formData.user_goals];
    newGoals[index] = value;
    setFormData({ ...formData, user_goals: newGoals });
  };

  const addGoal = () => {
    setFormData({
      ...formData,
      user_goals: [...formData.user_goals, '']
    });
  };

  const removeGoal = (index) => {
    const newGoals = formData.user_goals.filter((_, i) => i !== index);
    setFormData({ ...formData, user_goals: newGoals });
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-pink-50 py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-white/70 backdrop-blur-lg rounded-3xl border border-white/20 shadow-2xl p-8">
          <div className="text-center mb-12">
            <div className="flex items-center justify-center mb-6">
              <div className={`flex items-center justify-center w-8 h-8 rounded-full text-sm font-semibold ${
                currentStep >= 1 ? 'bg-purple-600 text-white' : 'bg-gray-200 text-gray-600'
              }`}>
                1
              </div>
              <div className={`w-16 h-1 mx-2 ${
                currentStep >= 2 ? 'bg-purple-600' : 'bg-gray-200'
              }`}></div>
              <div className={`flex items-center justify-center w-8 h-8 rounded-full text-sm font-semibold ${
                currentStep >= 2 ? 'bg-purple-600 text-white' : 'bg-gray-200 text-gray-600'
              }`}>
                2
              </div>
            </div>
            <h1 className="text-5xl font-bold text-gray-900 mb-4 tracking-tight">
              {currentStep === 1 ? 'Configure Your Profile' : 'AI Analysis Results'}
            </h1>
            <p className="text-gray-600 text-xl leading-relaxed max-w-3xl mx-auto">
              {currentStep === 1 
                ? 'Tell us about yourself to get personalized AI recommendations'
                : 'Your comprehensive analysis from our AI agents'
              }
            </p>
          </div>

      {currentStep === 1 && (
      <form onSubmit={handleSubmit} className="space-y-10">
        {/* Goals Section */}
        <div className="bg-white/70 backdrop-blur-lg rounded-3xl border border-white/20 shadow-2xl p-8 mb-8">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h3 className="text-3xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent mb-2">
                Your Goals
              </h3>
              <p className="text-gray-600">Define what you want to achieve</p>
            </div>
            <div className="text-sm text-gray-500">
              {formData.user_goals.filter(g => g.trim()).length} goals added
            </div>
          </div>
          {validationErrors.goals && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-3 mb-4">
              <p className="text-red-600 text-sm">{validationErrors.goals}</p>
            </div>
          )}
          {formData.user_goals.map((goal, index) => (
            <div key={index} className="flex gap-2 mb-3">
              <input
                type="text"
                value={goal}
                onChange={(e) => updateGoal(index, e.target.value)}
                className={`flex-1 px-4 py-3 bg-white/50 border rounded-xl text-gray-700 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200 ${
                  validationErrors.goals ? 'border-red-300' : 'border-gray-200'
                }`}
                placeholder="e.g., Get promoted to senior developer"
              />
              <button
                type="button"
                onClick={() => removeGoal(index)}
                className="px-4 py-3 bg-red-50/80 text-red-600 rounded-xl hover:bg-red-100/80 transition-all duration-200 shadow-sm hover:shadow-md backdrop-blur-sm border border-red-200/50"
              >
                ✕
              </button>
            </div>
          ))}
          <button
            type="button"
            onClick={addGoal}
            className="px-6 py-3 bg-purple-100/80 text-purple-700 rounded-xl hover:bg-purple-200/80 font-semibold transition-all duration-200 shadow-sm hover:shadow-md flex items-center gap-2 backdrop-blur-sm border border-purple-200/50"
          >
            <span className="text-lg">+</span> Add Goal
          </button>
        </div>

        {/* User Data Section */}
        <div className="grid md:grid-cols-2 gap-8">
          <div className="bg-white/70 backdrop-blur-lg rounded-3xl border border-white/20 shadow-2xl p-8">
            <h3 className="text-3xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent mb-2">
              Personal Info
            </h3>
            <p className="text-gray-600 mb-6">Tell us about yourself</p>
            <div className="space-y-6">
              <div>
                <input
                  type="number"
                  value={formData.user_data.age}
                  onChange={(e) => setFormData({
                    ...formData,
                    user_data: { ...formData.user_data, age: e.target.value }
                  })}
                  className={`w-full px-4 py-3 bg-white/50 border rounded-xl text-gray-700 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200 ${
                    validationErrors.age ? 'border-red-300' : 'border-gray-200'
                  }`}
                  placeholder="Age"
                />
                {validationErrors.age && (
                  <p className="text-red-600 text-sm mt-1">{validationErrors.age}</p>
                )}
              </div>
              <div>
                <input
                  type="text"
                  value={formData.user_data.current_role}
                  onChange={(e) => setFormData({
                    ...formData,
                    user_data: { ...formData.user_data, current_role: e.target.value }
                  })}
                  className={`w-full px-4 py-3 bg-white/50 border rounded-xl text-gray-700 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200 ${
                    validationErrors.current_role ? 'border-red-300' : 'border-gray-200'
                  }`}
                  placeholder="e.g., Software Developer"
                />
                {validationErrors.current_role && (
                  <p className="text-red-600 text-sm mt-1">{validationErrors.current_role}</p>
                )}
              </div>
              <div>
                <input
                  type="number"
                  value={formData.user_data.experience_years}
                  onChange={(e) => setFormData({
                    ...formData,
                    user_data: { ...formData.user_data, experience_years: e.target.value }
                  })}
                  className={`w-full px-4 py-3 bg-white/50 border rounded-xl text-gray-700 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200 ${
                    validationErrors.experience_years ? 'border-red-300' : 'border-gray-200'
                  }`}
                  placeholder="Years of Experience"
                />
                {validationErrors.experience_years && (
                  <p className="text-red-600 text-sm mt-1">{validationErrors.experience_years}</p>
                )}
              </div>
            </div>
          </div>

          <div className="bg-white/70 backdrop-blur-lg rounded-3xl border border-white/20 shadow-2xl p-8">
            <h3 className="text-3xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent mb-2">
              Financial Info
            </h3>
            <p className="text-gray-600 mb-6">Your financial situation</p>
            <div className="space-y-6">
              <div>
                <input
                  type="text"
                  inputMode="numeric"
                  pattern="[0-9]*"
                  value={formData.user_data.income}
                  onChange={(e) => {
                    const value = e.target.value.replace(/[^0-9]/g, '');
                    setFormData({
                      ...formData,
                      user_data: { ...formData.user_data, income: value }
                    });
                  }}
                  className={`w-full px-4 py-3 bg-white/50 border rounded-xl text-gray-700 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200 ${
                    validationErrors.income ? 'border-red-300' : 'border-gray-200'
                  }`}
                  placeholder="Annual Income ($)"
                />
                {validationErrors.income && (
                  <p className="text-red-600 text-sm mt-1">{validationErrors.income}</p>
                )}
              </div>
              <div>
                <input
                  type="text"
                  inputMode="numeric"
                  pattern="[0-9]*"
                  value={formData.user_data.expenses}
                  onChange={(e) => {
                    const value = e.target.value.replace(/[^0-9]/g, '');
                    setFormData({
                      ...formData,
                      user_data: { ...formData.user_data, expenses: value }
                    });
                  }}
                  className={`w-full px-4 py-3 bg-white/50 border rounded-xl text-gray-700 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all duration-200 ${
                    validationErrors.expenses ? 'border-red-300' : 'border-gray-200'
                  }`}
                  placeholder="Monthly Expenses ($)"
                />
                {validationErrors.expenses && (
                  <p className="text-red-600 text-sm mt-1">{validationErrors.expenses}</p>
                )}
              </div>
            </div>
          </div>
        </div>

        <div className="pt-8 flex justify-center">
          <button
            type="submit"
            disabled={loading}
            className="px-12 py-4 bg-gradient-to-r from-purple-600 to-pink-600 text-white font-semibold rounded-xl hover:from-purple-700 hover:to-pink-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 shadow-lg hover:shadow-xl transform hover:scale-105 text-lg"
          >
            {loading ? (
              <div className="flex items-center gap-3">
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                <span>Analyzing Your Profile...</span>
              </div>
            ) : (
              <div className="flex items-center gap-2">
                <span>Generate AI Analysis</span>
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                </svg>
              </div>
            )}
          </button>
        </div>
      </form>
      )}

      {error && (
        <div className="mt-8 p-6 bg-red-50/80 border border-red-200 rounded-2xl shadow-lg backdrop-blur-sm">
          <div className="flex items-start gap-3">
            <div className="w-8 h-8 bg-red-100 rounded-full flex items-center justify-center flex-shrink-0">
              <span className="text-red-600 text-sm">!</span>
            </div>
            <div>
              <h4 className="text-lg font-semibold text-red-800 mb-1">Request Failed</h4>
              <p className="text-red-700 text-sm leading-relaxed">{error}</p>
            </div>
          </div>
        </div>
      )}

      {currentStep === 2 && results && (
        <div className="mb-8 flex justify-center">
          <button
            onClick={() => {
              setCurrentStep(1);
              setResults(null);
              setValidationErrors({});
              setError('');
            }}
            className="px-6 py-3 bg-white/70 border border-gray-200 text-gray-700 font-medium rounded-xl hover:bg-white/90 transition-all duration-200 shadow-sm"
          >
            ← Edit Profile
          </button>
        </div>
      )}

      {currentStep === 2 && results && (
        <div className="mt-16 space-y-12">
          <div className="bg-white/70 backdrop-blur-sm rounded-2xl border border-white/20 shadow-lg p-6">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 bg-gradient-to-r from-purple-100 to-pink-100 rounded-xl flex items-center justify-center">
                  <svg className="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-gray-900">Analysis Complete</h3>
                  <p className="text-gray-600 text-sm">All agents have finished processing</p>
                </div>
              </div>
              <div className="text-right">
                <div className="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-purple-100 text-purple-800 mb-2">
                  Success
                </div>
                <div className="text-sm text-gray-500">{results.execution_time?.toFixed(2)}s execution</div>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 auto-rows-fr">
            {/* Career Results */}
            {results.results?.career && (
              <div className="bg-white/70 backdrop-blur-sm rounded-2xl border border-white/20 shadow-lg p-6 h-full flex flex-col justify-between hover:shadow-xl transition-all duration-300">
                <div className="w-12 h-12 bg-gradient-to-r from-purple-100 to-pink-100 rounded-xl flex items-center justify-center mb-4">
                  <svg className="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                </div>
                <h4 className="text-lg font-semibold text-gray-900 mb-2">Career Development</h4>
                
                <div className="flex-1 space-y-4 min-h-[400px]">
                  {results.results.career.situation_summary && (
                    <p className="text-gray-600 text-sm leading-relaxed">{results.results.career.situation_summary}</p>
                  )}
                  
                  <div>
                    <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-3">Target Roles</div>
                    <div className="space-y-2">
                      {results.results.career.target_roles?.map((role, i) => (
                        <div key={i} className="p-3 bg-purple-50/80 rounded-xl border border-purple-100 hover:bg-purple-100/80 transition-all duration-200 hover:scale-[1.02]">
                          <div className="font-semibold text-purple-900 mb-1">{role.title}</div>
                          <div className="text-sm text-purple-700 leading-relaxed">{role.why_fit}</div>
                        </div>
                      ))}
                    </div>
                  </div>
                  
                  {results.results.career.key_skills && (
                    <div>
                      <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-3">Key Skills to Strengthen</div>
                      <div className="space-y-2">
                        {results.results.career.key_skills.slice(0, 3).map((skill, i) => (
                          <div key={i} className="p-2 bg-purple-50/80 rounded-lg border border-purple-100">
                            <div className="text-sm text-purple-800 font-medium">{skill}</div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                  
                  <div>
                    <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-3">Strategic Roadmap</div>
                    <div className="bg-gray-50/80 p-4 rounded-xl border border-gray-200">
                      {results.results.career.roadmap_summary ? (
                        <div className="space-y-2">
                          {results.results.career.roadmap_summary.slice(0, 3).map((action, i) => (
                            <div key={i} className="flex items-start gap-2 text-sm text-gray-700">
                              <span className="text-purple-500 mt-1 flex-shrink-0">•</span>
                              <span>{action}</span>
                            </div>
                          ))}
                        </div>
                      ) : (
                        <div className="text-sm text-gray-700">
                          <span className="font-semibold">{results.results.career.tasks?.length || 0}</span> strategic actions planned
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Wellness Results */}
            {results.results?.wellness && (
              <div className="bg-white/70 backdrop-blur-sm rounded-2xl border border-white/20 shadow-lg p-6 h-full flex flex-col justify-between hover:shadow-xl transition-all duration-300">
                <div className="w-12 h-12 bg-gradient-to-r from-purple-100 to-pink-100 rounded-xl flex items-center justify-center mb-4">
                  <svg className="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                  </svg>
                </div>
                <h4 className="text-lg font-semibold text-gray-900 mb-2">Wellness Plan</h4>
                
                <div className="flex-1 space-y-4 min-h-[400px]">
                  {results.results.wellness.assessment && (
                    <p className="text-gray-600 text-sm leading-relaxed">{results.results.wellness.assessment}</p>
                  )}
                  
                  {results.results.wellness.health_metrics && (
                    <div>
                      <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-3">Health Metrics</div>
                      <div className="bg-purple-50/80 p-4 rounded-xl border border-purple-100">
                        <div className="grid grid-cols-2 gap-4 text-sm">
                          <div className="flex flex-col">
                            <span className="text-gray-600 text-xs uppercase tracking-wide">Status</span>
                            <span className="font-semibold text-purple-800">{results.results.wellness.health_metrics.status}</span>
                          </div>
                          <div className="flex flex-col">
                            <span className="text-gray-600 text-xs uppercase tracking-wide">Target Calories</span>
                            <span className="font-semibold text-purple-800">{results.results.wellness.health_metrics.target_calories}</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  )}
                  
                  <div>
                    <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-3">Weekly Plan</div>
                    <div className="bg-gray-50/80 p-4 rounded-xl border border-gray-200 min-h-[160px]">
                      <div className="space-y-2 text-sm text-gray-700 max-h-40 overflow-y-auto scrollbar-thin scrollbar-thumb-gray-300 scrollbar-track-gray-100">
                        {results.results.wellness.weekly_plan?.map((day, i) => (
                          <div key={i} className="flex items-start gap-3 py-1">
                            <span className="text-purple-500 mt-1 flex-shrink-0">•</span>
                            <span className="leading-relaxed" dangerouslySetInnerHTML={{__html: day.replace(/\*\*(.*?)\*\*/g, '<strong class="text-gray-900">$1</strong>')}} />
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Learning Results */}
            {results.results?.learning && (
              <div className="bg-white/70 backdrop-blur-sm rounded-2xl border border-white/20 shadow-lg p-6 h-full flex flex-col justify-between hover:shadow-xl transition-all duration-300">
                <div className="w-12 h-12 bg-gradient-to-r from-purple-100 to-pink-100 rounded-xl flex items-center justify-center mb-4">
                  <svg className="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                  </svg>
                </div>
                <h4 className="text-lg font-semibold text-gray-900 mb-2">Learning Path</h4>
                
                <div className="flex-1 space-y-4 min-h-[400px]">
                  {results.results.learning.profile_summary && (
                    <p className="text-gray-600 text-sm leading-relaxed">{results.results.learning.profile_summary}</p>
                  )}
                  
                  <div>
                    <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-3">Learning Phases</div>
                    <div className="space-y-2">
                      {results.results.learning.learning_phases?.slice(0, 2).map((phase, i) => (
                        <div key={i} className="p-3 bg-purple-50/80 rounded-xl border border-purple-100 hover:bg-purple-100/80 transition-all duration-200 hover:scale-[1.02]">
                          <div className="font-semibold text-purple-900 mb-1">{phase.name} <span className="text-sm font-normal text-purple-700">({phase.duration})</span></div>
                          <div className="text-sm text-purple-700 leading-relaxed">{phase.focus}</div>
                        </div>
                      ))}
                    </div>
                  </div>
                  
                  <div>
                    <div className="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-3">Course Recommendations</div>
                    <div className="space-y-2">
                      {(results.results.learning.courses || results.results.learning.course_recommendations || []).slice(0, 3).map((course, i) => (
                        <div key={i} className="p-2 bg-purple-50/80 rounded-lg border border-purple-100">
                          <div className="font-medium text-purple-900 text-sm">{course.title}</div>
                          <div className="text-xs text-purple-700">{course.platform} - {course.why_relevant}</div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>

          <ErrorSection errors={results.errors} />
        </div>
      )}
        </div>
      </div>
    </div>
  );
};

export default ParallelAgentsForm;