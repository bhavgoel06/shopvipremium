#!/bin/bash

# Shop VIP Premium - Create Information Pages
# This script creates all remaining information and admin pages

set -e

echo "📄 Creating information pages and admin dashboard..."
echo "=================================================="

cd /var/www/shopvippremium/frontend/src/pages

# Create AboutPage.js
cat > AboutPage.js << 'EOF'
import React from 'react';
import { Helmet } from 'react-helmet';
import { motion } from 'framer-motion';

const AboutPage = () => {
  return (
    <div className="min-h-screen bg-gray-900 py-12">
      <Helmet>
        <title>About Us - Shop VIP Premium</title>
        <meta name="description" content="Learn about Shop VIP Premium, your trusted source for premium digital workspace tools and productivity software." />
      </Helmet>

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <h1 className="text-4xl font-bold text-white mb-4">
            About Shop VIP Premium
          </h1>
          <p className="text-xl text-gray-400">
            Your trusted partner for premium digital workspace solutions
          </p>
        </motion.div>

        <div className="space-y-12">
          {/* Mission Section */}
          <motion.section
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="bg-gray-800 rounded-xl p-8"
          >
            <h2 className="text-2xl font-bold text-white mb-6">Our Mission</h2>
            <p className="text-gray-300 text-lg leading-relaxed">
              At Shop VIP Premium, we're dedicated to empowering professionals, freelancers, and businesses 
              with cutting-edge digital workspace tools. Our mission is to provide access to premium productivity 
              software, business utilities, and professional-grade applications that enhance your workflow and 
              boost your success.
            </p>
          </motion.section>

          {/* What We Offer */}
          <motion.section
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="bg-gray-800 rounded-xl p-8"
          >
            <h2 className="text-2xl font-bold text-white mb-6">What We Offer</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="space-y-4">
                <div className="flex items-center space-x-3">
                  <div className="w-8 h-8 bg-blue-500 rounded-full flex items-center justify-center">
                    <span className="text-white text-sm">💼</span>
                  </div>
                  <h3 className="text-lg font-semibold text-white">Business Tools</h3>
                </div>
                <p className="text-gray-400">
                  Professional business software and productivity suites designed for modern enterprises.
                </p>
              </div>

              <div className="space-y-4">
                <div className="flex items-center space-x-3">
                  <div className="w-8 h-8 bg-green-500 rounded-full flex items-center justify-center">
                    <span className="text-white text-sm">🎨</span>
                  </div>
                  <h3 className="text-lg font-semibold text-white">Creative Suite</h3>
                </div>
                <p className="text-gray-400">
                  Advanced creative tools for designers, artists, and content creators.
                </p>
              </div>

              <div className="space-y-4">
                <div className="flex items-center space-x-3">
                  <div className="w-8 h-8 bg-purple-500 rounded-full flex items-center justify-center">
                    <span className="text-white text-sm">⚡</span>
                  </div>
                  <h3 className="text-lg font-semibold text-white">Productivity Tools</h3>
                </div>
                <p className="text-gray-400">
                  Efficiency-enhancing applications to streamline your workflow and maximize output.
                </p>
              </div>

              <div className="space-y-4">
                <div className="flex items-center space-x-3">
                  <div className="w-8 h-8 bg-red-500 rounded-full flex items-center justify-center">
                    <span className="text-white text-sm">🔧</span>
                  </div>
                  <h3 className="text-lg font-semibold text-white">Developer Utilities</h3>
                </div>
                <p className="text-gray-400">
                  Essential development tools and utilities for programmers and software engineers.
                </p>
              </div>
            </div>
          </motion.section>

          {/* Why Choose Us */}
          <motion.section
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="bg-gray-800 rounded-xl p-8"
          >
            <h2 className="text-2xl font-bold text-white mb-6">Why Choose Shop VIP Premium?</h2>
            <div className="space-y-6">
              <div className="flex items-start space-x-4">
                <div className="w-6 h-6 bg-blue-500 rounded-full flex items-center justify-center mt-1">
                  <span className="text-white text-xs">✓</span>
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-white mb-2">Premium Quality</h3>
                  <p className="text-gray-400">
                    We curate only the highest quality digital tools and software solutions.
                  </p>
                </div>
              </div>

              <div className="flex items-start space-x-4">
                <div className="w-6 h-6 bg-green-500 rounded-full flex items-center justify-center mt-1">
                  <span className="text-white text-xs">✓</span>
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-white mb-2">Secure Payments</h3>
                  <p className="text-gray-400">
                    Safe and secure cryptocurrency payments with full encryption protection.
                  </p>
                </div>
              </div>

              <div className="flex items-start space-x-4">
                <div className="w-6 h-6 bg-purple-500 rounded-full flex items-center justify-center mt-1">
                  <span className="text-white text-xs">✓</span>
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-white mb-2">24/7 Support</h3>
                  <p className="text-gray-400">
                    Round-the-clock customer support via Telegram and WhatsApp.
                  </p>
                </div>
              </div>

              <div className="flex items-start space-x-4">
                <div className="w-6 h-6 bg-yellow-500 rounded-full flex items-center justify-center mt-1">
                  <span className="text-white text-xs">✓</span>
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-white mb-2">Instant Delivery</h3>
                  <p className="text-gray-400">
                    Quick delivery of digital products after payment confirmation.
                  </p>
                </div>
              </div>
            </div>
          </motion.section>

          {/* Contact Information */}
          <motion.section
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 }}
            className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl p-8 text-center"
          >
            <h2 className="text-2xl font-bold text-white mb-4">Get In Touch</h2>
            <p className="text-blue-100 mb-6">
              Have questions or need support? We're here to help you succeed.
            </p>
            <div className="flex justify-center space-x-6">
              <a
                href="https://t.me/shopvippremium"
                target="_blank"
                rel="noopener noreferrer"
                className="bg-white bg-opacity-20 text-white px-6 py-3 rounded-lg hover:bg-opacity-30 transition-all duration-200"
              >
                📱 Telegram Support
              </a>
              <a
                href="https://wa.me/1234567890"
                target="_blank"
                rel="noopener noreferrer"
                className="bg-white bg-opacity-20 text-white px-6 py-3 rounded-lg hover:bg-opacity-30 transition-all duration-200"
              >
                💬 WhatsApp Support
              </a>
            </div>
          </motion.section>
        </div>
      </div>
    </div>
  );
};

