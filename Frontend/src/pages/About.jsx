import { Link } from 'react-router-dom'
import { ScrollReveal, StaggeredReveal } from '../hooks/useScrollReveal'
import CountUpNumber from '../components/CountUpNumber'
import { 
  SparklesIcon, 
  RocketLaunchIcon, 
  ChartBarIcon,
  UserGroupIcon,
  BellIcon,
  CpuChipIcon,
  ArrowRightIcon
} from '@heroicons/react/24/outline'

const About = () => {
  const features = [
    {
      icon: SparklesIcon,
      title: 'AI Goal Generator',
      description: 'Create personalized goals with advanced AI assistance'
    },
    {
      icon: UserGroupIcon,
      title: 'Multi-Agent Planners',
      description: 'Career, Finance, Wellness & Learning agents working for you'
    },
    {
      icon: RocketLaunchIcon,
      title: '30/60/90 Career Roadmaps',
      description: 'Structured career progression with actionable milestones'
    },
    {
      icon: ChartBarIcon,
      title: 'Personal Dashboards',
      description: 'Track progress with beautiful analytics and insights'
    },
    {
      icon: BellIcon,
      title: 'Smart Reminders',
      description: 'Never miss important milestones with intelligent notifications'
    },
    {
      icon: CpuChipIcon,
      title: 'Kaggle-ready Analytics',
      description: 'Export data for advanced analysis and machine learning'
    }
  ]

  const steps = [
    { number: '01', title: 'Create Profile', description: 'Set up your personal profile with goals and preferences' },
    { number: '02', title: 'Generate Goals with AI', description: 'Let our AI agents create personalized roadmaps for you' },
    { number: '03', title: 'Track Milestones', description: 'Monitor progress with dashboards and celebrate achievements' }
  ]

  const stats = [
    { label: 'Goals Created', value: 10000, suffix: '+', icon: SparklesIcon },
    { label: 'Categories Supported', value: 4, suffix: '', icon: ChartBarIcon },
    { label: 'Years Experience', value: 5, suffix: '+', icon: CpuChipIcon }
  ]

  const founder = {
    name: 'Bharath',
    role: 'Founder & AI Developer',
    avatar: '/mypic.jpeg',
    description: 'Passionate about AI and helping people achieve their goals through technology'
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-pink-50">
      {/* Hero Section */}
      <section className="pt-32 pb-20">
        <div className="max-w-6xl mx-auto px-6 sm:px-8 lg:px-12 text-center">
          <ScrollReveal>
            <h1 className="text-5xl lg:text-6xl font-bold text-gray-900 mb-6">
              About <span className="bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent">Goalstone</span>
            </h1>
          </ScrollReveal>
          <ScrollReveal delay={200}>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto mb-8 leading-relaxed">
              An AI-powered life goals and milestones planner that helps you transform dreams into achievable roadmaps with personalized guidance across career, finance, wellness, and learning.
            </p>
          </ScrollReveal>
          <ScrollReveal delay={400}>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                to="/agents"
                className="inline-flex items-center px-6 py-3 bg-gradient-to-r from-purple-600 to-pink-600 text-white font-semibold rounded-xl hover:from-purple-700 hover:to-pink-700 transition-all duration-200"
              >
                Try Goal Generator
                <ArrowRightIcon className="ml-2 w-4 h-4" />
              </Link>
              <Link
                to="/dashboard"
                className="inline-flex items-center px-6 py-3 bg-white text-gray-700 font-semibold rounded-xl border border-gray-200 hover:border-purple-300 hover:text-purple-600 transition-all duration-200"
              >
                View Dashboard
              </Link>
            </div>
          </ScrollReveal>
        </div>
      </section>

      {/* Our Mission */}
      <section className="py-20 bg-white/50">
        <div className="max-w-6xl mx-auto px-6 sm:px-8 lg:px-12">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            <ScrollReveal>
              <div>
                <h2 className="text-4xl font-bold text-gray-900 mb-6">Our Mission</h2>
                <p className="text-lg text-gray-600 mb-6 leading-relaxed">
                  We believe everyone deserves a clear path to their dreams. Goalstone empowers individuals to set, track, and achieve meaningful life goals through the power of artificial intelligence.
                </p>
                <p className="text-lg text-gray-600 leading-relaxed">
                  Built for <span className="font-semibold text-purple-600">students</span> planning their careers, <span className="font-semibold text-purple-600">professionals</span> seeking growth, and <span className="font-semibold text-purple-600">creators</span> pursuing their passions.
                </p>
              </div>
            </ScrollReveal>
            <ScrollReveal delay={200}>
              <img 
                src="/our-mission-gif.gif" 
                alt="Our Mission" 
                className="w-full h-auto rounded-xl shadow-lg"
              />
            </ScrollReveal>
          </div>
        </div>
      </section>

      {/* What Goalstone Does */}
      <section className="py-20">
        <div className="max-w-6xl mx-auto px-6 sm:px-8 lg:px-12">
          <ScrollReveal>
            <div className="text-center mb-16">
              <h2 className="text-4xl font-bold text-gray-900 mb-4">What Goalstone Does</h2>
              <p className="text-xl text-gray-600">Comprehensive tools to plan, track, and achieve your life goals</p>
            </div>
          </ScrollReveal>
          <StaggeredReveal staggerDelay={80} className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => {
              const directions = ['left', 'up', 'right', 'left', 'up', 'right'];
              return (
                <div key={index} className="bg-white/70 backdrop-blur-sm rounded-2xl p-6 shadow-lg border border-white/20 hover:shadow-xl transition-all duration-300">
                  <ScrollReveal type="scale" delay={index * 50}>
                    <div className="w-12 h-12 bg-gradient-to-r from-purple-100 to-pink-100 rounded-xl flex items-center justify-center mb-4">
                      <feature.icon className="w-6 h-6 text-purple-600" />
                    </div>
                  </ScrollReveal>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">{feature.title}</h3>
                  <p className="text-gray-600 text-sm leading-relaxed">{feature.description}</p>
                </div>
              );
            })}
          </StaggeredReveal>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-20 bg-white/50">
        <div className="max-w-6xl mx-auto px-6 sm:px-8 lg:px-12">
          <ScrollReveal>
            <div className="text-center mb-16">
              <h2 className="text-4xl font-bold text-gray-900 mb-4">How It Works</h2>
              <p className="text-xl text-gray-600">Three simple steps to transform your life</p>
            </div>
          </ScrollReveal>
          <div className="grid md:grid-cols-3 gap-8">
            {steps.map((step, index) => (
              <ScrollReveal key={index} delay={index * 150 + 100}>
                <div className="text-center">
                  <div className="w-16 h-16 bg-gradient-to-r from-purple-600 to-pink-600 rounded-full flex items-center justify-center text-white font-bold text-xl mx-auto mb-6">
                    {step.number}
                  </div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-4">{step.title}</h3>
                  <p className="text-gray-600 leading-relaxed">{step.description}</p>
                </div>
              </ScrollReveal>
            ))}
          </div>
        </div>
      </section>

      {/* Built For You Stats */}
      <section className="py-20">
        <div className="max-w-6xl mx-auto px-6 sm:px-8 lg:px-12">
          <ScrollReveal>
            <div className="text-center mb-12">
              <h2 className="text-4xl font-bold text-gray-900 mb-4">Built For You</h2>
              <p className="text-xl text-gray-600">Trusted by thousands of goal achievers worldwide</p>
            </div>
          </ScrollReveal>
          <div className="grid md:grid-cols-3 gap-6">
            {stats.map((stat, index) => (
              <ScrollReveal key={index} delay={index * 100 + 200}>
                <div className="bg-white/70 backdrop-blur-sm rounded-2xl p-6 shadow-lg border border-white/20 text-center">
                  <div className="w-12 h-12 bg-gradient-to-r from-purple-100 to-pink-100 rounded-xl flex items-center justify-center mx-auto mb-4">
                    <stat.icon className="w-6 h-6 text-purple-600" />
                  </div>
                  <div className="text-3xl font-bold text-gray-900 mb-2">
                    <CountUpNumber endValue={stat.value} suffix={stat.suffix} durationMs={1500} />
                  </div>
                  <div className="text-gray-600 font-medium">{stat.label}</div>
                </div>
              </ScrollReveal>
            ))}
          </div>
        </div>
      </section>

      {/* Behind Goalstone */}
      <section className="py-20 bg-white/50">
        <div className="max-w-6xl mx-auto px-6 sm:px-8 lg:px-12">
          <ScrollReveal>
            <div className="text-center mb-12">
              <h2 className="text-4xl font-bold text-gray-900 mb-4">Behind Goalstone</h2>
              <p className="text-xl text-gray-600">Meet the creator building the future of goal achievement</p>
            </div>
          </ScrollReveal>
          <ScrollReveal delay={200}>
            <div className="flex justify-center">
              <div className="bg-white/70 backdrop-blur-sm rounded-2xl p-8 shadow-lg border border-white/20 text-center max-w-sm">
                <img
                  src={founder.avatar}
                  alt={founder.name}
                  className="w-32 h-32 rounded-full mx-auto mb-6 object-cover border-4 border-gradient-to-r from-purple-200 to-pink-200"
                />
                <h3 className="text-xl font-semibold text-gray-900 mb-2">{founder.name}</h3>
                <p className="text-purple-600 font-medium mb-4">{founder.role}</p>
                <p className="text-gray-600 text-sm leading-relaxed">{founder.description}</p>
              </div>
            </div>
          </ScrollReveal>
        </div>
      </section>
    </div>
  )
}

export default About