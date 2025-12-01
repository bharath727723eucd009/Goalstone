/**
 * Goalie AI chatbot API client - isolated from existing APIs
 */
import axios from 'axios'

const GOALIE_API_BASE = 'http://localhost:8080/goalie'

// Create separate axios instance for Goalie to avoid conflicts
const goalieClient = axios.create({
  baseURL: GOALIE_API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000, // 10 second timeout
})

export async function chatWithGoalie({ message, pagePath = '/', historySnippet = [] }) {
  try {
    console.log('Goalie API: Sending request to /goalie/chat', { message, pagePath })
    
    const response = await goalieClient.post('/chat', {
      message,
      pagePath,
      history: historySnippet
    })
    
    console.log('Goalie API: Received response', response.data)
    
    // Ensure we have a valid response
    if (response.data && response.data.reply) {
      return response.data.reply
    } else {
      console.error('Goalie API: Invalid response format', response.data)
      throw new Error('Invalid response format')
    }
  } catch (error) {
    console.error('Goalie chat error:', error)
    console.error('Error details:', {
      status: error.response?.status,
      statusText: error.response?.statusText,
      data: error.response?.data,
      code: error.code
    })
    
    // Return user-friendly error message based on error type
    if (error.code === 'ECONNABORTED') {
      return "I'm taking a bit longer to respond. Please try again."
    } else if (error.response?.status >= 500) {
      return "I'm experiencing some technical difficulties. Please try again in a moment."
    } else if (error.response?.status === 404) {
      return "I'm not available right now. Please try again later."
    } else if (error.code === 'ECONNREFUSED' || error.code === 'ERR_NETWORK') {
      return "I can't connect to the server right now. Please try again."
    } else if (!navigator.onLine) {
      return "You appear to be offline. Please check your connection and try again."
    } else {
      return "Sorry, I couldn't reach the server. Please try again."
    }
  }
}