export default AboutPage;
EOF

# Create ContactPage.js
cat > ContactPage.js << 'EOF'
import React, { useState } from 'react';
import { Helmet } from 'react-helmet';
import { motion } from 'framer-motion';
import { toast } from 'react-toastify';

const ContactPage = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    subject: '',
    message: ''
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // For now, just show a message (would typically send to backend)
    toast.success('Thank you for your message! We\'ll get back to you soon via Telegram or WhatsApp.');
    setFormData({ name: '', email: '', subject: '', message: '' });
  };

  return (
    <div className="min-h-screen bg-gray-900 py-12">
      <Helmet>
        <title>Contact Us - Shop VIP Premium</title>
        <meta name="description" content="Get in touch with Shop VIP Premium for support, questions, or feedback. We're here to help!" />
      </Helmet>

      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <h1 className="text-4xl font-bold text-white mb-4">Contact Us</h1>
          <p className="text-xl text-gray-400">
            We're here to help with any questions or support you need
          </p>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
          {/* Contact Form */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
            className="bg-gray-800 rounded-xl p-8"
          >
            <h2 className="text-2xl font-bold text-white mb-6">Send us a Message</h2>
            
            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Full Name
                  </label>
                  <input
                    type="text"
                    name="name"
                    required
                    value={formData.name}
                    onChange={handleChange}
                    className="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-2 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="Your full name"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-300 mb-2">
                    Email Address
                  </label>
                  <input
                    type="email"
                    name="email"
                    required
                    value={formData.email}
                    onChange={handleChange}
                    className="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-2 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="your@email.com"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Subject
                </label>
                <input
                  type="text"
                  name="subject"
                  required
                  value={formData.subject}
                  onChange={handleChange}
                  className="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-2 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="How can we help?"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  Message
                </label>
                <textarea
                  name="message"
                  required
                  rows={6}
                  value={formData.message}
                  onChange={handleChange}
                  className="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-2 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
                  placeholder="Tell us more about your inquiry..."
                />
              </div>

              <button
                type="submit"
                className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors"
              >
                Send Message
              </button>
            </form>
          </motion.div>

          {/* Contact Information */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.3 }}
            className="space-y-8"
          >
            {/* Direct Contact */}
            <div className="bg-gray-800 rounded-xl p-8">
              <h2 className="text-2xl font-bold text-white mb-6">Direct Contact</h2>
              <div className="space-y-6">
                <div className="flex items-start space-x-4">
                  <div className="w-12 h-12 bg-blue-500 rounded-full flex items-center justify-center">
                    <span className="text-white text-lg">📱</span>
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-white">Telegram Support</h3>
                    <p className="text-gray-400 mb-2">Fast and reliable support via Telegram</p>
                    <a
                      href="https://t.me/shopvippremium"
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-block bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
                    >
                      Contact on Telegram
                    </a>
                  </div>
                </div>

                <div className="flex items-start space-x-4">
                  <div className="w-12 h-12 bg-green-500 rounded-full flex items-center justify-center">
                    <span className="text-white text-lg">💬</span>
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-white">WhatsApp Support</h3>
                    <p className="text-gray-400 mb-2">Connect with us on WhatsApp</p>
                    <a
                      href="https://wa.me/1234567890"
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-block bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700 transition-colors"
                    >
                      Chat on WhatsApp
                    </a>
                  </div>
                </div>
              </div>
            </div>

            {/* Support Hours */}
            <div className="bg-gray-800 rounded-xl p-8">
              <h2 className="text-2xl font-bold text-white mb-6">Support Hours</h2>
              <div className="space-y-3">
                <div className="flex justify-between items-center text-gray-300">
                  <span>Monday - Friday:</span>
                  <span className="text-white font-semibold">24/7</span>
                </div>
                <div className="flex justify-between items-center text-gray-300">
                  <span>Saturday - Sunday:</span>
                  <span className="text-white font-semibold">24/7</span>
                </div>
                <div className="mt-4 p-3 bg-green-900 bg-opacity-30 rounded-lg">
                  <p className="text-green-300 text-sm">
                    ✅ We provide 24/7 support for all our customers
                  </p>
                </div>
              </div>
            </div>

            {/* FAQ Note */}
            <div className="bg-gray-800 rounded-xl p-8">
              <h2 className="text-2xl font-bold text-white mb-4">Before You Contact</h2>
              <div className="space-y-3 text-gray-300">
                <p>Common questions we can help with:</p>
                <ul className="space-y-2 ml-4">
                  <li>• Product delivery and access issues</li>
                  <li>• Payment and billing questions</li>
                  <li>• Technical support for digital products</li>
                  <li>• Account and order management</li>
                  <li>• Refund and return policies</li>
                </ul>
              </div>
            </div>
          </motion.div>
        </div>
      </div>
    </div>
  );
};

