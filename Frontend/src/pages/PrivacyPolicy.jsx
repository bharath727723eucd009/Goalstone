import { ScrollReveal } from '../hooks/useScrollReveal'
import { ShieldCheckIcon } from '@heroicons/react/24/outline'

const PrivacyPolicy = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-pink-50 py-16">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        
        {/* Hero Section */}
        <ScrollReveal>
          <div className="text-center mb-16">
            <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-r from-purple-600 to-pink-600 rounded-3xl mb-6 shadow-lg">
              <ShieldCheckIcon className="h-10 w-10 text-white" />
            </div>
            <h1 className="text-4xl md:text-6xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent mb-6">
              Privacy Policy
            </h1>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto mb-8">
              How Goalstone handles and protects your personal data with transparency and care.
            </p>
            <div className="flex items-center justify-center space-x-6 text-sm text-gray-500">
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                <span>GDPR Compliant</span>
              </div>
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-blue-500 rounded-full"></div>
                <span>India IT Act 2000</span>
              </div>
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-purple-500 rounded-full"></div>
                <span>ISO 27001 Standards</span>
              </div>
            </div>
          </div>
        </ScrollReveal>

        {/* Privacy Policy Content */}
        <ScrollReveal delay={200}>
          <div className="backdrop-blur-sm bg-white/70 rounded-3xl p-8 shadow-xl border border-white/20 space-y-8">
            
            <div className="flex items-center justify-between mb-8">
              <div className="text-sm text-gray-500">
                Last updated: January 15, 2024
              </div>
              <div className="text-sm text-purple-600 font-medium">
                Effective from: January 1, 2024
              </div>
            </div>

            <section className="space-y-4">
              <h2 className="text-2xl font-bold text-gray-900">1. Information We Collect</h2>
              <p className="text-gray-700 leading-relaxed">
                We collect information you provide when creating an account (name, email, profile details), 
                usage data (how you interact with our AI agents and features), goal and agent interaction data 
                (your inputs, preferences, and generated recommendations), and communications you send to us 
                for support or feedback.
              </p>
            </section>

            <section className="space-y-4">
              <h2 className="text-2xl font-bold text-gray-900">2. How We Use Your Information</h2>
              <p className="text-gray-700 leading-relaxed">
                We use your information to provide and improve our AI-powered goal management service, 
                ensure security and prevent fraud, analyze usage patterns to enhance features, 
                communicate with you about updates and support, and personalize your experience. 
                We do not sell your personal data to third parties.
              </p>
            </section>

            <section className="space-y-4">
              <h2 className="text-2xl font-bold text-gray-900">3. AI and Data Processing</h2>
              <p className="text-gray-700 leading-relaxed">
                Your prompts and context may be sent to AI model providers to generate recommendations 
                and insights. We minimize personal identifiers in these requests and work with providers 
                who maintain appropriate data protection standards. Generated content is processed to 
                provide you with personalized goal guidance.
              </p>
            </section>

            <section className="space-y-4">
              <h2 className="text-2xl font-bold text-gray-900">4. Legal Basis</h2>
              <p className="text-gray-700 leading-relaxed">
                We process your data based on our contract with you to provide services, your consent 
                for specific features, and our legitimate interests in improving and securing our platform. 
                We comply with applicable data protection laws, including those in India where we are based.
              </p>
            </section>

            <section className="space-y-4">
              <h2 className="text-2xl font-bold text-gray-900">5. Data Retention</h2>
              <p className="text-gray-700 leading-relaxed">
                We retain your data while your account is active and for a reasonable period afterward 
                to provide continued service. Some data may be retained in backups and logs for security 
                and operational purposes, but is not actively used after account closure.
              </p>
            </section>

            <section className="space-y-4">
              <h2 className="text-2xl font-bold text-gray-900">6. Sharing Your Information</h2>
              <p className="text-gray-700 leading-relaxed">
                We may share your information with trusted service providers who help us operate our platform, 
                when required by law or to protect safety and security, and in the event of a business 
                merger or acquisition. We require all third parties to maintain appropriate data protection standards.
              </p>
            </section>

            <section className="space-y-4">
              <h2 className="text-2xl font-bold text-gray-900">7. International Transfers</h2>
              <p className="text-gray-700 leading-relaxed">
                Our servers and service providers may be located outside your country. We implement 
                appropriate safeguards to ensure your data receives adequate protection during international 
                transfers, including contractual protections and security measures.
              </p>
            </section>

            <section className="space-y-4">
              <h2 className="text-2xl font-bold text-gray-900">8. Your Rights and Choices</h2>
              <p className="text-gray-700 leading-relaxed">
                You have the right to access, correct, or delete your personal data, request data portability, 
                restrict or object to processing, and withdraw consent where applicable. You can exercise 
                these rights through your account settings or by contacting us directly.
              </p>
            </section>

            <section className="space-y-4">
              <h2 className="text-2xl font-bold text-gray-900">9. Data Security</h2>
              <p className="text-gray-700 leading-relaxed">
                We implement security measures including HTTPS encryption, access controls, and monitoring 
                to protect your data. However, no system is completely secure, and we cannot guarantee 
                absolute protection against all potential threats.
              </p>
            </section>

            <section className="space-y-4">
              <h2 className="text-2xl font-bold text-gray-900">10. Children's Privacy</h2>
              <p className="text-gray-700 leading-relaxed">
                Our service is not intended for children under 13. We do not knowingly collect personal 
                information from children under 13. If we become aware that we have collected such information, 
                we will take steps to remove it promptly.
              </p>
            </section>

            <section className="space-y-4">
              <h2 className="text-2xl font-bold text-gray-900">11. Third-Party Links</h2>
              <p className="text-gray-700 leading-relaxed">
                Our service may contain links to third-party websites or services. This privacy policy 
                does not cover those external sites. We encourage you to review the privacy policies 
                of any third-party services you visit.
              </p>
            </section>

            <section className="space-y-4">
              <h2 className="text-2xl font-bold text-gray-900">12. Changes to This Policy</h2>
              <p className="text-gray-700 leading-relaxed">
                We may update this privacy policy from time to time. When we make changes, we will 
                update the "Last updated" date and provide notice through our service or other appropriate 
                means. Continued use of our service after changes constitutes acceptance of the updated policy.
              </p>
            </section>

            <section className="space-y-4">
              <h2 className="text-2xl font-bold text-gray-900">13. Contact Us</h2>
              <p className="text-gray-700 leading-relaxed">
                If you have questions about this privacy policy or our data practices, please contact us at:
              </p>
              <div className="bg-purple-50 p-4 rounded-xl">
                <p className="text-gray-700">
                  <strong>Email:</strong> <a href="mailto:privacy@goalstone.in" className="text-purple-600 hover:text-purple-700">privacy@goalstone.in</a><br />
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

export default PrivacyPolicy