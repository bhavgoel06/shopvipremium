import React from 'react';
import { Link } from 'react-router-dom';

const PrivacyPage = () => {
  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="container mx-auto px-4">
        <div className="max-w-4xl mx-auto bg-white rounded-lg shadow-lg p-8">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-gray-800 mb-4">Privacy Policy</h1>
            <p className="text-gray-600">Last updated: December 2024</p>
          </div>

          <div className="space-y-8">
            <section>
              <h2 className="text-2xl font-semibold text-gray-800 mb-4">1. Information We Collect</h2>
              <div className="text-gray-600 leading-relaxed space-y-3">
                <p>We collect information you provide directly to us, such as:</p>
                <ul className="list-disc list-inside ml-4 space-y-1">
                  <li>Name and email address when creating an account</li>
                  <li>Payment information when making a purchase</li>
                  <li>Communication preferences and newsletter subscriptions</li>
                  <li>Customer service inquiries and support requests</li>
                </ul>
              </div>
            </section>

            <section>
              <h2 className="text-2xl font-semibold text-gray-800 mb-4">2. How We Use Your Information</h2>
              <div className="text-gray-600 leading-relaxed space-y-3">
                <p>We use the information we collect to:</p>
                <ul className="list-disc list-inside ml-4 space-y-1">
                  <li>Process your orders and deliver products</li>
                  <li>Provide customer support and respond to inquiries</li>
                  <li>Send you newsletters and promotional materials (with your consent)</li>
                  <li>Improve our website and services</li>
                  <li>Comply with legal obligations</li>
                </ul>
              </div>
            </section>

            <section>
              <h2 className="text-2xl font-semibold text-gray-800 mb-4">3. Information Sharing</h2>
              <div className="text-gray-600 leading-relaxed space-y-3">
                <p>We do not sell, trade, or rent your personal information to third parties. We may share your information only in the following circumstances:</p>
                <ul className="list-disc list-inside ml-4 space-y-1">
                  <li>With payment processors to complete transactions</li>
                  <li>With service providers who assist in our operations</li>
                  <li>When required by law or to protect our rights</li>
                  <li>With your explicit consent</li>
                </ul>
              </div>
            </section>

            <section>
              <h2 className="text-2xl font-semibold text-gray-800 mb-4">4. Data Security</h2>
              <p className="text-gray-600 leading-relaxed">
                We implement appropriate technical and organizational measures to protect your personal information against unauthorized access, alteration, disclosure, or destruction. However, no method of transmission over the internet or electronic storage is 100% secure.
              </p>
            </section>

            <section>
              <h2 className="text-2xl font-semibold text-gray-800 mb-4">5. Cookies and Tracking</h2>
              <div className="text-gray-600 leading-relaxed space-y-3">
                <p>We use cookies and similar tracking technologies to:</p>
                <ul className="list-disc list-inside ml-4 space-y-1">
                  <li>Remember your preferences and settings</li>
                  <li>Analyze website traffic and usage patterns</li>
                  <li>Provide personalized content and recommendations</li>
                  <li>Ensure website security and prevent fraud</li>
                </ul>
              </div>
            </section>

            <section>
              <h2 className="text-2xl font-semibold text-gray-800 mb-4">6. Your Rights</h2>
              <div className="text-gray-600 leading-relaxed space-y-3">
                <p>You have the right to:</p>
                <ul className="list-disc list-inside ml-4 space-y-1">
                  <li>Access your personal information</li>
                  <li>Correct inaccurate or incomplete information</li>
                  <li>Request deletion of your personal information</li>
                  <li>Opt-out of marketing communications</li>
                  <li>Object to the processing of your personal information</li>
                </ul>
              </div>
            </section>

            <section>
              <h2 className="text-2xl font-semibold text-gray-800 mb-4">7. Third-Party Services</h2>
              <p className="text-gray-600 leading-relaxed">
                Our website may contain links to third-party services. We are not responsible for the privacy practices of these external sites. We encourage you to review their privacy policies before providing any personal information.
              </p>
            </section>

            <section>
              <h2 className="text-2xl font-semibold text-gray-800 mb-4">8. Children's Privacy</h2>
              <p className="text-gray-600 leading-relaxed">
                Our services are not intended for children under 13 years of age. We do not knowingly collect personal information from children under 13. If you become aware that a child has provided us with personal information, please contact us.
              </p>
            </section>

            <section>
              <h2 className="text-2xl font-semibold text-gray-800 mb-4">9. Changes to This Policy</h2>
              <p className="text-gray-600 leading-relaxed">
                We may update this privacy policy from time to time. We will notify you of any changes by posting the new policy on this page and updating the "Last updated" date.
              </p>
            </section>

            <section>
              <h2 className="text-2xl font-semibold text-gray-800 mb-4">10. Contact Us</h2>
              <div className="text-gray-600 leading-relaxed space-y-2">
                <p>If you have any questions about this Privacy Policy, please contact us:</p>
                <div className="bg-gray-50 p-4 rounded-lg">
                  <p><strong>Email:</strong> privacy@shopforpremium.com</p>
                  <p><strong>Phone:</strong> +1-800-PREMIUM</p>
                  <p><strong>Address:</strong> Shop For Premium, Premium Business Center, Digital Commerce District</p>
                </div>
              </div>
            </section>
          </div>

          <div className="mt-12 text-center">
            <Link
              to="/"
              className="bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
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