export default ContactPage;
EOF

# Create PrivacyPage.js
cat > PrivacyPage.js << 'EOF'
import React from 'react';
import { Helmet } from 'react-helmet';
import { motion } from 'framer-motion';

const PrivacyPage = () => {
  return (
    <div className="min-h-screen bg-gray-900 py-12">
      <Helmet>
        <title>Privacy Policy - Shop VIP Premium</title>
        <meta name="description" content="Privacy Policy for Shop VIP Premium - Learn how we protect and handle your personal information." />
      </Helmet>

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <h1 className="text-4xl font-bold text-white mb-4">Privacy Policy</h1>
          <p className="text-gray-400">Last updated: June 2025</p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="bg-gray-800 rounded-xl p-8 prose prose-invert max-w-none"
        >
          <div className="space-y-8 text-gray-300">
            <section>
              <h2 className="text-2xl font-bold text-white mb-4">Information We Collect</h2>
              <p>
                When you use Shop VIP Premium, we may collect the following types of information:
              </p>
              <ul className="ml-6 space-y-2">
                <li>Personal identification information (name, email address, username)</li>
                <li>Payment information (processed securely through our payment processors)</li>
                <li>Usage data (how you interact with our website and services)</li>
                <li>Technical information (IP address, browser type, device information)</li>
              </ul>
            </section>

            <section>
              <h2 className="text-2xl font-bold text-white mb-4">How We Use Your Information</h2>
              <p>We use the collected information for the following purposes:</p>
              <ul className="ml-6 space-y-2">
                <li>To provide and maintain our services</li>
                <li>To process transactions and deliver digital products</li>
                <li>To communicate with you about your orders and account</li>
                <li>To improve our website and user experience</li>
                <li>To comply with legal obligations</li>
              </ul>
            </section>

            <section>
              <h2 className="text-2xl font-bold text-white mb-4">Information Sharing</h2>
              <p>
                We do not sell, trade, or otherwise transfer your personal information to third parties, 
                except in the following circumstances:
              </p>
              <ul className="ml-6 space-y-2">
                <li>With your explicit consent</li>
                <li>To process payments through secure payment processors</li>
                <li>To comply with legal requirements or protect our rights</li>
                <li>In connection with a business transfer or merger</li>
              </ul>
            </section>

            <section>
              <h2 className="text-2xl font-bold text-white mb-4">Data Security</h2>
              <p>
                We implement appropriate security measures to protect your personal information against 
                unauthorized access, alteration, disclosure, or destruction. This includes:
              </p>
              <ul className="ml-6 space-y-2">
                <li>SSL encryption for data transmission</li>
                <li>Secure storage of personal information</li>
                <li>Regular security assessments and updates</li>
                <li>Limited access to personal data on a need-to-know basis</li>
              </ul>
            </section>

            <section>
              <h2 className="text-2xl font-bold text-white mb-4">Cookies and Tracking</h2>
              <p>
                We use cookies and similar technologies to enhance your experience on our website. 
                These technologies help us:
              </p>
              <ul className="ml-6 space-y-2">
                <li>Remember your preferences and settings</li>
                <li>Analyze website usage and performance</li>
                <li>Provide personalized content and recommendations</li>
                <li>Prevent fraud and enhance security</li>
              </ul>
            </section>

            <section>
              <h2 className="text-2xl font-bold text-white mb-4">Your Rights</h2>
              <p>You have the right to:</p>
              <ul className="ml-6 space-y-2">
                <li>Access your personal information</li>
                <li>Update or correct your information</li>
                <li>Delete your account and associated data</li>
                <li>Object to the processing of your information</li>
                <li>Request data portability</li>
              </ul>
            </section>

            <section>
              <h2 className="text-2xl font-bold text-white mb-4">Data Retention</h2>
              <p>
                We retain your personal information only as long as necessary to fulfill the purposes 
                outlined in this Privacy Policy, unless a longer retention period is required by law.
              </p>
            </section>

            <section>
              <h2 className="text-2xl font-bold text-white mb-4">International Transfers</h2>
              <p>
                Your information may be transferred to and processed in countries other than your own. 
                We ensure appropriate safeguards are in place to protect your information in accordance 
                with this Privacy Policy.
              </p>
            </section>

            <section>
              <h2 className="text-2xl font-bold text-white mb-4">Children's Privacy</h2>
              <p>
                Our services are not intended for individuals under the age of 18. We do not knowingly 
                collect personal information from children under 18. If we become aware of such collection, 
                we will take steps to delete the information.
              </p>
            </section>

            <section>
              <h2 className="text-2xl font-bold text-white mb-4">Changes to This Policy</h2>
              <p>
                We may update this Privacy Policy from time to time. We will notify you of any material 
                changes by posting the new Privacy Policy on this page and updating the "Last updated" date.
              </p>
            </section>

            <section>
              <h2 className="text-2xl font-bold text-white mb-4">Contact Information</h2>
              <p>
                If you have any questions about this Privacy Policy or our data practices, please contact us:
              </p>
              <div className="bg-gray-700 rounded-lg p-4 mt-4">
                <div className="flex space-x-6">
                  <a
                    href="https://t.me/shopvippremium"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-400 hover:text-blue-300"
                  >
                    📱 Telegram Support
                  </a>
                  <a
                    href="https://wa.me/1234567890"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-green-400 hover:text-green-300"
                  >
                    💬 WhatsApp Support
                  </a>
                </div>
              </div>
            </section>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default PrivacyPage;
EOF

# Create TermsPage.js
cat > TermsPage.js << 'EOF'
import React from 'react';
import { Helmet } from 'react-helmet';
import { motion } from 'framer-motion';

const TermsPage = () => {
  return (
    <div className="min-h-screen bg-gray-900 py-12">
      <Helmet>
        <title>Terms & Conditions - Shop VIP Premium</title>
        <meta name="description" content="Terms and Conditions for Shop VIP Premium - Read our service terms, user agreements, and policies." />
      </Helmet>

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <h1 className="text-4xl font-bold text-white mb-4">Terms & Conditions</h1>
          <p className="text-gray-400">Last updated: June 2025</p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="bg-gray-800 rounded-xl p-8 prose prose-invert max-w-none"
        >
          <div className="space-y-8 text-gray-300">
            <section>
              <h2 className="text-2xl font-bold text-white mb-4">Acceptance of Terms</h2>
              <p>
                By accessing and using Shop VIP Premium services, you accept and agree to be bound by 
                the terms and provision of this agreement. If you do not agree to abide by the above, 
                please do not use this service.
              </p>
            </section>

            <section>
              <h2 className="text-2xl font-bold text-white mb-4">Service Description</h2>
              <p>
                Shop VIP Premium provides digital workspace tools, productivity software, and business 
                utilities. Our services include:
              </p>
              <ul className="ml-6 space-y-2">
                <li>Access to premium digital tools and software</li>
                <li>Digital product delivery via secure channels</li>
                <li>Customer support via Telegram and WhatsApp</li>
                <li>Account management and order tracking</li>
              </ul>
            </section>

            <section>
              <h2 className="text-2xl font-bold text-white mb-4">User Accounts</h2>
              <p>To use our services, you must:</p>
              <ul className="ml-6 space-y-2">
                <li>Be at least 18 years of age</li>
                <li>Provide accurate and complete registration information</li>
                <li>Maintain the security of your account credentials</li>
                <li>Notify us immediately of any unauthorized use of your account</li>
                <li>Accept responsibility for all activities under your account</li>
              </ul>
            </section>

            <section>
              <h2 className="text-2xl font-bold text-white mb-4">Products and Services</h2>
              <p>
                All products sold through Shop VIP Premium are digital tools and utilities. 
                By purchasing our products, you agree that:
              </p>
              <ul className="ml-6 space-y-2">
                <li>Products are for personal or business use only</li>
                <li>You will not redistribute or resell our products</li>
                <li>Product descriptions and features may vary</li>
                <li>We reserve the right to modify or discontinue products</li>
              </ul>
            </section>

            <section>
              <h2 className="text-2xl font-bold text-white mb-4">Payment and Billing</h2>
              <p>Payment terms and conditions:</p>
              <ul className="ml-6 space-y-2">
                <li>All payments are processed securely through our payment providers</li>
                <li>Prices are displayed in USD and INR</li>
                <li>Payment is required before product delivery</li>
                <li>Cryptocurrency payments are processed through Nowpayments</li>
                <li>Failed payments may result in order cancellation</li>
              </ul>
            </section>

            <section>
              <h2 className="text-2xl font-bold text-white mb-4">Refunds and Returns</h2>
              <p>
                Due to the digital nature of our products:
              </p>
              <ul className="ml-6 space-y-2">
                <li>All sales are final once the product is delivered</li>
                <li>Refunds may be considered for technical issues preventing product use</li>
                <li>Refund requests must be made within 7 days of purchase</li>
                <li>Each refund request will be evaluated on a case-by-case basis</li>
                <li>Contact support via Telegram or WhatsApp for refund requests</li>
              </ul>
            </section>

            <section>
              <h2 className="text-2xl font-bold text-white mb-4">Intellectual Property</h2>
              <p>
                All content, trademarks, and intellectual property on Shop VIP Premium are 
                protected by copyright and other intellectual property laws. You agree to:
              </p>
              <ul className="ml-6 space-y-2">
                <li>Not copy, modify, or distribute our content without permission</li>
                <li>Respect the intellectual property rights of product creators</li>
                <li>Use products only as licensed or permitted</li>
                <li>Not reverse engineer or attempt to extract source code</li>
              </ul>
            </section>

            <section>
              <h2 className="text-2xl font-bold text-white mb-4">Prohibited Uses</h2>
              <p>You may not use our service:</p>
              <ul className="ml-6 space-y-2">
                <li>For any unlawful purpose or to solicit others to perform unlawful acts</li>
                <li>To violate any international, federal, provincial, or state regulations or laws</li>
                <li>To transmit or procure the sending of any advertising or promotional material</li>
                <li>To impersonate or attempt to impersonate the company or other users</li>
                <li>To engage in any other conduct that restricts or inhibits anyone's use of the website</li>
              </ul>
            </section>

            <section>
              <h2 className="text-2xl font-bold text-white mb-4">Disclaimers</h2>
              <p>
                Our services are provided "as is" without any representations or warranties. 
                We disclaim all warranties, express or implied, including but not limited to:
              </p>
              <ul className="ml-6 space-y-2">
                <li>Merchantability and fitness for a particular purpose</li>
                <li>Non-infringement of third-party rights</li>
                <li>Continuous, uninterrupted, or error-free service</li>
                <li>Accuracy or completeness of content</li>
              </ul>
            </section>

            <section>
              <h2 className="text-2xl font-bold text-white mb-4">Limitation of Liability</h2>
              <p>
                Shop VIP Premium shall not be liable for any indirect, incidental, special, 
                consequential, or punitive damages, including but not limited to loss of profits, 
                data, use, goodwill, or other intangible losses.
              </p>
            </section>

            <section>
              <h2 className="text-2xl font-bold text-white mb-4">Termination</h2>
              <p>
                We may terminate or suspend your account and access to our services immediately, 
                without prior notice, for any reason, including breach of these Terms.
              </p>
            </section>

            <section>
              <h2 className="text-2xl font-bold text-white mb-4">Changes to Terms</h2>
              <p>
                We reserve the right to modify these terms at any time. Changes will be effective 
                immediately upon posting. Your continued use of the service constitutes acceptance 
                of the modified terms.
              </p>
            </section>

            <section>
              <h2 className="text-2xl font-bold text-white mb-4">Contact Information</h2>
              <p>
                If you have any questions about these Terms & Conditions, please contact us:
              </p>
              <div className="bg-gray-700 rounded-lg p-4 mt-4">
                <div className="flex space-x-6">
                  <a
                    href="https://t.me/shopvippremium"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-400 hover:text-blue-300"
                  >
                    📱 Telegram Support
                  </a>
                  <a
                    href="https://wa.me/1234567890"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-green-400 hover:text-green-300"
                  >
                    💬 WhatsApp Support
                  </a>
                </div>
              </div>
            </section>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default TermsPage;
EOF

# Create AdminDashboard.js (Comprehensive Admin Panel)
cat > AdminDashboard.js << 'EOF'
import React, { useState, useEffect } from 'react';
import { Helmet } from 'react-helmet';
import { toast } from 'react-toastify';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';
import { useCurrency } from '../context/CurrencyContext';
import {
  ChartBarIcon,
  ShoppingBagIcon,
  UsersIcon,
  CurrencyDollarIcon,
  PlusIcon,
  TrashIcon,
  PencilIcon
} from '@heroicons/react/24/outline';

const AdminDashboard = () => {
  const { user, login } = useAuth();
  const { formatPrice } = useCurrency();
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [loginForm, setLoginForm] = useState({ email: '', password: '' });
  const [activeTab, setActiveTab] = useState('dashboard');
  const [loading, setLoading] = useState(false);

  // Dashboard data
  const [dashboardStats, setDashboardStats] = useState({});
  const [products, setProducts] = useState([]);
  const [orders, setOrders] = useState([]);
  const [users, setUsers] = useState([]);

  // Product form
  const [productForm, setProductForm] = useState({
    name: '',
    description: '',
    price_usd: '',
    price_inr: '',
    category: '',
    image_url: '',
    is_featured: false,
    is_bestseller: false
  });

  const API_URL = process.env.REACT_APP_BACKEND_URL;

  useEffect(() => {
    if (user && user.role === 'admin') {
      setIsLoggedIn(true);
      fetchDashboardData();
    }
  }, [user]);

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const result = await login(loginForm.email, loginForm.password);
      
      if (result.success) {
        toast.success('Admin login successful!');
        // The useEffect will handle setting isLoggedIn when user updates
      } else {
        toast.error(result.error || 'Invalid admin credentials');
      }
    } catch (error) {
      toast.error('Login failed');
    } finally {
      setLoading(false);
    }
  };

  const fetchDashboardData = async () => {
    try {
      const [statsRes, productsRes, ordersRes, usersRes] = await Promise.all([
        axios.get(`${API_URL}/api/admin/dashboard`),
        axios.get(`${API_URL}/api/products?limit=20`),
        axios.get(`${API_URL}/api/admin/orders?limit=20`),
        axios.get(`${API_URL}/api/admin/users?limit=20`)
      ]);

      setDashboardStats(statsRes.data);
      setProducts(productsRes.data.products);
      setOrders(ordersRes.data.orders);
      setUsers(usersRes.data.users);
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
      toast.error('Failed to load dashboard data');
    }
  };

  const handleProductSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      await axios.post(`${API_URL}/api/admin/products`, {
        ...productForm,
        price_usd: parseFloat(productForm.price_usd),
        price_inr: parseFloat(productForm.price_inr)
      });

      toast.success('Product created successfully!');
      setProductForm({
        name: '', description: '', price_usd: '', price_inr: '',
        category: '', image_url: '', is_featured: false, is_bestseller: false
      });
      fetchDashboardData();
    } catch (error) {
      toast.error('Failed to create product');
    } finally {
      setLoading(false);
    }
  };

  const deleteProduct = async (productId) => {
    if (!window.confirm('Are you sure you want to delete this product?')) {
      return;
    }

    try {
      await axios.delete(`${API_URL}/api/admin/products/${productId}`);
      toast.success('Product deleted successfully!');
      fetchDashboardData();
    } catch (error) {
      toast.error('Failed to delete product');
    }
  };

  // Login Form Component
  if (!isLoggedIn || !user || user.role !== 'admin') {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center py-12 px-4">
        <Helmet>
          <title>Admin Login - Shop VIP Premium</title>
        </Helmet>

        <div className="max-w-md w-full">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-white mb-2">Admin Panel</h1>
            <p className="text-gray-400">Login to access the admin dashboard</p>
          </div>

          <form onSubmit={handleLogin} className="bg-gray-800 rounded-xl p-8 space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Admin Email
              </label>
              <input
                type="email"
                required
                value={loginForm.email}
                onChange={(e) => setLoginForm({...loginForm, email: e.target.value})}
                className="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="admin@shopvippremium.com"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Password
              </label>
              <input
                type="password"
                required
                value={loginForm.password}
                onChange={(e) => setLoginForm({...loginForm, password: e.target.value})}
                className="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Enter admin password"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors disabled:opacity-50"
            >
              {loading ? 'Signing in...' : 'Sign In'}
            </button>

            <div className="text-center text-xs text-gray-500">
              Demo: admin@shopvippremium.com / admin123
            </div>
          </form>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-900">
      <Helmet>
        <title>Admin Dashboard - Shop VIP Premium</title>
      </Helmet>

      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">Admin Dashboard</h1>
          <p className="text-gray-400">Welcome back, {user.username}</p>
        </div>

        {/* Navigation Tabs */}
        <div className="bg-gray-800 rounded-xl p-1 mb-8">
          <nav className="flex space-x-1">
            {[
              { id: 'dashboard', label: 'Dashboard', icon: ChartBarIcon },
              { id: 'products', label: 'Products', icon: ShoppingBagIcon },
              { id: 'orders', label: 'Orders', icon: CurrencyDollarIcon },
              { id: 'users', label: 'Users', icon: UsersIcon }
            ].map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center space-x-2 px-4 py-2 rounded-lg font-medium transition-colors ${
                  activeTab === tab.id
                    ? 'bg-blue-600 text-white'
                    : 'text-gray-400 hover:text-white hover:bg-gray-700'
                }`}
              >
                <tab.icon className="h-5 w-5" />
                <span>{tab.label}</span>
              </button>
            ))}
          </nav>
        </div>

        {/* Dashboard Tab */}
        {activeTab === 'dashboard' && (
          <div className="space-y-8">
            {/* Stats Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <div className="bg-gray-800 rounded-xl p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-gray-400 text-sm">Total Revenue</p>
                    <p className="text-2xl font-bold text-white">
                      ${dashboardStats.total_revenue || 0}
                    </p>
                  </div>
                  <CurrencyDollarIcon className="h-8 w-8 text-green-400" />
                </div>
              </div>

              <div className="bg-gray-800 rounded-xl p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-gray-400 text-sm">Total Orders</p>
                    <p className="text-2xl font-bold text-white">
                      {dashboardStats.total_orders || 0}
                    </p>
                  </div>
                  <ShoppingBagIcon className="h-8 w-8 text-blue-400" />
                </div>
              </div>

              <div className="bg-gray-800 rounded-xl p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-gray-400 text-sm">Total Products</p>
                    <p className="text-2xl font-bold text-white">
                      {dashboardStats.total_products || 0}
                    </p>
                  </div>
                  <ShoppingBagIcon className="h-8 w-8 text-purple-400" />
                </div>
              </div>

              <div className="bg-gray-800 rounded-xl p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-gray-400 text-sm">Total Users</p>
                    <p className="text-2xl font-bold text-white">
                      {dashboardStats.total_users || 0}
                    </p>
                  </div>
                  <UsersIcon className="h-8 w-8 text-yellow-400" />
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Products Tab */}
        {activeTab === 'products' && (
          <div className="space-y-8">
            {/* Add Product Form */}
            <div className="bg-gray-800 rounded-xl p-6">
              <h2 className="text-xl font-bold text-white mb-4">Add New Product</h2>
              <form onSubmit={handleProductSubmit} className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <input
                  type="text"
                  placeholder="Product Name"
                  required
                  value={productForm.name}
                  onChange={(e) => setProductForm({...productForm, name: e.target.value})}
                  className="bg-gray-700 border border-gray-600 rounded-lg px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                />

                <input
                  type="text"
                  placeholder="Category"
                  required
                  value={productForm.category}
                  onChange={(e) => setProductForm({...productForm, category: e.target.value})}
                  className="bg-gray-700 border border-gray-600 rounded-lg px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                />

                <input
                  type="number"
                  placeholder="Price USD"
                  step="0.01"
                  required
                  value={productForm.price_usd}
                  onChange={(e) => setProductForm({...productForm, price_usd: e.target.value})}
                  className="bg-gray-700 border border-gray-600 rounded-lg px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                />

                <input
                  type="number"
                  placeholder="Price INR"
                  step="0.01"
                  required
                  value={productForm.price_inr}
                  onChange={(e) => setProductForm({...productForm, price_inr: e.target.value})}
                  className="bg-gray-700 border border-gray-600 rounded-lg px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                />

                <input
                  type="url"
                  placeholder="Image URL"
                  value={productForm.image_url}
                  onChange={(e) => setProductForm({...productForm, image_url: e.target.value})}
                  className="bg-gray-700 border border-gray-600 rounded-lg px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                />

                <div className="flex items-center space-x-4">
                  <label className="flex items-center text-white">
                    <input
                      type="checkbox"
                      checked={productForm.is_featured}
                      onChange={(e) => setProductForm({...productForm, is_featured: e.target.checked})}
                      className="mr-2"
                    />
                    Featured
                  </label>
                  <label className="flex items-center text-white">
                    <input
                      type="checkbox"
                      checked={productForm.is_bestseller}
                      onChange={(e) => setProductForm({...productForm, is_bestseller: e.target.checked})}
                      className="mr-2"
                    />
                    Bestseller
                  </label>
                </div>

                <textarea
                  placeholder="Product Description"
                  required
                  rows={3}
                  value={productForm.description}
                  onChange={(e) => setProductForm({...productForm, description: e.target.value})}
                  className="md:col-span-2 bg-gray-700 border border-gray-600 rounded-lg px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
                />

                <button
                  type="submit"
                  disabled={loading}
                  className="md:col-span-2 bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors disabled:opacity-50"
                >
                  {loading ? 'Adding...' : 'Add Product'}
                </button>
              </form>
            </div>

            {/* Products List */}
            <div className="bg-gray-800 rounded-xl overflow-hidden">
              <div className="p-6 border-b border-gray-700">
                <h2 className="text-xl font-bold text-white">All Products</h2>
              </div>
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead className="bg-gray-700">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase">Product</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase">Category</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase">Price</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase">Status</th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase">Actions</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-gray-700">
                    {products.map((product) => (
                      <tr key={product.id}>
                        <td className="px-6 py-4">
                          <div className="flex items-center">
                            <img className="h-10 w-10 rounded-lg object-cover mr-3" src={product.image_url} alt="" />
                            <div>
                              <div className="text-sm font-medium text-white">{product.name}</div>
                              <div className="text-sm text-gray-400">{product.description?.substring(0, 50)}...</div>
                            </div>
                          </div>
                        </td>
                        <td className="px-6 py-4 text-sm text-gray-300">{product.category}</td>
                        <td className="px-6 py-4 text-sm text-white">{formatPrice(product.price_usd, product.price_inr)}</td>
                        <td className="px-6 py-4">
                          <div className="flex space-x-1">
                            {product.is_featured && (
                              <span className="px-2 py-1 text-xs bg-yellow-100 text-yellow-800 rounded-full">Featured</span>
                            )}
                            {product.is_bestseller && (
                              <span className="px-2 py-1 text-xs bg-green-100 text-green-800 rounded-full">Bestseller</span>
                            )}
                          </div>
                        </td>
                        <td className="px-6 py-4">
                          <button
                            onClick={() => deleteProduct(product.id)}
                            className="text-red-400 hover:text-red-300"
                          >
                            <TrashIcon className="h-5 w-5" />
                          </button>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {/* Orders Tab */}
        {activeTab === 'orders' && (
          <div className="bg-gray-800 rounded-xl overflow-hidden">
            <div className="p-6 border-b border-gray-700">
              <h2 className="text-xl font-bold text-white">Recent Orders</h2>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-700">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase">Order ID</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase">User</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase">Amount</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase">Status</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase">Date</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-700">
                  {orders.map((order) => (
                    <tr key={order.id}>
                      <td className="px-6 py-4 text-sm font-mono text-white">{order.id.substring(0, 8)}...</td>
                      <td className="px-6 py-4 text-sm text-gray-300">{order.user_id}</td>
                      <td className="px-6 py-4 text-sm text-white">${order.total_amount}</td>
                      <td className="px-6 py-4">
                        <span className={`px-2 py-1 text-xs rounded-full ${
                          order.status === 'completed' 
                            ? 'bg-green-100 text-green-800' 
                            : order.status === 'pending'
                            ? 'bg-yellow-100 text-yellow-800'
                            : 'bg-red-100 text-red-800'
                        }`}>
                          {order.status}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-300">
                        {new Date(order.created_at).toLocaleDateString()}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Users Tab */}
        {activeTab === 'users' && (
          <div className="bg-gray-800 rounded-xl overflow-hidden">
            <div className="p-6 border-b border-gray-700">
              <h2 className="text-xl font-bold text-white">All Users</h2>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-700">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase">User</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase">Email</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase">Role</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-300 uppercase">Joined</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-700">
                  {users.map((user) => (
                    <tr key={user.id}>
                      <td className="px-6 py-4 text-sm font-medium text-white">{user.username}</td>
                      <td className="px-6 py-4 text-sm text-gray-300">{user.email}</td>
                      <td className="px-6 py-4">
                        <span className={`px-2 py-1 text-xs rounded-full ${
                          user.role === 'admin' 
                            ? 'bg-purple-100 text-purple-800' 
                            : 'bg-blue-100 text-blue-800'
                        }`}>
                          {user.role}
                        </span>
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-300">
                        {new Date(user.created_at).toLocaleDateString()}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default AdminDashboard;
EOF

echo ""
echo "✅ All information pages and admin dashboard created successfully!"
echo "🎯 Ready for final deployment!"