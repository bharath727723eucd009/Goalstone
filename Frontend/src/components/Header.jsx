import { useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth'
import { 
  Bars3Icon, 
  XMarkIcon, 
  BellIcon,
  UserCircleIcon,
  ChevronDownIcon,
  Cog6ToothIcon,
  ArrowRightOnRectangleIcon,
  SparklesIcon,
  CodeBracketIcon
} from '@heroicons/react/24/outline'

const Header = () => {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)
  const [profileMenuOpen, setProfileMenuOpen] = useState(false)
  const [moreMenuOpen, setMoreMenuOpen] = useState(false)
  const { user, logout } = useAuth()
  const location = useLocation()

  const mainNavigation = [
    { name: 'Home', href: '/' },
    { name: 'Dashboard', href: '/dashboard' },
    { name: 'Agents', href: '/agents' },
    { name: 'Parallel AI', href: '/parallel-agents' },
    { name: 'Milestones', href: '/milestones' },
    { name: 'About Us', href: '/about' }
  ]

  const moreNavigation = [
    { name: 'Features', href: '/features' },
    { name: 'Blog', href: '/blog' },
    { name: 'Support', href: '/support' },
    { name: 'GitHub', href: 'https://github.com/yourusername/ai-life-goals', external: true }
  ]

  return (
    <header className="fixed inset-x-0 top-0 z-50 bg-white/80 backdrop-blur-lg border-b border-purple-100/50 shadow-sm">
      <nav className="mx-auto flex max-w-7xl items-center justify-between p-4 lg:px-8" aria-label="Global">
        <div className="flex lg:flex-1">
          <Link to="/" className="-m-1.5 p-1.5 flex items-center space-x-2">
            <img 
              src="/Logo.png" 
              alt="Goalstone Logo" 
              className="h-12 w-12 object-contain"
            />
            <span className="text-xl font-bold text-black ml-3">
              Goalstone
            </span>
          </Link>
        </div>

        <div className="flex lg:hidden">
          <button
            type="button"
            className="-m-2.5 inline-flex items-center justify-center rounded-md p-2.5 text-gray-700 hover:bg-gray-100"
            onClick={() => setMobileMenuOpen(true)}
          >
            <span className="sr-only">Open main menu</span>
            <Bars3Icon className="h-6 w-6" aria-hidden="true" />
          </button>
        </div>

        <div className="hidden lg:flex lg:gap-x-6">
          {mainNavigation.map((item) => {
            const isActive = location.pathname === item.href
            return (
              <Link
                key={item.name}
                to={item.href}
                className={`text-sm font-medium transition-all duration-200 ${
                  isActive
                    ? 'text-purple-600 border-b-2 border-purple-600 pb-1'
                    : 'text-gray-700 hover:text-purple-600 hover:border-b-2 hover:border-purple-300 pb-1'
                }`}
              >
                {item.name}
              </Link>
            )
          })}
          
          {/* More Dropdown */}
          <div className="relative">
            <button
              onClick={() => setMoreMenuOpen(!moreMenuOpen)}
              className="text-sm font-medium text-gray-700 hover:text-purple-600 transition-colors duration-200 flex items-center pb-1"
            >
              More
              <ChevronDownIcon className="w-4 h-4 ml-1" />
            </button>
            
            {moreMenuOpen && (
              <div className="absolute right-0 z-10 mt-2 w-48 origin-top-right rounded-xl bg-white py-2 shadow-lg ring-1 ring-gray-900/5">
                {moreNavigation.map((item) => {
                  if (item.external) {
                    return (
                      <a
                        key={item.name}
                        href={item.href}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-50"
                        onClick={() => setMoreMenuOpen(false)}
                      >
                        <CodeBracketIcon className="w-4 h-4 mr-2" />
                        {item.name}
                      </a>
                    )
                  }
                  return (
                    <Link
                      key={item.name}
                      to={item.href}
                      className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50"
                      onClick={() => setMoreMenuOpen(false)}
                    >
                      {item.name}
                    </Link>
                  )
                })}
              </div>
            )}
          </div>
        </div>

        <div className="hidden lg:flex lg:flex-1 lg:justify-end lg:items-center lg:space-x-4">
          <button
            type="button"
            className="relative rounded-full bg-white p-2 text-gray-400 hover:text-gray-500 hover:bg-gray-50 transition-colors duration-200"
          >
            <span className="sr-only">View notifications</span>
            <BellIcon className="h-6 w-6" aria-hidden="true" />
            <span className="absolute -top-1 -right-1 h-4 w-4 bg-red-500 rounded-full flex items-center justify-center">
              <span className="text-xs font-bold text-white">3</span>
            </span>
          </button>

          <div className="relative">
            <button
              type="button"
              className="flex items-center space-x-3 rounded-full bg-white p-2 text-sm hover:bg-gray-50 transition-colors duration-200"
              onClick={() => setProfileMenuOpen(!profileMenuOpen)}
            >
              <div className="h-8 w-8 rounded-full bg-gradient-to-r from-purple-100 to-pink-100 ring-2 ring-purple-500 flex items-center justify-center">
                <UserCircleIcon className="h-6 w-6 text-purple-400" />
              </div>
              <span className="hidden md:block font-medium text-gray-700">{user?.name || 'Demo User'}</span>
              <ChevronDownIcon className="h-4 w-4 text-gray-400" />
            </button>

            {profileMenuOpen && (
              <div className="absolute right-0 z-10 mt-2 w-56 origin-top-right rounded-xl bg-white py-2 shadow-lg ring-1 ring-gray-900/5 focus:outline-none">
                <div className="px-4 py-3 border-b border-gray-100">
                  <p className="text-sm font-medium text-gray-900">{user?.name || 'Demo User'}</p>
                  <p className="text-sm text-gray-500">{user?.email || 'demo@example.com'}</p>
                </div>
                <Link
                  to="/profile"
                  className="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-50"
                  onClick={() => setProfileMenuOpen(false)}
                >
                  <UserCircleIcon className="mr-3 h-5 w-5 text-gray-400" />
                  Your Profile
                </Link>
                <Link
                  to="/settings"
                  className="flex items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-50"
                  onClick={() => setProfileMenuOpen(false)}
                >
                  <Cog6ToothIcon className="mr-3 h-5 w-5 text-gray-400" />
                  Settings
                </Link>
                <button
                  onClick={() => {
                    logout()
                    setProfileMenuOpen(false)
                  }}
                  className="flex w-full items-center px-4 py-2 text-sm text-gray-700 hover:bg-gray-50"
                >
                  <ArrowRightOnRectangleIcon className="mr-3 h-5 w-5 text-gray-400" />
                  Sign out
                </button>
              </div>
            )}
          </div>
        </div>
      </nav>

      {mobileMenuOpen && (
        <div className="lg:hidden" role="dialog" aria-modal="true">
          <div className="fixed inset-0 z-10 bg-black/30" onClick={() => setMobileMenuOpen(false)}></div>
          <div className="fixed inset-y-0 right-0 z-10 w-full overflow-y-auto bg-white px-6 py-6 sm:max-w-sm sm:ring-1 sm:ring-gray-900/10">
            <div className="flex items-center justify-between">
              <Link to="/" className="-m-1.5 p-1.5 flex items-center space-x-2">
                <img 
                  src="/Logo.png" 
                  alt="Goalstone Logo" 
                  className="h-10 w-10 object-contain"
                />
                <span className="text-lg font-bold text-black">
                  Goalstone
                </span>
              </Link>
              <button
                type="button"
                className="-m-2.5 rounded-md p-2.5 text-gray-700"
                onClick={() => setMobileMenuOpen(false)}
              >
                <span className="sr-only">Close menu</span>
                <XMarkIcon className="h-6 w-6" aria-hidden="true" />
              </button>
            </div>
            <div className="mt-6 flow-root">
              <div className="-my-6 divide-y divide-gray-500/10">
                <div className="space-y-2 py-6">
                  {mainNavigation.map((item) => {
                    const isActive = location.pathname === item.href
                    return (
                      <Link
                        key={item.name}
                        to={item.href}
                        className={`-mx-3 block rounded-lg px-3 py-2 text-base font-semibold leading-7 transition-colors duration-200 ${
                          isActive
                            ? 'bg-purple-50 text-purple-600'
                            : 'text-gray-900 hover:bg-gray-50'
                        }`}
                        onClick={() => setMobileMenuOpen(false)}
                      >
                        {item.name}
                      </Link>
                    )
                  })}
                  
                  <div className="border-t border-gray-200 pt-4 mt-4">
                    <p className="px-3 text-xs font-semibold text-gray-500 uppercase tracking-wide">More</p>
                    {moreNavigation.map((item) => {
                      if (item.external) {
                        return (
                          <a
                            key={item.name}
                            href={item.href}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="-mx-3 flex items-center rounded-lg px-3 py-2 text-base font-semibold leading-7 text-gray-900 hover:bg-gray-50 transition-colors duration-200"
                            onClick={() => setMobileMenuOpen(false)}
                          >
                            <CodeBracketIcon className="w-5 h-5 mr-2" />
                            {item.name}
                          </a>
                        )
                      }
                      return (
                        <Link
                          key={item.name}
                          to={item.href}
                          className="-mx-3 block rounded-lg px-3 py-2 text-base font-semibold leading-7 text-gray-900 hover:bg-gray-50 transition-colors duration-200"
                          onClick={() => setMobileMenuOpen(false)}
                        >
                          {item.name}
                        </Link>
                      )
                    })}
                  </div>
                </div>
                <div className="py-6">
                  <div className="flex items-center space-x-3 px-3 py-2">
                    <div className="h-10 w-10 rounded-full bg-gradient-to-r from-purple-100 to-pink-100 flex items-center justify-center">
                      <UserCircleIcon className="h-8 w-8 text-purple-400" />
                    </div>
                    <div>
                      <p className="text-base font-semibold text-gray-900">{user?.name || 'Demo User'}</p>
                      <p className="text-sm text-gray-500">{user?.email || 'demo@example.com'}</p>
                    </div>
                  </div>
                  <button
                    onClick={() => {
                      logout()
                      setMobileMenuOpen(false)
                    }}
                    className="flex w-full items-center space-x-3 rounded-lg px-3 py-2 text-base font-semibold text-gray-900 hover:bg-gray-50 mt-4"
                  >
                    <ArrowRightOnRectangleIcon className="h-5 w-5 text-gray-400" />
                    <span>Sign out</span>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </header>
  )
}

export default Header