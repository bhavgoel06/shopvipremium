import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import WooCommerceAdminInterface from '../components/WooCommerceAdminInterface';

const AdminDashboard = () => {
  const { isAuthenticated, user } = useAuth();
  const [showAdminInterface, setShowAdminInterface] = useState(false);
  const [adminPassword, setAdminPassword] = useState('');

  const handleAdminAccess = () => {
    // Simple admin access for development
    if (adminPassword === 'admin123' || isAuthenticated) {
      setShowAdminInterface(true);
    } else {
      alert('Invalid admin password');
    }
  };

  if (!isAuthenticated && !showAdminInterface) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-blue-900 to-gray-900 text-white flex items-center justify-center">
        <div className="bg-gray-800 p-8 rounded-2xl shadow-2xl max-w-md w-full mx-4">
          <div className="text-center mb-6">
            <div className="w-16 h-16 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
              </svg>
            </div>
            <h1 className="text-2xl font-bold mb-2">Admin Dashboard</h1>
            <p className="text-gray-400 mb-6">Enter admin password to access dashboard</p>
          </div>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-300 mb-2">
                Admin Password
              </label>
              <input
                type="password"
                value={adminPassword}
                onChange={(e) => setAdminPassword(e.target.value)}
                className="w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-white placeholder-gray-400"
                placeholder="Enter admin password"
                onKeyPress={(e) => e.key === 'Enter' && handleAdminAccess()}
              />
            </div>
            
            <button
              onClick={handleAdminAccess}
              className="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white py-3 rounded-lg hover:from-blue-700 hover:to-purple-700 transition-all duration-300 font-semibold"
            >
              Access Admin Dashboard
            </button>
            
            <div className="text-center text-sm text-gray-400">
              <p>Or <a href="/login" className="text-blue-400 hover:text-blue-300">login with your account</a></p>
            </div>
            
            <div className="mt-6 p-4 bg-gray-700 rounded-lg">
              <p className="text-xs text-gray-400 mb-2">
                <strong>Demo Access:</strong>
              </p>
              <p className="text-xs text-gray-300">
                Password: <code className="bg-gray-600 px-1 rounded">admin123</code>
              </p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return <WooCommerceAdminInterface />;
};

export default AdminDashboard;