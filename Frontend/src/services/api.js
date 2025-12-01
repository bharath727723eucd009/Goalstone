import axios from 'axios'
import toast from 'react-hot-toast'

const API_BASE_URL = 'http://localhost:8080/api/v1'

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Token management
const getToken = () => localStorage.getItem('token')
const setToken = (token) => localStorage.setItem('token', token)
const removeToken = () => localStorage.removeItem('token')

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = getToken()
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => Promise.reject(error)
)

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Don't redirect on login attempts - let component handle it
      if (!error.config?.url?.includes('/auth/login') && !error.config?.url?.includes('/agents/career')) {
        removeToken()
        window.location.href = '/'
        toast.error('Session expired. Please login again.')
      }
    } else if (error.response?.status >= 500) {
      toast.error('Server error. Please try again later.')
    }
    return Promise.reject(error)
  }
)

// Auth API
export const authAPI = {
  login: async (credentials) => {
    console.log('Login attempt with:', credentials)
    console.log('API URL:', API_BASE_URL)
    try {
      const response = await api.post('/auth/login', credentials)
      console.log('Login response:', response.data)
      if (response.data.access_token) {
        setToken(response.data.access_token)
        localStorage.setItem('user', JSON.stringify(response.data.user))
      }
      return response.data
    } catch (error) {
      console.error('Login error:', error)
      console.error('Error response:', error.response?.data)
      console.error('Error status:', error.response?.status)
      throw error
    }
  },
  
  register: async (userData) => {
    console.log('Register attempt with:', userData)
    try {
      const response = await api.post('/auth/register', userData)
      console.log('Register response:', response.data)
      return response.data
    } catch (error) {
      console.error('Register error:', error)
      throw error
    }
  },
  
  logout: () => {
    removeToken()
    localStorage.removeItem('user')
  },
  
  getCurrentUser: async () => {
    const token = getToken()
    if (!token) {
      throw new Error('No token found')
    }
    
    try {
      const response = await api.get('/auth/me')
      return response.data
    } catch (error) {
      removeToken()
      localStorage.removeItem('user')
      throw new Error('Invalid session')
    }
  }
}

// Agent API
export const agentAPI = {
  career: async (data) => {
    const response = await api.post('/agents/career', data)
    return response.data
  },
  
  saveCareerPlan: async (roadmap) => {
    const response = await api.post('/career/plan/save', { roadmap })
    return response.data
  },
  
  replanCareer: async (completedTasks, feedback = '') => {
    const response = await api.post('/career/plan/replan', { 
      completed_tasks: completedTasks, 
      feedback 
    })
    return response.data
  },
  
  finance: async (data) => {
    const response = await api.post('/agents/finance', data)
    return response.data
  },
  
  wellness: async (data) => {
    const response = await api.post('/agents/wellness', data)
    return response.data
  },
  
  learning: async (data) => {
    const response = await api.post('/agents/learning', data)
    return response.data
  },
  
  getAgentHealth: async (agentType) => {
    const response = await api.get(`/agents/${agentType}/health`)
    return response.data
  },
  
  parallel: async (data) => {
    const response = await api.post('/agents/parallel', data)
    return response.data
  },
  
  updateRoadmapProgress: async (taskId, completed) => {
    const response = await api.post('/career/roadmap/progress', { task_id: taskId, completed })
    return response.data
  },
  
  getRoadmapProgress: async () => {
    const response = await api.get('/career/roadmap/progress')
    return response.data
  },
  
  saveRoadmapProgress: async (completedTaskIds) => {
    const promises = completedTaskIds.map(taskId => 
      api.post('/career/roadmap/progress', { task_id: taskId, completed: true })
    )
    const responses = await Promise.all(promises)
    return responses.map(r => r.data)
  },
  
  updateCourseProgress: async (courseTitle, completed) => {
    const response = await api.post('/career/course/progress', { course_title: courseTitle, completed })
    return response.data
  },
  
  getCourseProgress: async () => {
    const response = await api.get('/career/course/progress')
    return response.data
  }
}

// Data API
export const dataAPI = {
  getUserProfile: async () => {
    const response = await api.get('/data/users/profile')
    return response.data
  },
  
  updateUserProfile: async (profileData) => {
    const response = await api.post('/data/users/profile', profileData)
    return response.data
  },
  
  getMilestones: async (status = null) => {
    const params = status ? { status } : {}
    const response = await api.get('/data/milestones', { params })
    return response.data
  },
  
  createMilestone: async (milestoneData) => {
    const response = await api.post('/data/milestones', milestoneData)
    return response.data
  },
  
  updateMilestone: async (milestoneId, updates) => {
    const response = await api.put(`/data/milestones/${milestoneId}`, updates)
    return response.data
  },
  
  getAgentHistory: async (agentType = null, limit = 10) => {
    const params = { limit }
    if (agentType) params.agent_type = agentType
    const response = await api.get('/data/agent-outputs', { params })
    return response.data
  },
  
  getUserProgress: async () => {
    const response = await api.get('/data/progress')
    return response.data
  },
  
  getGoalsSummary: async () => {
    const response = await api.get('/goals/summary')
    return response.data
  },
  
  createGoal: async (goalData) => {
    const response = await api.post('/goals', goalData)
    return response.data
  },
  
  getUserStats: async () => {
    const response = await api.get('/user/stats')
    return response.data
  }
}

// System API
export const systemAPI = {
  getSystemStatus: async () => {
    const response = await api.get('/status')
    return response.data
  },
  
  getMetrics: async () => {
    const response = await axios.get('http://localhost:8000/metrics')
    return response.data
  }
}

// Profile API
export const profileAPI = {
  getProfile: async () => {
    const response = await api.get('/users/me')
    return response.data
  },
  
  updateProfile: async (profileData) => {
    const response = await api.put('/users/me', profileData)
    return response.data
  },
  
  updatePreferences: async (preferences) => {
    const response = await api.put('/users/me/preferences', preferences)
    return response.data
  },
  
  changePassword: async (passwordData) => {
    const response = await api.post('/users/me/password', passwordData)
    return response.data
  },
  
  uploadAvatar: async (formData) => {
    const response = await api.post('/users/me/avatar', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    return response.data
  }
}

export { getToken, setToken, removeToken }
export default api