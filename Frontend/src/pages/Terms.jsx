import { ScrollReveal } from '../hooks/useScrollReveal'
import { DocumentTextIcon } from '@heroicons/react/24/outline'

const Terms = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-pink-50 py-16">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Hero Section */}
        <ScrollReveal>
          <div className="text-center mb-16">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-purple-600 to-pink-600 rounded-2xl mb-6">
              <DocumentTextIcon className="h-8 w-8 text-white" />
            </div>
            <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
              Terms & Conditions
            </h1>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              The rules for using Goalstone's AI-powered life goals dashboard.
            </p>
          </div>
        </ScrollReveal>

        {/* Terms Content */}
        <ScrollReveal delay={200}>
          <div className="bg-white/70 backdrop-blur-sm rounded-3xl p-8 shadow-xl border border-white/20 space-y-8">
            
            <div className="text-sm text-gray-500 mb-8">
              Last updated: January 15, 2024
            </div>

            <section className="space-y-4">
              <h2 className="text-2xl font-bold text-gray-900">1. Acceptance of Terms</h2>
              <p className="text-gray-700 leading-relaxed">
                By creating an account or using Goalstone, you agree to these Terms and Conditions 
                and our Privacy Policy. If you do not agree with these terms, please do not use our service.
              </p>
            </section>

            <section className="space-y-4">
              <h2 className="text-2xl font-bold text-gray-900">2. Service Description</h2>
              <p className="text-gray-700 leading-relaxed">
                Goalstone is an AI-assisted life goals dashboard for planning, tracking, and achieving 
                your personal and professional goals. Our service availability and features may change 
                over time as we continue to improve and expand our platform.
              </p>
            </section>

            <section className="space-y-4">
              <h2 className="text-2xl font-bold text-gray-900">3. Eligibility & Accounts</h2>
              <p className="text-gray-700 leading-relaxed">
                Users must be at least 13 years old to use Goalstone. You are responsible for keeping 
                your account credentials secure and providing accurate account information. You may not 
                share your account with others or create multiple accounts.
              </p>
            </section>

            <section className="space-y-4">
              <h2 className="text-2xl font-bold text-gray-900">4. Acceptable Use</h2>
              <p className="text-gray-700 leading-relaxed">
                You may not use Goalstone for illegal activities, abuse, spam, scraping, or attempts 
                to attack the service or other users. You must respect other users and use the platform 
                in good faith for its intended purpose of goal management and personal development.
              </p>
            </section>

            <section className="space-y-4">
              <h2 className="text-2xl font-bold text-gray-900">5. Subscriptions & Payments</h2>
              <p className="text-gray-700 leading-relaxed">
                While Goalstone currently offers free access to core features, some advanced features 
                may require a paid subscription in the future. Any billing will be clearly communicated, 
                and you can cancel subscriptions at any time. Refunds will be handled according to our 
                refund policy at the time of purchase.
              </p>
            </section>

            <section className="space-y-4">
              <h2 className="text-2xl font-bold text-gray-900">6. User Content & Data</h2>
              <p className="text-gray-700 leading-relaxed">
                You own your goals, inputs, and personal data. By using Goalstone, you grant us a 
                limited license to process and analyze your data to provide our AI-powered recommendations 
                and services. We will handle your data according to our Privacy Policy.
              </p>
            </section>

            <section className="space-y-4">
              <h2 className="text-2xl font-bold text-gray-900">7. Intellectual Property</h2>
              <p className="text-gray-700 leading-relaxed">
                The Goalstone name, branding, application code, and proprietary algorithms remain our 
                intellectual property. Users receive a limited, personal, non-transferable license to 
                use the service for its intended purpose.
              </p>
            </section>

            <section className="space-y-4">
              <h2 className="text-2xl font-bold text-gray-900">8. Third-Party Services & AI Models</h2>
              <p className="text-gray-700 leading-relaxed">
                Some features rely on external APIs and AI models from third-party providers. We are 
                not responsible for outages, changes, or issues with these external services, though 
                we strive to minimize any impact on your experience.
              </p>
            </section>

            <section className="space-y-4">
              <h2 className="text-2xl font-bold text-gray-900">9. Termination</h2>
              <p className="text-gray-700 leading-relaxed">
                We may suspend or terminate accounts for violations of these terms. Users can stop 
                using the service at any time and may request data deletion by contacting our support 
                team. Account termination does not relieve you of any outstanding payment obligations.
              </p>
            </section>

            <section className="space-y-4">
              <h2 className="text-2xl font-bold text-gray-900">10. Disclaimers & Limitation of Liability</h2>
              <p className="text-gray-700 leading-relaxed">
                Goalstone is provided "as is" without warranties of any kind. We do not guarantee 
                uninterrupted availability or error-free operation. Our liability is limited to the 
                maximum extent allowed by applicable law, and we are not liable for indirect or 
                consequential damages.
              </p>
            </section>

            <section className="space-y-4">
              <h2 className="text-2xl font-bold text-gray-900">11. Changes to Service or Terms</h2>
              <p className="text-gray-700 leading-relaxed">
                We may update our features, service, or these Terms at any time. Material changes 
                will be communicated through our platform or email, and the "Last updated" date 
                will be revised. Continued use after changes constitutes acceptance of the updated terms.
              </p>
            </section>

            <section className="space-y-4">
              <h2 className="text-2xl font-bold text-gray-900">12. Governing Law</h2>
              <p className="text-gray-700 leading-relaxed">
                These Terms are governed by the laws of India, without regard to conflict of law 
                principles. Any disputes will be resolved in the courts of Coimbatore, Tamil Nadu, India.
              </p>
            </section>

            <section className="space-y-4">
              <h2 className="text-2xl font-bold text-gray-900">13. Contact Information</h2>
              <p className="text-gray-700 leading-relaxed">
                If you have questions about these Terms & Conditions, please contact us:
              </p>
              <div className="bg-purple-50 p-4 rounded-xl">
                <p className="text-gray-700">
                  <strong>Email:</strong> <a href="mailto:support@goalstone.in" className="text-purple-600 hover:text-purple-700">support@goalstone.in</a><br />
                  <strong>Address:</strong> Goalstone Technologies, Coimbatore, Tamil Nadu, India<br />
                  <strong>Phone:</strong> <a href="tel:+918754365691" className="text-purple-600 hover:text-purple-700">+91 87543 65691</a>
                </p>
              </div>
            </section>

          </div>
        </ScrollReveal>
      </div>
    </div>
  )
}

export default Terms