import React from 'react';
import { Helmet } from 'react-helmet';

const TermsPage = () => {
  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <Helmet>
        <title>Terms & Conditions - Shop For Premium</title>
        <meta name="description" content="Terms & Conditions, Terms of service are the legal agreements between Shop For Premium and a person who wants to use that service." />
      </Helmet>
      
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-white rounded-lg shadow-lg p-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-8">Terms & Conditions</h1>
          
          <div className="prose prose-lg max-w-none">
            <div className="mb-8">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Quick Terms</h2>
              <ol className="list-decimal list-inside space-y-2 text-gray-700">
                <li>No Exchanges. We Only Refund If We Aren't Able To Fulfill Service</li>
                <li>Read Product Description Before Buying</li>
                <li>You Are Not Allowed To Change Details Of Given Account. If Did Warranty Will Be Exhausted</li>
                <li>Replacements Will Be Given As Long As You Have Warranty</li>
                <li>Any Chargeback Or Dispute On Payment Will Result In Account And Warranty Termination. Please Contact Us Before Doing So</li>
                <li>We Are Not Responsible For Negative Outcomes After Your Purchase By Buying Any Product On Site. Customer Agree To Follow These Terms</li>
              </ol>
            </div>

            <div className="mb-8">
              <h2 className="text-xl font-semibold text-gray-900 mb-4">Terms of Use</h2>
              <p className="text-gray-700 mb-4">
                Welcome to Shop For Premium, a comprehensive digital membership platform (the "Site") owned, managed and operated by Shop For Premium Team (hereinafter referred to as the "Company", "we" or "our", which expression shall unless the same be repugnant to the context or meaning thereof be deemed to mean and include its affiliates, successors in business and assigns).
              </p>
            </div>

            <div className="mb-8">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">1. Acceptance of Terms of Use</h3>
              <p className="text-gray-700 mb-4">
                Please read the following terms and conditions as these terms of use ("Terms") constitute a legally binding agreement between you and the Company regarding your browsing, access and use of the Site and any functionalities, features, information, contests, services, products offered by the Company including but not limited to the bundled subscriptions via the Site, any mobile or internet connected device or otherwise (the "Service").
              </p>
              <p className="text-gray-700 mb-4">
                "User", "you" or "your": means any person, who is accessing, using the Site, in any manner whatsoever, and is of 18 years of age or older, capable to enter into a legally binding agreement under the laws in India.
              </p>
            </div>

            <div className="mb-8">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">2. Content Ownership and Limited License</h3>
              <p className="text-gray-700 mb-4">
                The Site, Services and the Company Content are protected by copyright, trademark and other applicable laws. Except as expressly provided in these Terms, Company and its licensors exclusively own all right, title and interest in and to the Site, Services, and the Company Content, including all associated intellectual property rights.
              </p>
              <p className="text-gray-700 mb-4">
                Subject to your compliance with the Terms herein, the Company hereby grants you a personal, limited, non-exclusive, non-transferable, freely revocable license to use the Services for the personal and non-commercial use only.
              </p>
            </div>

            <div className="mb-8">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">3. Service Registration/Subscription and Access</h3>
              <p className="text-gray-700 mb-4">
                To register for the Services, you may be required to log in by completing the registration process (i.e. by providing us with current, complete and accurate information as prompted by the applicable registration form).
              </p>
              <p className="text-gray-700 mb-4">
                The subscription prices shall be determined by the Company, in its sole discretion. When you purchase a subscription, you must provide us with complete and accurate payment and other information required by the Company.
              </p>
            </div>

            <div className="mb-8">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">4. Prohibited Activities</h3>
              <p className="text-gray-700 mb-4">You hereby agree not to upload, post, modify, publish, update, share or otherwise transmit any matter or views on the Site, which:</p>
              <ul className="list-disc list-inside space-y-2 text-gray-700 ml-4">
                <li>Are grossly harmful, harassing, blasphemous, defamatory, abusive, pervasive, obscene, pornographic, libellous, invasive of another's privacy</li>
                <li>Harm children in any way</li>
                <li>Infringe any patent, trademark, copyright or other proprietary rights</li>
                <li>Violate any Law for the time being in force</li>
                <li>Deceive or mislead the addressee about the origin of such messages</li>
                <li>Contains software viruses or any other computer code, files or programs designed to interrupt, destroy or limit the functionality of any computer resource</li>
              </ul>
            </div>

            <div className="mb-8">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">5. Payment and Refund Policy</h3>
              <p className="text-gray-700 mb-4">
                All payments are processed through secure payment gateways. Subscription and access to subscription based Services fall under the purview of applicable Tax laws of India. Unless otherwise indicated, prices stated on Site are inclusive of applicable taxes, including but not limited to Goods and Services Tax (GST) or other applicable taxes.
              </p>
              <p className="text-gray-700 mb-4">
                Subscription to the subscription based Services commences immediately on the realisation of payment of the subscription fees from the Users and there can be no cancellation once a User's account is active for the subscription based Services.
              </p>
            </div>

            <div className="mb-8">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">6. Disclaimer of Warranties</h3>
              <p className="text-gray-700 mb-4">
                You understand and agree that the Company provides the Services on 'as-is' 'with all faults' and 'as available' basis. You agree that use of the Site or the Services is at your risk. All warranties including without limitation, the implied warranties of merchantability, fitness for a particular purpose, for the title and non-infringement are disclaimed and excluded.
              </p>
            </div>

            <div className="mb-8">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">7. Limitation of Liability</h3>
              <p className="text-gray-700 mb-4">
                The Company, its affiliates, successors, and assigns, and each of their respective investors, directors, officers, employees, agents, and suppliers shall not be liable, at any time for any, direct, indirect, punitive, incidental, special, consequential, damages arising out of or in any way connected with the use of Site or the Services.
              </p>
              <p className="text-gray-700 mb-4">
                In the event any exclusion contained herein be held to be invalid for any reason and the Company or any of its affiliate entities, officers, directors or employees become liable for loss or damage, then, any such liability shall be limited to not exceeding INR 100/-.
              </p>
            </div>

            <div className="mb-8">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">8. Indemnification</h3>
              <p className="text-gray-700 mb-4">
                You agree to indemnify, defend and hold harmless, the Company, its affiliates, successors, and assigns, and each of their respective investors, directors, officers, employees, agents, and suppliers from and against any losses, claims, damages, liabilities, including legal fees and expenses, arising out of your violation of these Terms or your use of the Site or Services.
              </p>
            </div>

            <div className="mb-8">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">9. Termination</h3>
              <p className="text-gray-700 mb-4">
                The Company reserves the right to change, suspend, or discontinue temporarily or permanently, some or all of the Services, with respect to any or all users, at any time without notice. The Company reserves the right to suspend or terminate your subscription if you breach these Terms.
              </p>
            </div>

            <div className="mb-8">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">10. Contact Information</h3>
              <p className="text-gray-700 mb-4">
                If you have any questions about these Terms & Conditions, please contact us at:
              </p>
              <div className="bg-gray-50 p-4 rounded-lg">
                <p className="text-gray-700"><strong>Email:</strong> support@shopforpremium.com</p>
                <p className="text-gray-700"><strong>WhatsApp:</strong> +91 9876543210</p>
                <p className="text-gray-700"><strong>Telegram:</strong> @shopforpremium</p>
              </div>
            </div>

            <div className="text-sm text-gray-500 border-t pt-4">
              <p>Last updated: {new Date().toLocaleDateString()}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TermsPage;