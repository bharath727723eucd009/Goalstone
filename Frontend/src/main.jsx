import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import App from './App'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <App />
      <Toaster 
        position="top-right"
        toastOptions={{
          duration: 4000,
          style: {
            background: 'rgba(255, 255, 255, 0.9)',
            backdropFilter: 'blur(10px)',
            border: '1px solid rgba(255, 255, 255, 0.2)',
            borderRadius: '16px',
            color: '#374151',
            boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
          },
          success: {
            style: {
              background: 'linear-gradient(135deg, rgba(147, 51, 234, 0.1), rgba(219, 39, 119, 0.1))',
              border: '1px solid rgba(147, 51, 234, 0.2)',
              color: '#7c3aed',
            },
            iconTheme: {
              primary: '#7c3aed',
              secondary: '#ffffff',
            },
          },
          error: {
            style: {
              background: 'rgba(254, 226, 226, 0.9)',
              border: '1px solid rgba(248, 113, 113, 0.2)',
              color: '#dc2626',
            },
            iconTheme: {
              primary: '#dc2626',
              secondary: '#ffffff',
            },
          },
        }}
      />
    </BrowserRouter>
  </React.StrictMode>,
)