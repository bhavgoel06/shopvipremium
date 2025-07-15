import React from 'react';
import { Link } from 'react-router-dom';

const TermsPage = () => {
  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="container mx-auto px-4">
        <div className="max-w-4xl mx-auto bg-white rounded-lg shadow-lg p-8">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-gray-800 mb-4">Terms & Conditions</h1>
            <p className="text-gray-600">Last updated: December 2024</p>
          </div>

          <div className="space-y-8">
            <section>
              <h2 className="text-2xl font-semibold text-gray-800 mb-4">1. Acceptance of Terms</h2>
              <p className="text-gray-600 leading-relaxed">
                By accessing and using Shop For Premium ("we," "us," or "our"), you accept and agree to be bound by the terms and provision of this agreement.
              </p>
            </section>

            <section>
              <h2 className="text-2xl font-semibold text-gray-800 mb-4">2. Use License</h2>
              <div className="text-gray-600 leading-relaxed space-y-3">
                <p>Permission is granted to temporarily download one copy of the materials on Shop For Premium for personal, non-commercial transitory viewing only. This is the grant of a license, not a transfer of title, and under this license you may not:</p>
                <ul className="list-disc list-inside ml-4 space-y-1">
                  <li>modify or copy the materials</li>
                  <li>use the materials for any commercial purpose or for any public display</li>
                  <li>attempt to reverse engineer any software contained on the website</li>
                  <li>remove any copyright or other proprietary notations from the materials</li>
                </ul>
              </div>
            </section>

            <section>
              <h2 className="text-2xl font-semibold text-gray-800 mb-4">3. Product Information</h2>
              <div className="text-gray-600 leading-relaxed space-y-3">
                <p>All products sold on Shop For Premium are:</p>
                <ul className="list-disc list-inside ml-4 space-y-1">
                  <li>100% genuine and legally obtained subscriptions</li>
                  <li>Delivered instantly via WhatsApp or email</li>
                  <li>Non-refundable once delivered unless the product is defective</li>
                  <li>Subject to the terms of service of the original service provider</li>
                </ul>
              </div>
            </section>

            <section>
              <h2 className="text-2xl font-semibold text-gray-800 mb-4">4. Payment Terms</h2>
              <div className="text-gray-600 leading-relaxed space-y-3">
                <p>Payment terms include:</p>
                <ul className="list-disc list-inside ml-4 space-y-1">
                  <li>All payments must be made in full before product delivery</li>
                  <li>We accept major credit cards, debit cards, and digital wallets</li>
                  <li>Prices are listed in USD and INR and may change without notice</li>
                  <li>Failed payments may result in order cancellation</li>
                </ul>
              </div>
            </section>

            <section>
              <h2 className="text-2xl font-semibold text-gray-800 mb-4">5. Refund Policy</h2>
              <div className="text-gray-600 leading-relaxed space-y-3">
                <p>Our refund policy states:</p>
                <ul className="list-disc list-inside ml-4 space-y-1">
                  <li>Refunds are available within 24 hours of purchase if the product is defective</li>
                  <li>No refunds for change of mind or compatibility issues</li>
                  <li>Refunds will be processed within 5-7 business days</li>
                  <li>Refunds will be issued to the original payment method</li>
                </ul>
              </div>
            </section>

            <section>
              <h2 className="text-2xl font-semibold text-gray-800 mb-4">6. Privacy Policy</h2>
              <p className="text-gray-600 leading-relaxed">
                Your privacy is important to us. We collect only necessary information to process your orders and provide customer support. We do not share your personal information with third parties except as required to complete your purchase.
              </p>
            </section>

            <section>
              <h2 className="text-2xl font-semibold text-gray-800 mb-4">7. Prohibited Uses</h2>
              <div className="text-gray-600 leading-relaxed space-y-3">
                <p>You may not use our service:</p>
                <ul className="list-disc list-inside ml-4 space-y-1">
                  <li>For any unlawful purpose or to solicit others to perform unlawful acts</li>
                  <li>To violate any international, federal, provincial, or state regulations, rules, laws, or local ordinances</li>
                  <li>To infringe upon or violate our intellectual property rights or the intellectual property rights of others</li>
                  <li>To harass, abuse, insult, harm, defame, slander, disparage, intimidate, or discriminate</li>
                </ul>
              </div>
            </section>

            <section>
              <h2 className="text-2xl font-semibold text-gray-800 mb-4">8. Disclaimer</h2>
              <p className="text-gray-600 leading-relaxed">
                The materials on Shop For Premium are provided on an 'as is' basis. Shop For Premium makes no warranties, expressed or implied, and hereby disclaim and negate all other warranties including without limitation, implied warranties or conditions of merchantability, fitness for a particular purpose, or non-infringement of intellectual property or other violation of rights.
              </p>
            </section>

            <section>
              <h2 className="text-2xl font-semibold text-gray-800 mb-4">9. Limitations</h2>
              <p className="text-gray-600 leading-relaxed">
                In no event shall Shop For Premium or its suppliers be liable for any damages (including, without limitation, damages for loss of data or profit, or due to business interruption) arising out of the use or inability to use the materials on Shop For Premium, even if Shop For Premium or a Shop For Premium authorized representative has been notified orally or in writing of the possibility of such damage. Because some jurisdictions do not allow limitations on implied warranties, or limitations of liability for consequential or incidental damages, these limitations may not apply to you.
              </p>
            </section>

            <section>
              <h2 className="text-2xl font-semibold text-gray-800 mb-4">10. Contact Information</h2>
              <div className="text-gray-600 leading-relaxed space-y-2">
                <p>If you have any questions about these Terms & Conditions, please contact us:</p>
                <div className="bg-gray-50 p-4 rounded-lg">
                  <p><strong>Email:</strong> support@shopforpremium.com</p>
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

export default TermsPage;