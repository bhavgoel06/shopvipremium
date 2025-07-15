import React from 'react';
import { useAuth } from '../context/AuthContext';
import ModernAdminInterface from '../components/ModernAdminInterface';

const AdminDashboard = () => {
  const { isAuthenticated, user } = useAuth();

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen bg-gray-900 text-white flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-2xl font-bold mb-4">Admin Access Required</h1>
          <p className="text-gray-400 mb-6">Please log in to access the admin dashboard</p>
          <a href="/login" className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors">
            Login
          </a>
        </div>
      </div>
    );
  }

  return <ModernAdminInterface />;
};

export default AdminDashboard;