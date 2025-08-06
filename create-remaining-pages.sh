#!/bin/bash

# Shop VIP Premium - Create Remaining Pages
# This script creates all remaining React page components

set -e

echo "📄 Creating remaining frontend pages..."
echo "===================================="

cd /var/www/shopvippremium/frontend/src/pages

# Create CheckoutPage.js
cat > CheckoutPage.js << 'EOF'
import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { Helmet } from 'react-helmet';
import { toast } from 'react-toastify';
import axios from 'axios';
import { useAuth } from '../context/AuthContext';
import { useCurrency } from '../context/CurrencyContext';

const CheckoutPage = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { user } = useAuth();
  const { formatPrice, currency } = useCurrency();
  const [order, setOrder] = useState(null);
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [processing, setProcessing] = useState(false);
  const [paymentMethod, setPaymentMethod] = useState('crypto');
  const [cryptoCurrency, setCryptoCurrency] = useState('btc');
  
  const API_URL = process.env.REACT_APP_BACKEND_URL;

  useEffect(() => {
    if (!user) {
      navigate('/login');
      return;
    }

    const { orderId, product: productData } = location.state || {};
    
    if (!orderId) {
      toast.error('Invalid checkout session');
      navigate('/products');
      return;
    }

    fetchOrderDetails(orderId);
    if (productData) {
      setProduct(productData);
    }
  }, [user, location.state, navigate]);

  const fetchOrderDetails = async (orderId) => {
    try {
      const response = await axios.get(`${API_URL}/api/orders/${orderId}`);
      setOrder(response.data);
    } catch (error) {
      console.error('Error fetching order:', error);
      toast.error('Order not found');
      navigate('/products');
    } finally {
      setLoading(false);
    }
  };

  const handlePayment = async () => {
    if (paymentMethod === 'crypto') {
      await handleCryptoPayment();
    }
  };

  const handleCryptoPayment = async () => {
    setProcessing(true);

    try {
      const paymentData = {
        order_id: order.id,
        currency: cryptoCurrency
      };

      const response = await axios.post(`${API_URL}/api/payments/crypto`, paymentData);
      
      if (response.data.payment_url) {
        // Redirect to payment URL
        window.location.href = response.data.payment_url;
      } else {
        toast.error('Failed to create payment. Please try again.');
      }
    } catch (error) {
      console.error('Error creating payment:', error);
      toast.error('Payment creation failed. Please try again.');
    } finally {
      setProcessing(false);
    }
  };

  if (!user) {
    return null;
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (!order) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-white mb-4">Order Not Found</h2>
          <button
            onClick={() => navigate('/products')}
            className="btn-primary"
          >
            Back to Products
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-900 py-8">
      <Helmet>
        <title>Checkout - Shop VIP Premium</title>
        <meta name="description" content="Secure checkout with cryptocurrency payment" />
      </Helmet>

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-white mb-2">Checkout</h1>
          <p className="text-gray-400">Complete your purchase securely</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Order Summary */}
          <div className="bg-gray-800 rounded-xl p-6">
            <h2 className="text-xl font-semibold text-white mb-6">Order Summary</h2>
            
            {product && (
              <div className="flex items-center space-x-4 mb-6">
                <img
                  src={product.image_url}
                  alt={product.name}
                  className="w-16 h-16 object-cover rounded-lg"
                />
                <div className="flex-1">
                  <h3 className="text-white font-medium">{product.name}</h3>
                  <p className="text-gray-400 text-sm">{product.category}</p>
                </div>
                <div className="text-right">
                  <div className="text-blue-400 font-bold">
                    {formatPrice(product.price_usd, product.price_inr)}
                  </div>
                </div>
              </div>
            )}

            <div className="border-t border-gray-700 pt-6">
              <div className="flex justify-between text-white mb-2">
                <span>Subtotal:</span>
                <span>{formatPrice(order.total_amount, order.total_amount * 83)}</span>
              </div>
              <div className="flex justify-between text-white mb-2">
                <span>Processing Fee:</span>
                <span>Free</span>
              </div>
              <div className="border-t border-gray-700 pt-2 mt-4">
                <div className="flex justify-between text-xl font-bold text-white">
                  <span>Total:</span>
                  <span>{formatPrice(order.total_amount, order.total_amount * 83)}</span>
                </div>
              </div>
            </div>

            <div className="mt-6 p-4 bg-blue-900 bg-opacity-30 rounded-lg">
              <div className="flex items-center text-blue-300 text-sm">
                <svg className="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M10 2L3 7v11h4v-6h6v6h4V7l-7-5z"/>
                </svg>
                Secure payment protected by cryptocurrency technology
              </div>
            </div>
          </div>

          {/* Payment Method */}
          <div className="bg-gray-800 rounded-xl p-6">
            <h2 className="text-xl font-semibold text-white mb-6">Payment Method</h2>

            <div className="space-y-4">
              {/* Crypto Payment Option */}
              <div className="border border-gray-700 rounded-lg p-4">
                <label className="flex items-center">
                  <input
                    type="radio"
                    name="paymentMethod"
                    value="crypto"
                    checked={paymentMethod === 'crypto'}
                    onChange={(e) => setPaymentMethod(e.target.value)}
                    className="mr-3"
                  />
                  <div className="flex-1">
                    <div className="text-white font-medium">Cryptocurrency</div>
                    <div className="text-gray-400 text-sm">
                      Pay with Bitcoin, Ethereum, or other cryptocurrencies
                    </div>
                  </div>
                </label>

                {paymentMethod === 'crypto' && (
                  <div className="mt-4 ml-6">
                    <label className="block text-sm font-medium text-gray-300 mb-2">
                      Select Cryptocurrency:
                    </label>
                    <select
                      value={cryptoCurrency}
                      onChange={(e) => setCryptoCurrency(e.target.value)}
                      className="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-2 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="btc">Bitcoin (BTC)</option>
                      <option value="eth">Ethereum (ETH)</option>
                      <option value="ltc">Litecoin (LTC)</option>
                      <option value="doge">Dogecoin (DOGE)</option>
                      <option value="trx">Tron (TRX)</option>
                    </select>
                  </div>
                )}
              </div>
            </div>

            <div className="mt-8">
              <button
                onClick={handlePayment}
                disabled={processing}
                className={`w-full py-4 px-6 rounded-lg font-semibold text-lg transition-all duration-200 ${
                  processing
                    ? 'bg-gray-600 text-gray-400 cursor-not-allowed'
                    : 'bg-blue-600 hover:bg-blue-700 text-white transform hover:scale-105'
                }`}
              >
                {processing ? (
                  <div className="flex items-center justify-center">
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                    Processing Payment...
                  </div>
                ) : (
                  `Pay ${formatPrice(order.total_amount, order.total_amount * 83)}`
                )}
              </button>
            </div>

            <div className="mt-6 text-center">
              <p className="text-gray-400 text-sm mb-2">
                🔒 Your payment is secured with end-to-end encryption
              </p>
              <p className="text-gray-400 text-xs">
                By completing this purchase, you agree to our Terms & Conditions
              </p>
            </div>
          </div>
        </div>

        {/* Security Notice */}
        <div className="mt-8 bg-gray-800 rounded-xl p-6 text-center">
          <h3 className="text-lg font-semibold text-white mb-2">
            🛡️ 100% Secure Payment
          </h3>
          <p className="text-gray-400 text-sm">
            Your payment information is encrypted and secure. We never store your payment details.
            For support, contact us via Telegram or WhatsApp.
          </p>
        </div>
      </div>
    </div>
  );
};

