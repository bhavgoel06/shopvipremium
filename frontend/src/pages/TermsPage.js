import React from 'react';

const TermsPage = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white py-16">
        <div className="container mx-auto px-4">
          <div className="text-center">
            <h1 className="text-4xl font-bold mb-4">Terms and Conditions</h1>
            <p className="text-xl opacity-90">
              Please read these terms carefully before using our services
            </p>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="container mx-auto px-4 py-12">
        <div className="max-w-4xl mx-auto bg-white rounded-lg shadow-md p-8">
          <div className="space-y-8">
            <div>
              <h2 className="text-2xl font-bold text-gray-800 mb-4">1. Agreement to Terms</h2>
              <p className="text-gray-600 mb-4">
                By accessing and using Shop For Premium ("we," "us," or "our"), you accept and agree to be bound by the terms and provision of this agreement.
              </p>
              <p className="text-gray-600">
                These Terms of Service govern your use of the Shop For Premium website and services, including the purchase of premium subscription accounts.
              </p>
            </div>

            <div>
              <h2 className="text-2xl font-bold text-gray-800 mb-4">2. Products and Services</h2>
              <p className="text-gray-600 mb-4">
                Shop For Premium provides legitimate premium subscription accounts for various digital services including streaming platforms, software tools, VPN services, and other digital products.
              </p>
              <ul className="list-disc list-inside text-gray-600 space-y-2 mb-4">
                <li>All accounts are genuine and legally obtained</li>
                <li>Instant delivery via WhatsApp or email</li>
                <li>30-day warranty on all subscriptions</li>
                <li>24/7 customer support</li>
              </ul>
            </div>

            <div>
              <h2 className="text-2xl font-bold text-gray-800 mb-4">3. User Responsibilities</h2>
              <p className="text-gray-600 mb-4">By using our services, you agree to:</p>
              <ul className="list-disc list-inside text-gray-600 space-y-2 mb-4">
                <li>Provide accurate and complete information during registration</li>
                <li>Use purchased accounts only for personal use</li>
                <li>Not share or resell purchased accounts</li>
                <li>Comply with the terms of service of the respective platforms</li>
                <li>Not use our services for illegal activities</li>
              </ul>
            </div>

            <div>
              <h2 className="text-2xl font-bold text-gray-800 mb-4">4. Payment and Refunds</h2>
              <p className="text-gray-600 mb-4">
                All payments are processed through secure payment gateways. We accept various payment methods including credit cards, debit cards, and digital wallets.
              </p>
              <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-4">
                <h3 className="font-semibold text-yellow-800 mb-2">Refund Policy:</h3>
                <ul className="list-disc list-inside text-yellow-700 space-y-1">
                  <li>30-day warranty on all subscriptions</li>
                  <li>Refunds available for non-working accounts</li>
                  <li>Replacement or refund at customer's choice</li>
                  <li>Refunds processed within 5-7 business days</li>
                </ul>
              </div>
            </div>

            <div>
              <h2 className="text-2xl font-bold text-gray-800 mb-4">5. Age Restrictions</h2>
              <p className="text-gray-600 mb-4">
                You must be at least 18 years old to use our services. Some products may contain adult content and are restricted to users 18 years and older.
              </p>
              <p className="text-gray-600">
                By using our services, you confirm that you are of legal age in your jurisdiction.
              </p>
            </div>

            <div>
              <h2 className="text-2xl font-bold text-gray-800 mb-4">6. Disclaimer of Warranties</h2>
              <p className="text-gray-600 mb-4">
                While we strive to provide the best service, we provide our services "as is" without any warranties. We do not guarantee uninterrupted service or that our services will meet your specific requirements.
              </p>
            </div>

            <div>
              <h2 className="text-2xl font-bold text-gray-800 mb-4">7. Limitation of Liability</h2>
              <p className="text-gray-600 mb-4">
                In no event shall Shop For Premium be liable for any indirect, incidental, special, consequential, or punitive damages arising out of your use of our services.
              </p>
            </div>

            <div>
              <h2 className="text-2xl font-bold text-gray-800 mb-4">8. Privacy Policy</h2>
              <p className="text-gray-600 mb-4">
                Your privacy is important to us. Please review our Privacy Policy, which also governs your use of our services.
              </p>
            </div>

            <div>
              <h2 className="text-2xl font-bold text-gray-800 mb-4">9. Changes to Terms</h2>
              <p className="text-gray-600 mb-4">
                We reserve the right to modify these terms at any time. Changes will be effective immediately upon posting on our website.
              </p>
            </div>

            <div>
              <h2 className="text-2xl font-bold text-gray-800 mb-4">10. Contact Information</h2>
              <p className="text-gray-600 mb-4">
                If you have any questions about these Terms and Conditions, please contact us:
              </p>
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                <p className="text-blue-800 mb-2"><strong>Email:</strong> support@shopforpremium.com</p>
                <p className="text-blue-800 mb-2"><strong>WhatsApp:</strong> +91 9876543210</p>
                <p className="text-blue-800"><strong>Telegram:</strong> @shopforpremium</p>
              </div>
            </div>

            <div className="border-t pt-8">
              <p className="text-gray-500 text-sm">
                Last updated: {new Date().toLocaleDateString('en-US', { 
                  year: 'numeric', 
                  month: 'long', 
                  day: 'numeric' 
                })}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TermsPage;