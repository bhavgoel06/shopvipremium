import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { EyeIcon, EyeSlashIcon, LockClosedIcon, UserIcon } from '@heroicons/react/24/outline';

const SecureAdminLogin = ({ onLoginSuccess }) => {
  const [credentials, setCredentials] = useState({
    username: '',
    password: ''
  });
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [attempts, setAttempts] = useState(0);
  const [lockoutTime, setLockoutTime] = useState(null);

  const API_URL = process.env.REACT_APP_BACKEND_URL;

  useEffect(() => {
    // Check if already logged in
    const token = localStorage.getItem('vip_admin_token');
    if (token) {
      verifyExistingToken(token);
    }

    // Handle lockout timer
    if (lockoutTime) {
      const timer = setInterval(() => {
        if (Date.now() > lockoutTime) {
          setLockoutTime(null);
          setAttempts(0);
        }
      }, 1000);
      return () => clearInterval(timer);
    }
  }, [lockoutTime]);

  const verifyExistingToken = async (token) => {
    try {
      const response = await fetch(`${API_URL}/api/admin/verify`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        onLoginSuccess(token);
      } else {
        localStorage.removeItem('vip_admin_token');
      }
    } catch (error) {
      localStorage.removeItem('vip_admin_token');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    // Check lockout
    if (lockoutTime && Date.now() < lockoutTime) {
      const remainingTime = Math.ceil((lockoutTime - Date.now()) / 1000);
      setError(`Too many failed attempts. Try again in ${remainingTime} seconds.`);
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await fetch(`${API_URL}/api/admin/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(credentials)
      });

      const data = await response.json();

      if (response.ok && data.success) {
        // Store token securely
        localStorage.setItem('vip_admin_token', data.token);
        localStorage.setItem('vip_admin_expires', Date.now() + (data.expires_in * 1000));
        
        // Reset attempts
        setAttempts(0);
        setLockoutTime(null);
        
        // Success callback
        onLoginSuccess(data.token);
        
        // Show success message
        setError('');
      } else {
        // Handle failed login
        const newAttempts = attempts + 1;
        setAttempts(newAttempts);
        
        if (newAttempts >= 5) {
          // Lockout for 5 minutes after 5 attempts
          setLockoutTime(Date.now() + (5 * 60 * 1000));
          setError('Too many failed attempts. Account locked for 5 minutes.');
        } else {
          setError(`Invalid credentials. ${5 - newAttempts} attempts remaining.`);
        }
      }
    } catch (error) {
      setError('Connection error. Please check your internet connection.');
    } finally {
      setLoading(false);
    }
  };

  const isLocked = lockoutTime && Date.now() < lockoutTime;
  const remainingLockTime = isLocked ? Math.ceil((lockoutTime - Date.now()) / 1000) : 0;

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-blue-900 flex items-center justify-center p-4">
      <div className="absolute inset-0 bg-black opacity-20"></div>
      <div className="absolute inset-0">
        <div className="absolute top-20 left-10 w-72 h-72 bg-purple-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse"></div>
        <div className="absolute top-40 right-10 w-96 h-96 bg-blue-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse animation-delay-2000"></div>
      </div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        className="relative z-10 w-full max-w-md"
      >
        <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 border border-white/20 shadow-2xl">
          {/* Header */}
          <div className="text-center mb-8">
            <div className="mx-auto w-16 h-16 bg-gradient-to-r from-purple-500 to-blue-500 rounded-full flex items-center justify-center mb-4">
              <LockClosedIcon className="w-8 h-8 text-white" />
            </div>
            <h1 className="text-2xl font-bold text-white mb-2">VIP Admin Access</h1>
            <p className="text-gray-300">Secure login to Shop VIP Premium dashboard</p>
          </div>

          {/* Security Notice */}
          <div className="bg-yellow-500/10 border border-yellow-500/20 rounded-lg p-3 mb-6">
            <p className="text-yellow-300 text-xs text-center">
              🔐 This is a secure admin area. All login attempts are monitored and logged.
            </p>
          </div>

          {/* Login Form */}
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Username Field */}
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Admin Username
              </label>
              <div className="relative">
                <UserIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                <input
                  type="text"
                  value={credentials.username}
                  onChange={(e) => setCredentials({...credentials, username: e.target.value})}
                  className="w-full pl-10 pr-4 py-3 bg-white/5 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:ring-2 focus:ring-purple-500 focus:border-transparent backdrop-blur-sm"
                  placeholder="Enter admin username"
                  required
                  disabled={loading || isLocked}
                />
              </div>
            </div>

            {/* Password Field */}
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Admin Password
              </label>
              <div className="relative">
                <LockClosedIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
                <input
                  type={showPassword ? 'text' : 'password'}
                  value={credentials.password}
                  onChange={(e) => setCredentials({...credentials, password: e.target.value})}
                  className="w-full pl-10 pr-12 py-3 bg-white/5 border border-white/20 rounded-lg text-white placeholder-gray-400 focus:ring-2 focus:ring-purple-500 focus:border-transparent backdrop-blur-sm"
                  placeholder="Enter secure password"
                  required
                  disabled={loading || isLocked}
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-white transition-colors"
                  disabled={loading || isLocked}
                >
                  {showPassword ? <EyeSlashIcon className="w-5 h-5" /> : <EyeIcon className="w-5 h-5" />}
                </button>
              </div>
            </div>

            {/* Error Message */}
            {error && (
              <motion.div
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                className="bg-red-500/10 border border-red-500/20 rounded-lg p-3"
              >
                <p className="text-red-300 text-sm text-center">{error}</p>
              </motion.div>
            )}

            {/* Lockout Timer */}
            {isLocked && (
              <div className="bg-orange-500/10 border border-orange-500/20 rounded-lg p-3">
                <p className="text-orange-300 text-sm text-center">
                  🔒 Account locked. Retry in {Math.floor(remainingLockTime / 60)}:{(remainingLockTime % 60).toString().padStart(2, '0')}
                </p>
              </div>
            )}

            {/* Login Button */}
            <button
              type="submit"
              disabled={loading || isLocked || !credentials.username || !credentials.password}
              className="w-full bg-gradient-to-r from-purple-500 to-blue-500 text-white py-3 px-6 rounded-lg font-semibold hover:from-purple-600 hover:to-blue-600 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300 transform hover:scale-105 shadow-lg"
            >
              {loading ? (
                <div className="flex items-center justify-center">
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                  Authenticating...
                </div>
              ) : isLocked ? (
                'Account Locked'
              ) : (
                '🔓 Access VIP Dashboard'
              )}
            </button>
          </form>

          {/* Security Info */}
          <div className="mt-6 pt-6 border-t border-white/10">
            <p className="text-xs text-gray-400 text-center">
              Protected by end-to-end encryption • Session expires in 8 hours
            </p>
            <div className="flex items-center justify-center mt-2 space-x-4 text-xs text-gray-500">
              <span>Attempts: {attempts}/5</span>
              <span>•</span>
              <span>IP Monitored</span>
              <span>•</span>
              <span>Secure Login</span>
            </div>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default SecureAdminLogin;