export default CheckoutPage;
EOF

# Create LoginPage.js
cat > LoginPage.js << 'EOF'
import React, { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { Helmet } from 'react-helmet';
import { toast } from 'react-toastify';
import { motion } from 'framer-motion';
import { useAuth } from '../context/AuthContext';
import { EyeIcon, EyeSlashIcon } from '@heroicons/react/24/outline';

const LoginPage = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  
  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const from = location.state?.from || '/';

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const result = await login(formData.email, formData.password);
      
      if (result.success) {
        toast.success('Login successful!');
        navigate(from);
      } else {
        toast.error(result.error || 'Login failed');
      }
    } catch (error) {
      toast.error('An unexpected error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <Helmet>
        <title>Login - Shop VIP Premium</title>
        <meta name="description" content="Login to your Shop VIP Premium account" />
      </Helmet>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-md w-full space-y-8"
      >
        <div className="text-center">
          <h2 className="text-3xl font-bold text-white mb-2">
            Welcome Back
          </h2>
          <p className="text-gray-400">
            Sign in to your Shop VIP Premium account
          </p>
        </div>

        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          <div className="bg-gray-800 rounded-xl p-6 space-y-4">
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-300 mb-2">
                Email Address
              </label>
              <input
                id="email"
                name="email"
                type="email"
                required
                value={formData.email}
                onChange={handleChange}
                className="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-2 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Enter your email"
              />
            </div>

            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-300 mb-2">
                Password
              </label>
              <div className="relative">
                <input
                  id="password"
                  name="password"
                  type={showPassword ? 'text' : 'password'}
                  required
                  value={formData.password}
                  onChange={handleChange}
                  className="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-2 pr-10 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Enter your password"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-white"
                >
                  {showPassword ? (
                    <EyeSlashIcon className="h-5 w-5" />
                  ) : (
                    <EyeIcon className="h-5 w-5" />
                  )}
                </button>
              </div>
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className={`w-full flex justify-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white transition-all duration-200 ${
              loading
                ? 'bg-gray-600 cursor-not-allowed'
                : 'bg-blue-600 hover:bg-blue-700 transform hover:scale-105'
            }`}
          >
            {loading ? (
              <div className="flex items-center">
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                Signing In...
              </div>
            ) : (
              'Sign In'
            )}
          </button>

          <div className="text-center">
            <p className="text-gray-400">
              Don't have an account?{' '}
              <Link
                to="/register"
                className="font-medium text-blue-400 hover:text-blue-300 transition-colors"
              >
                Create one now
              </Link>
            </p>
          </div>
        </form>

        {/* Demo Credentials */}
        <div className="bg-gray-800 rounded-xl p-4 border border-gray-700">
          <h3 className="text-sm font-medium text-yellow-400 mb-2">Demo Access:</h3>
          <div className="text-xs text-gray-400 space-y-1">
            <p>Admin: admin@shopvippremium.com / admin123</p>
          </div>
        </div>

        <div className="text-center">
          <p className="text-gray-500 text-xs">
            By signing in, you agree to our{' '}
            <Link to="/terms" className="text-blue-400 hover:text-blue-300">
              Terms & Conditions
            </Link>{' '}
            and{' '}
            <Link to="/privacy" className="text-blue-400 hover:text-blue-300">
              Privacy Policy
            </Link>
          </p>
        </div>
      </motion.div>
    </div>
  );
};

