import { useState } from 'react'
import { Link } from 'react-router-dom'
import { ScrollReveal } from '../hooks/useScrollReveal'
import {
  MagnifyingGlassIcon,
  QuestionMarkCircleIcon,
  ChevronDownIcon,
  ChevronUpIcon,
  EnvelopeIcon,
  ClockIcon
} from '@heroicons/react/24/outline'

const HelpCenter = () => {
  const [searchQuery, setSearchQuery] = useState('')
  const [openFAQ, setOpenFAQ] = useState(null)

  const allFAQs = [
    {
      question: 'How do I create my first goal?',
      answer: 'Navigate to your Dashboard and click the "Add Goal" button. Choose a category (Career, Finance, Wellness, or Learning) and describe your goal. Our AI agents will help you create a personalized action plan.'
    },
    {
      question: 'What is the Life Goals Dashboard?',
      answer: 'The Dashboard is your central hub for tracking all your goals and progress. It shows your active goals, completed milestones, AI agent recommendations, and overall progress statistics.'
    },
    {
      question: 'How do I sign up or log in?',
      answer: 'Click the "Get Started" button on the homepage to create a new account with your email and password. Existing users can log in using the same credentials from any page.'
    },
    {
      question: 'Can I set multiple goals at once?',
      answer: 'Yes! You can create and track multiple goals across different categories. Our AI agents will help you prioritize and manage them effectively.'
    },
    {
      question: 'How do I track my progress?',
      answer: 'Your Dashboard automatically tracks progress as you complete tasks and milestones. You can also manually update your progress and add notes about your journey.'
    },
    {
      question: 'What can the Career, Finance, Wellness, and Learning agents do?',
      answer: 'Each AI agent specializes in its domain: Career agent helps with job searches and skill development, Finance agent assists with budgeting and investments, Wellness agent focuses on health and fitness goals, and Learning agent supports educational objectives.'
    },
    {
      question: 'How does Parallel AI work?',
      answer: 'Parallel AI allows multiple agents to work together on complex goals that span multiple areas of your life. For example, a career change goal might involve the Career, Finance, and Learning agents working in coordination.'
    },
    {
      question: 'Is my data shared with AI providers?',
      answer: 'We prioritize your privacy. While we use AI services to generate recommendations, we minimize personal identifiers and work only with providers who maintain strict data protection standards. See our Privacy Policy for full details.'
    },
    {
      question: 'Can I customize AI recommendations?',
      answer: 'Yes! You can provide feedback on recommendations, set preferences in your profile, and the AI agents will learn and adapt to your specific needs and goals over time.'
    },
    {
      question: 'How do I update my email or password?',
      answer: 'Go to your Profile page from the user menu. You can update your email, change your password, and modify other account settings from there.'
    },
    {
      question: 'How do I delete my account and data?',
      answer: 'You can delete your account from the Profile page under Security settings. This will permanently remove all your data. You can also contact our support team for assistance.'
    },
    {
      question: 'Is Goalstone free to use?',
      answer: 'Goalstone offers a free tier with core features. Premium features and advanced AI capabilities may require a subscription. Check our pricing page for current plans and features.'
    },
    {
      question: 'How do I export my data?',
      answer: 'You can export your goals, progress data, and AI recommendations from your Profile page. We support multiple formats including PDF and CSV for your convenience.'
    }
  ]

  const filteredFAQs = allFAQs.filter(faq => 
    faq.question.toLowerCase().includes(searchQuery.toLowerCase()) ||
    faq.answer.toLowerCase().includes(searchQuery.toLowerCase())
  )

  const toggleFAQ = (index) => {
    setOpenFAQ(openFAQ === index ? null : index)
  }

  const hasResults = filteredFAQs.length > 0

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-pink-50 py-16">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Hero Section */}
        <ScrollReveal>
          <div className="text-center mb-16">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-purple-600 to-pink-600 rounded-2xl mb-6">
              <QuestionMarkCircleIcon className="h-8 w-8 text-white" />
            </div>
            <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
              Help Center
            </h1>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto mb-8">
              Find quick answers, guides, and ways to contact the Goalstone team.
            </p>
            
            {/* Search Bar */}
            <div className="backdrop-blur-sm bg-white/70 rounded-3xl p-6 shadow-xl border border-white/20 max-w-2xl mx-auto">
              <div className="relative">
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Search help topics (e.g. goals, agents, billing)..."
                  className="w-full px-6 py-4 bg-white/50 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-purple-500 pr-12"
                />
                <button className="absolute right-3 top-1/2 transform -translate-y-1/2 p-2 text-purple-600 hover:text-purple-700">
                  <MagnifyingGlassIcon className="h-5 w-5" />
                </button>
              </div>
            </div>
          </div>
        </ScrollReveal>

        {/* FAQ Section */}
        <ScrollReveal delay={200}>
          <div className="w-full max-w-4xl mx-auto mt-10 mb-16">
            {hasResults ? (
              <div className="bg-white/70 backdrop-blur-sm rounded-3xl shadow-xl border border-white/20 p-8 hover:shadow-2xl transition-all duration-300">
                <h2 className="text-3xl font-bold text-gray-900 mb-8 text-center">Frequently Asked Questions</h2>
                <div className="space-y-3">
                  {filteredFAQs.map((faq, index) => {
                    const isOpen = openFAQ === index
                    return (
                      <div key={index} className="border border-gray-200 rounded-xl overflow-hidden hover:border-purple-300 transition-colors">
                        <button
                          onClick={() => toggleFAQ(index)}
                          className="w-full px-6 py-4 text-left bg-white/50 hover:bg-white/70 transition-colors flex items-center justify-between group"
                        >
                          <span className="font-medium text-gray-900 group-hover:text-purple-700 transition-colors">{faq.question}</span>
                          {isOpen ? (
                            <ChevronUpIcon className="h-5 w-5 text-purple-600 transform transition-transform" />
                          ) : (
                            <ChevronDownIcon className="h-5 w-5 text-purple-600 transform transition-transform" />
                          )}
                        </button>
                        {isOpen && (
                          <div className="px-6 py-4 bg-gradient-to-r from-purple-50/50 to-pink-50/50 border-t border-gray-200">
                            <p className="text-gray-700 leading-relaxed">{faq.answer}</p>
                          </div>
                        )}
                      </div>
                    )
                  })}
                </div>
              </div>
            ) : searchQuery ? (
              <div className="text-center py-16">
                <div className="bg-white/70 backdrop-blur-sm rounded-3xl shadow-xl border border-white/20 p-12 max-w-2xl mx-auto">
                  <QuestionMarkCircleIcon className="h-16 w-16 text-gray-400 mx-auto mb-4" />
                  <h3 className="text-xl font-semibold text-gray-900 mb-2">No results found</h3>
                  <p className="text-gray-600 mb-6">
                    We couldn't find any help topics matching "{searchQuery}". Try different keywords or browse our FAQ below.
                  </p>
                  <button
                    onClick={() => setSearchQuery('')}
                    className="px-6 py-3 bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-xl hover:from-purple-700 hover:to-pink-700 transition-all duration-200 transform hover:scale-105"
                  >
                    Clear Search
                  </button>
                </div>
              </div>
            ) : null}
          </div>
        </ScrollReveal>

        {/* Contact & Support Grid */}
        <ScrollReveal delay={400}>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 w-full max-w-4xl mx-auto">
            {/* Contact & Support */}
            <div className="h-full flex flex-col bg-white/70 backdrop-blur-sm rounded-3xl shadow-xl border border-white/20 p-8 hover:shadow-2xl transition-all duration-300">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Contact & Support</h2>
              <div className="space-y-6 flex-1">
                <div className="flex items-start space-x-4">
                  <div className="p-3 bg-purple-100 rounded-xl">
                    <EnvelopeIcon className="h-6 w-6 text-purple-600" />
                  </div>
                  <div>
                    <p className="font-semibold text-gray-900">Email Support</p>
                    <a href="mailto:support@goalstone.in" className="text-purple-600 hover:text-purple-700 transition-colors">
                      support@goalstone.in
                    </a>
                    <p className="text-sm text-gray-500 mt-1">We typically respond within 24 hours</p>
                  </div>
                </div>
                <div className="flex items-start space-x-4">
                  <div className="p-3 bg-purple-100 rounded-xl">
                    <ClockIcon className="h-6 w-6 text-purple-600" />
                  </div>
                  <div>
                    <p className="font-semibold text-gray-900">Support Hours</p>
                    <p className="text-gray-600">10:00–18:00 IST</p>
                    <p className="text-sm text-gray-500">Monday to Saturday</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Still Need Help */}
            <div className="h-full flex flex-col bg-white/70 backdrop-blur-sm rounded-3xl shadow-xl border border-white/20 p-8 hover:shadow-2xl transition-all duration-300">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">Still Need Help?</h2>
              <div className="flex-1 flex flex-col justify-between">
                <div>
                  <p className="text-gray-600 mb-4">
                    Can't find what you're looking for? Our support team is here to help you succeed with your goals.
                  </p>
                  <div className="bg-gradient-to-r from-purple-50 to-pink-50 p-4 rounded-xl mb-6">
                    <p className="text-sm text-purple-700 font-medium">
                      💡 Pro tip: Include your goal details when contacting support for faster assistance!
                    </p>
                  </div>
                </div>
                <Link
                  to="/contact"
                  className="inline-flex items-center justify-center px-6 py-3 bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-xl hover:from-purple-700 hover:to-pink-700 transition-all duration-200 transform hover:scale-105 shadow-lg"
                >
                  Contact Support
                </Link>
              </div>
            </div>
          </div>
        </ScrollReveal>
      </div>
    </div>
  )
}

export default HelpCenter