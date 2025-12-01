import { Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider, useAuth } from './hooks/useAuth'
import Header from './components/Header'
import Footer from './components/Footer'
import ProtectedRoute from './components/ProtectedRoute'
import ScrollToTop from './components/ScrollToTop'
import GoalieChatWidget from './components/GoalieChatWidget'
import Home from './pages/Home'
import Dashboard from './pages/Dashboard'
import Agents from './pages/Agents'
import Milestones from './pages/Milestones'
import Assistant from './pages/Assistant'
import About from './pages/About'
import Features from './pages/Features'
import Blog from './pages/Blog'
import Support from './pages/Support'
import Contact from './pages/Contact'
import Register from './pages/Register'
import Profile from './pages/Profile'
import PrivacyPolicy from './pages/PrivacyPolicy'
import Terms from './pages/Terms'
import HelpCenter from './pages/HelpCenter'
import ParallelAgentsForm from './components/ParallelAgentsForm'

// Home route - always show home page
const HomeRoute = () => {
  return <Home />
}

// Layout Component with modern theme
const Layout = ({ children }) => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-pink-50 to-indigo-50 flex flex-col">
      <Header />
      <main className="pt-16 flex-1">
        {children}
      </main>
      <Footer />
    </div>
  )
}



// App Routes
const AppRoutes = () => {
  return (
    <Routes>
      <Route path="/" element={<HomeRoute />} />
      <Route path="/register" element={<Register />} />
      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <Layout>
              <Dashboard />
            </Layout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/agents"
        element={
          <ProtectedRoute>
            <Layout>
              <Agents />
            </Layout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/assistant"
        element={
          <Layout>
            <Assistant />
          </Layout>
        }
      />
      <Route
        path="/about"
        element={
          <Layout>
            <About />
          </Layout>
        }
      />
      <Route
        path="/features"
        element={
          <Layout>
            <Features />
          </Layout>
        }
      />
      <Route
        path="/blog"
        element={
          <Layout>
            <Blog />
          </Layout>
        }
      />
      <Route
        path="/support"
        element={
          <Layout>
            <Support />
          </Layout>
        }
      />
      <Route
        path="/contact"
        element={
          <Layout>
            <Contact />
          </Layout>
        }
      />
      <Route
        path="/privacy"
        element={
          <Layout>
            <PrivacyPolicy />
          </Layout>
        }
      />
      <Route
        path="/help"
        element={
          <Layout>
            <HelpCenter />
          </Layout>
        }
      />
      <Route
        path="/terms"
        element={
          <Layout>
            <Terms />
          </Layout>
        }
      />
      <Route
        path="/milestones"
        element={
          <ProtectedRoute>
            <Layout>
              <Milestones />
            </Layout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/parallel-agents"
        element={
          <ProtectedRoute>
            <Layout>
              <div className="px-4 sm:px-6 lg:px-8 py-8">
                <div className="max-w-7xl mx-auto">
                  <ParallelAgentsForm />
                </div>
              </div>
            </Layout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/profile"
        element={
          <ProtectedRoute>
            <Layout>
              <Profile />
            </Layout>
          </ProtectedRoute>
        }
      />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}

// Main App Component
const App = () => {
  return (
    <AuthProvider>
      <ScrollToTop />
      <AppRoutes />
      <GoalieChatWidget />
    </AuthProvider>
  )
}

export default App