export default LoginPage;
EOF

# Create RegisterPage.js
cat > RegisterPage.js << 'EOF'
import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Helmet } from 'react-helmet';
import { toast } from 'react-toastify';
import { motion } from 'framer-motion';
import { useAuth } from '../context/AuthContext';
import { EyeIcon, EyeSlashIcon } from '@heroicons/react/24/outline';

const RegisterPage = () => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: ''
  });
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  
  const { register } = useAuth();
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const validateForm = () => {
    if (formData.password !== formData.confirmPassword) {
      toast.error('Passwords do not match');
      return false;
    }

    if (formData.password.length < 6) {
      toast.error('Password must be at least 6 characters long');
      return false;
    }

    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    setLoading(true);

    try {
      const result = await register(formData.username, formData.email, formData.password);
      
      if (result.success) {
        toast.success('Registration successful! Welcome to Shop VIP Premium');
        navigate('/');
      } else {
        toast.error(result.error || 'Registration failed');
      }
    } catch (error) {
      toast.error('An unexpected error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <Helmet>
        <title>Create Account - Shop VIP Premium</title>
        <meta name="description" content="Create your Shop VIP Premium account" />
      </Helmet>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-md w-full space-y-8"
      >
        <div className="text-center">
          <h2 className="text-3xl font-bold text-white mb-2">
            Create Account
          </h2>
          <p className="text-gray-400">
            Join Shop VIP Premium today
          </p>
        </div>

        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          <div className="bg-gray-800 rounded-xl p-6 space-y-4">
            <div>
              <label htmlFor="username" className="block text-sm font-medium text-gray-300 mb-2">
                Username
              </label>
              <input
                id="username"
                name="username"
                type="text"
                required
                value={formData.username}
                onChange={handleChange}
                className="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-2 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Choose a username"
              />
            </div>

            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-300 mb-2">
                Email Address
              </label>
              <input
                id="email"
                name="email"
                type="email"
                required
                value={formData.email}
                onChange={handleChange}
                className="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-2 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Enter your email"
              />
            </div>

            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-300 mb-2">
                Password
              </label>
              <div className="relative">
                <input
                  id="password"
                  name="password"
                  type={showPassword ? 'text' : 'password'}
                  required
                  value={formData.password}
                  onChange={handleChange}
                  className="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-2 pr-10 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="Create a password"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-white"
                >
                  {showPassword ? (
                    <EyeSlashIcon className="h-5 w-5" />
                  ) : (
                    <EyeIcon className="h-5 w-5" />
                  )}
                </button>
              </div>
            </div>

            <div>
              <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-300 mb-2">
                Confirm Password
              </label>
              <input
                id="confirmPassword"
                name="confirmPassword"
                type="password"
                required
                value={formData.confirmPassword}
                onChange={handleChange}
                className="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-2 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="Confirm your password"
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className={`w-full flex justify-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white transition-all duration-200 ${
              loading
                ? 'bg-gray-600 cursor-not-allowed'
                : 'bg-blue-600 hover:bg-blue-700 transform hover:scale-105'
            }`}
          >
            {loading ? (
              <div className="flex items-center">
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                Creating Account...
              </div>
            ) : (
              'Create Account'
            )}
          </button>

          <div className="text-center">
            <p className="text-gray-400">
              Already have an account?{' '}
              <Link
                to="/login"
                className="font-medium text-blue-400 hover:text-blue-300 transition-colors"
              >
                Sign in here
              </Link>
            </p>
          </div>
        </form>

        <div className="text-center">
          <p className="text-gray-500 text-xs">
            By creating an account, you agree to our{' '}
            <Link to="/terms" className="text-blue-400 hover:text-blue-300">
              Terms & Conditions
            </Link>{' '}
            and{' '}
            <Link to="/privacy" className="text-blue-400 hover:text-blue-300">
              Privacy Policy
            </Link>
          </p>
        </div>
      </motion.div>
    </div>
  );
};

export default RegisterPage;
EOF

# Create Order status pages
cat > OrderSuccess.js << 'EOF'
import React, { useEffect, useState } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import { Helmet } from 'react-helmet';
import { motion } from 'framer-motion';
import { CheckCircleIcon } from '@heroicons/react/24/solid';

const OrderSuccess = () => {
  const [searchParams] = useSearchParams();
  const orderId = searchParams.get('order_id');

  return (
    <div className="min-h-screen bg-gray-900 flex items-center justify-center py-12 px-4">
      <Helmet>
        <title>Payment Successful - Shop VIP Premium</title>
        <meta name="description" content="Your payment has been processed successfully" />
      </Helmet>

      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        className="max-w-md w-full text-center"
      >
        <div className="bg-gray-800 rounded-xl p-8">
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ delay: 0.2 }}
          >
            <CheckCircleIcon className="h-20 w-20 text-green-400 mx-auto mb-6" />
          </motion.div>

          <h1 className="text-2xl font-bold text-white mb-4">
            Payment Successful! 🎉
          </h1>
          
          <p className="text-gray-400 mb-6">
            Your order has been processed successfully. You will receive your digital products shortly.
          </p>

          {orderId && (
            <div className="bg-gray-700 rounded-lg p-4 mb-6">
              <p className="text-sm text-gray-300 mb-1">Order ID:</p>
              <p className="font-mono text-white text-sm">{orderId}</p>
            </div>
          )}

          <div className="space-y-4">
            <div className="bg-blue-900 bg-opacity-30 rounded-lg p-4">
              <h3 className="text-blue-300 font-semibold mb-2">What's Next?</h3>
              <ul className="text-sm text-blue-200 space-y-1">
                <li>• Product delivery via email/Telegram</li>
                <li>• Access to customer support</li>
                <li>• Future updates and support</li>
              </ul>
            </div>

            <div className="bg-gray-700 rounded-lg p-4">
              <h3 className="text-white font-semibold mb-2">Need Support?</h3>
              <div className="flex justify-center space-x-4">
                <a
                  href="https://t.me/shopvippremium"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center text-blue-400 hover:text-blue-300 text-sm"
                >
                  📱 Telegram
                </a>
                <a
                  href="https://wa.me/1234567890"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center text-green-400 hover:text-green-300 text-sm"
                >
                  💬 WhatsApp
                </a>
              </div>
            </div>
          </div>

          <div className="mt-8 space-y-3">
            <Link
              to="/products"
              className="block w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors"
            >
              Continue Shopping
            </Link>
            <Link
              to="/"
              className="block w-full bg-gray-700 hover:bg-gray-600 text-white font-semibold py-3 px-6 rounded-lg transition-colors"
            >
              Back to Home
            </Link>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default OrderSuccess;
EOF

cat > OrderFailed.js << 'EOF'
import React from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import { Helmet } from 'react-helmet';
import { motion } from 'framer-motion';
import { XCircleIcon } from '@heroicons/react/24/solid';

const OrderFailed = () => {
  const [searchParams] = useSearchParams();
  const orderId = searchParams.get('order_id');

  return (
    <div className="min-h-screen bg-gray-900 flex items-center justify-center py-12 px-4">
      <Helmet>
        <title>Payment Failed - Shop VIP Premium</title>
        <meta name="description" content="Payment could not be processed" />
      </Helmet>

      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        className="max-w-md w-full text-center"
      >
        <div className="bg-gray-800 rounded-xl p-8">
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ delay: 0.2 }}
          >
            <XCircleIcon className="h-20 w-20 text-red-400 mx-auto mb-6" />
          </motion.div>

          <h1 className="text-2xl font-bold text-white mb-4">
            Payment Failed
          </h1>
          
          <p className="text-gray-400 mb-6">
            We were unable to process your payment. This could be due to insufficient funds,
            network issues, or payment timeout.
          </p>

          {orderId && (
            <div className="bg-gray-700 rounded-lg p-4 mb-6">
              <p className="text-sm text-gray-300 mb-1">Order ID:</p>
              <p className="font-mono text-white text-sm">{orderId}</p>
            </div>
          )}

          <div className="space-y-4">
            <div className="bg-red-900 bg-opacity-30 rounded-lg p-4">
              <h3 className="text-red-300 font-semibold mb-2">Common Issues:</h3>
              <ul className="text-sm text-red-200 space-y-1">
                <li>• Insufficient cryptocurrency balance</li>
                <li>• Payment timeout or network congestion</li>
                <li>• Invalid payment address</li>
              </ul>
            </div>

            <div className="bg-gray-700 rounded-lg p-4">
              <h3 className="text-white font-semibold mb-2">Need Help?</h3>
              <p className="text-gray-400 text-sm mb-3">
                Contact our support team for assistance
              </p>
              <div className="flex justify-center space-x-4">
                <a
                  href="https://t.me/shopvippremium"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center text-blue-400 hover:text-blue-300 text-sm"
                >
                  📱 Telegram
                </a>
                <a
                  href="https://wa.me/1234567890"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center text-green-400 hover:text-green-300 text-sm"
                >
                  💬 WhatsApp
                </a>
              </div>
            </div>
          </div>

          <div className="mt-8 space-y-3">
            <button
              onClick={() => window.history.back()}
              className="block w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors"
            >
              Try Again
            </button>
            <Link
              to="/products"
              className="block w-full bg-gray-700 hover:bg-gray-600 text-white font-semibold py-3 px-6 rounded-lg transition-colors"
            >
              Continue Shopping
            </Link>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default OrderFailed;
EOF

cat > OrderCancelled.js << 'EOF'
import React from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import { Helmet } from 'react-helmet';
import { motion } from 'framer-motion';
import { XCircleIcon } from '@heroicons/react/24/solid';

const OrderCancelled = () => {
  const [searchParams] = useSearchParams();
  const orderId = searchParams.get('order_id');

  return (
    <div className="min-h-screen bg-gray-900 flex items-center justify-center py-12 px-4">
      <Helmet>
        <title>Payment Cancelled - Shop VIP Premium</title>
        <meta name="description" content="Payment has been cancelled" />
      </Helmet>

      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        className="max-w-md w-full text-center"
      >
        <div className="bg-gray-800 rounded-xl p-8">
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ delay: 0.2 }}
          >
            <XCircleIcon className="h-20 w-20 text-yellow-400 mx-auto mb-6" />
          </motion.div>

          <h1 className="text-2xl font-bold text-white mb-4">
            Payment Cancelled
          </h1>
          
          <p className="text-gray-400 mb-6">
            Your payment has been cancelled. No charges have been made to your account.
            You can try again whenever you're ready.
          </p>

          {orderId && (
            <div className="bg-gray-700 rounded-lg p-4 mb-6">
              <p className="text-sm text-gray-300 mb-1">Order ID:</p>
              <p className="font-mono text-white text-sm">{orderId}</p>
            </div>
          )}

          <div className="space-y-4">
            <div className="bg-yellow-900 bg-opacity-30 rounded-lg p-4">
              <h3 className="text-yellow-300 font-semibold mb-2">What Happened?</h3>
              <ul className="text-sm text-yellow-200 space-y-1">
                <li>• Payment was cancelled by user</li>
                <li>• Transaction was not completed</li>
                <li>• No charges were made</li>
              </ul>
            </div>

            <div className="bg-gray-700 rounded-lg p-4">
              <h3 className="text-white font-semibold mb-2">Questions?</h3>
              <p className="text-gray-400 text-sm mb-3">
                Contact us if you need assistance with your purchase
              </p>
              <div className="flex justify-center space-x-4">
                <a
                  href="https://t.me/shopvippremium"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center text-blue-400 hover:text-blue-300 text-sm"
                >
                  📱 Telegram
                </a>
                <a
                  href="https://wa.me/1234567890"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center text-green-400 hover:text-green-300 text-sm"
                >
                  💬 WhatsApp
                </a>
              </div>
            </div>
          </div>

          <div className="mt-8 space-y-3">
            <button
              onClick={() => window.history.back()}
              className="block w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors"
            >
              Try Again
            </button>
            <Link
              to="/products"
              className="block w-full bg-gray-700 hover:bg-gray-600 text-white font-semibold py-3 px-6 rounded-lg transition-colors"
            >
              Continue Shopping
            </Link>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default OrderCancelled;
EOF

echo "✅ Order status pages created successfully!"