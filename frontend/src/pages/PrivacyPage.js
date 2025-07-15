import React from 'react';
import { Link } from 'react-router-dom';

const PrivacyPage = () => {
  return (
    <div className="min-h-screen bg-gray-900 text-white py-12">
      <div className="container mx-auto px-4">
        <div className="max-w-4xl mx-auto bg-gray-800 rounded-2xl shadow-2xl p-8">
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent mb-4">
              Privacy Policy
            </h1>
            <p className="text-gray-400">Last updated: December 2024</p>
          </div>

          <div className="space-y-8 text-gray-300">
            <section>
              <h2 className="text-2xl font-semibold text-white mb-4">1. Information We Collect</h2>
              <div className="space-y-3">
                <p>At Shop For Premium, we collect information that you provide directly to us, including:</p>
                <ul className="list-disc list-inside ml-4 space-y-2">
                  <li>Personal information such as your name, email address, and phone number when you create an account</li>
                  <li>Payment information including credit card details, billing address, and transaction history</li>
                  <li>Communication preferences and newsletter subscriptions</li>
                  <li>Customer service inquiries, support requests, and feedback</li>
                  <li>Device information, IP address, and browsing behavior on our website</li>
                </ul>
              </div>
            </section>

            <section>
              <h2 className="text-2xl font-semibold text-white mb-4">2. How We Use Your Information</h2>
              <div className="space-y-3">
                <p>We use the collected information for the following purposes:</p>
                <ul className="list-disc list-inside ml-4 space-y-2">
                  <li>Process your orders and deliver premium subscription services</li>
                  <li>Provide customer support and respond to your inquiries</li>
                  <li>Send transactional emails and order confirmations</li>
                  <li>Improve our website performance and user experience</li>
                  <li>Detect and prevent fraud, abuse, and security threats</li>
                  <li>Comply with legal obligations and regulatory requirements</li>
                  <li>Send promotional communications (with your consent)</li>
                </ul>
              </div>
            </section>

            <section>
              <h2 className="text-2xl font-semibold text-white mb-4">3. Information Sharing and Disclosure</h2>
              <div className="space-y-3">
                <p>We respect your privacy and do not sell or rent your personal information to third parties. We may share your information only in the following circumstances:</p>
                <ul className="list-disc list-inside ml-4 space-y-2">
                  <li>With payment processors and financial institutions to complete transactions</li>
                  <li>With trusted service providers who assist in our business operations</li>
                  <li>With subscription service providers to activate your premium accounts</li>
                  <li>When required by law, legal process, or government authorities</li>
                  <li>To protect our rights, property, and safety, or that of our users</li>
                  <li>In connection with a business transfer or acquisition</li>
                </ul>
              </div>
            </section>

            <section>
              <h2 className="text-2xl font-semibold text-white mb-4">4. Data Security</h2>
              <p>We implement industry-standard security measures to protect your personal information, including:</p>
              <ul className="list-disc list-inside ml-4 space-y-2 mt-3">
                <li>SSL encryption for all data transmissions</li>
                <li>Secure payment processing through trusted payment gateways</li>
                <li>Regular security audits and vulnerability assessments</li>
                <li>Access controls and authentication mechanisms</li>
                <li>Employee training on data protection best practices</li>
              </ul>
            </section>

            <section>
              <h2 className="text-2xl font-semibold text-white mb-4">5. Cookies and Tracking Technologies</h2>
              <div className="space-y-3">
                <p>We use cookies and similar technologies to enhance your browsing experience:</p>
                <ul className="list-disc list-inside ml-4 space-y-2">
                  <li>Essential cookies for website functionality and security</li>
                  <li>Performance cookies to analyze website usage and optimize performance</li>
                  <li>Functional cookies to remember your preferences and settings</li>
                  <li>Marketing cookies to deliver relevant advertisements (with consent)</li>
                </ul>
                <p className="text-sm text-gray-400 mt-3">
                  You can manage cookie preferences through your browser settings.
                </p>
              </div>
            </section>

            <section>
              <h2 className="text-2xl font-semibold text-white mb-4">6. Your Rights and Choices</h2>
              <div className="space-y-3">
                <p>You have the following rights regarding your personal information:</p>
                <ul className="list-disc list-inside ml-4 space-y-2">
                  <li>Access and review your personal information</li>
                  <li>Correct inaccurate or incomplete information</li>
                  <li>Request deletion of your personal information</li>
                  <li>Opt-out of marketing communications</li>
                  <li>Object to certain processing activities</li>
                  <li>Request data portability</li>
                  <li>Withdraw consent for optional data processing</li>
                </ul>
              </div>
            </section>

            <section>
              <h2 className="text-2xl font-semibold text-white mb-4">7. Data Retention</h2>
              <p>We retain your personal information only for as long as necessary to fulfill the purposes outlined in this privacy policy, including:</p>
              <ul className="list-disc list-inside ml-4 space-y-2 mt-3">
                <li>Account information: Until you close your account</li>
                <li>Transaction records: As required by law (typically 7 years)</li>
                <li>Customer support records: 3 years after resolution</li>
                <li>Marketing preferences: Until you unsubscribe</li>
                <li>Website analytics: 2 years from collection</li>
              </ul>
            </section>

            <section>
              <h2 className="text-2xl font-semibold text-white mb-4">8. Third-Party Services</h2>
              <p>Our website may contain links to third-party services and websites. We are not responsible for the privacy practices of these external sites. We encourage you to review their privacy policies before providing any personal information.</p>
            </section>

            <section>
              <h2 className="text-2xl font-semibold text-white mb-4">9. Children's Privacy</h2>
              <p>Our services are not intended for children under 13 years of age. We do not knowingly collect personal information from children under 13. If we become aware that we have collected personal information from a child under 13, we will take steps to delete that information.</p>
            </section>

            <section>
              <h2 className="text-2xl font-semibold text-white mb-4">10. International Data Transfers</h2>
              <p>Your information may be transferred to and processed in countries other than your country of residence. We ensure that such transfers comply with applicable data protection laws and provide appropriate safeguards for your personal information.</p>
            </section>

            <section>
              <h2 className="text-2xl font-semibold text-white mb-4">11. Changes to This Privacy Policy</h2>
              <p>We may update this privacy policy periodically to reflect changes in our practices or applicable laws. We will notify you of any material changes by posting the updated policy on our website and updating the "Last updated" date.</p>
            </section>

            <section>
              <h2 className="text-2xl font-semibold text-white mb-4">12. Contact Information</h2>
              <div className="space-y-3">
                <p>If you have any questions about this privacy policy or our data practices, please contact us:</p>
                <div className="bg-gray-700 p-6 rounded-lg">
                  <p><strong className="text-blue-400">Email:</strong> privacy@shopforpremium.com</p>
                  <p><strong className="text-blue-400">Phone:</strong> +1-800-PREMIUM (773-6486)</p>
                  <p><strong className="text-blue-400">Address:</strong> Shop For Premium, Digital Commerce Center, India</p>
                  <p><strong className="text-blue-400">Response Time:</strong> We respond to all privacy inquiries within 48 hours</p>
                </div>
              </div>
            </section>
          </div>

          <div className="mt-12 text-center">
            <Link
              to="/"
              className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-8 py-3 rounded-lg font-semibold hover:from-blue-700 hover:to-purple-700 transition-all duration-300 transform hover:scale-105"
            >
              Back to Home
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PrivacyPage;