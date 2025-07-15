import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useCart } from '../context/CartContext';
import { useAuth } from '../context/AuthContext';
import { useCurrency } from '../context/CurrencyContext';
import CartSidebar from './CartSidebar';

const Header = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const [isCartOpen, setIsCartOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const { getCartItemsCount } = useCart();
  const { isAuthenticated, user, logout } = useAuth();
  const { currency, switchCurrency } = useCurrency();
  const navigate = useNavigate();

  const handleSearch = (e) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      navigate(`/products?search=${encodeURIComponent(searchQuery)}`);
      setSearchQuery('');
    }
  };

  const categories = [
    { name: 'OTT Platforms', slug: 'ott', icon: '📺' },
    { name: 'Software & Tools', slug: 'software', icon: '💻' },
    { name: 'VPN & Security', slug: 'vpn', icon: '🔒' },
    { name: 'Professional', slug: 'professional', icon: '🎓' },
    { name: 'Education', slug: 'education', icon: '📚' },
    { name: 'Gaming', slug: 'gaming', icon: '🎮' },
    { name: 'Social Media', slug: 'social_media', icon: '💝' },
    { name: 'Health & Fitness', slug: 'health', icon: '💪' }
  ];

  return (
    <>
      <header className="bg-white shadow-lg border-b-2 border-blue-600 sticky top-0 z-50">
        {/* Top Bar */}
        <div className="bg-blue-600 text-white py-2">
          <div className="container mx-auto px-4">
            <div className="flex justify-between items-center text-sm">
              <div className="flex items-center space-x-4">
                <span>🔥 Up to 70% OFF on Premium Subscriptions!</span>
                <span className="hidden md:inline">📞 24/7 Support Available</span>
              </div>
              <div className="flex items-center space-x-4">
                <span>⚡ Instant Delivery</span>
                <span className="hidden md:inline">🔒 Secure Payments</span>
                
                {/* Contact Buttons */}
                <div className="flex items-center space-x-2">
                  <a 
                    href="https://wa.me/919876543210?text=Hello%20Shop%20For%20Premium%21%20I%20need%20help%20with%20my%20order." 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="bg-green-500 text-white px-2 py-1 rounded-lg hover:bg-green-600 transition-colors text-xs flex items-center gap-1"
                  >
                    <span>💬</span>
                    <span className="hidden lg:inline">WhatsApp</span>
                  </a>
                  <a 
                    href="https://t.me/shopforpremium" 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="bg-blue-500 text-white px-2 py-1 rounded-lg hover:bg-blue-600 transition-colors text-xs flex items-center gap-1"
                  >
                    <span>🚀</span>
                    <span className="hidden lg:inline">Telegram</span>
                  </a>
                </div>
                
                {/* Currency Switcher */}
                <div className="flex items-center space-x-2">
                  <span className="text-sm">Currency:</span>
                  <button
                    onClick={() => switchCurrency(currency === 'USD' ? 'INR' : 'USD')}
                    className="bg-white bg-opacity-20 text-white px-3 py-1 rounded-lg hover:bg-opacity-30 transition-colors text-sm font-medium"
                  >
                    {currency === 'USD' ? '🇺🇸 USD' : '🇮🇳 INR'}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Running Disclaimer */}
        <div className="bg-yellow-500 text-black py-1 overflow-hidden">
          <div className="animate-marquee whitespace-nowrap">
            <span className="text-sm font-medium">
              🎯 Looking for any other software/subscription/product/license key? Contact us on Telegram for instant support: 
              <a 
                href="https://t.me/shopforpremium" 
                target="_blank" 
                rel="noopener noreferrer"
                className="underline hover:text-blue-800 ml-1 font-semibold"
              >
                @shopforpremium
              </a>
              &nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;🔥 Custom orders available • Best prices guaranteed • Instant delivery
            </span>
          </div>
        </div>

        {/* Main Header */}
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            {/* Logo */}
            <Link to="/" className="flex items-center space-x-3">
              <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white p-3 rounded-lg">
                <svg className="w-8 h-8" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-800">Shop For Premium</h1>
                <p className="text-sm text-gray-600">Get More, Pay Less</p>
              </div>
            </Link>

            {/* Search Bar */}
            <div className="hidden md:flex flex-1 max-w-xl mx-8">
              <form onSubmit={handleSearch} className="w-full">
                <div className="relative">
                  <input
                    type="text"
                    placeholder="Search for subscriptions..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="w-full pl-12 pr-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <svg className="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                    </svg>
                  </div>
                </div>
              </form>
            </div>

            {/* Header Actions */}
            <div className="flex items-center space-x-4">
              {/* Cart Button */}
              <button
                onClick={() => setIsCartOpen(true)}
                className="relative p-2 text-gray-700 hover:text-blue-600 transition-colors"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 3h2l.4 2M7 13h10l4-8H5.4m1.6 8L6 5H5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17M17 13v6a2 2 0 01-2 2H9a2 2 0 01-2-2v-6m8 0V9a2 2 0 00-2-2H9a2 2 0 00-2 2v4.01" />
                </svg>
                {getCartItemsCount() > 0 && (
                  <span className="absolute -top-2 -right-2 bg-red-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center">
                    {getCartItemsCount()}
                  </span>
                )}
              </button>

              {/* User Menu */}
              {isAuthenticated ? (
                <div className="relative">
                  <button className="flex items-center space-x-2 text-gray-700 hover:text-blue-600">
                    <div className="w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center">
                      {user?.first_name?.charAt(0) || 'U'}
                    </div>
                    <span className="hidden md:inline">{user?.first_name}</span>
                  </button>
                  {/* Dropdown menu would go here */}
                </div>
              ) : (
                <Link
                  to="/login"
                  className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
                >
                  Login
                </Link>
              )}

              {/* Mobile Menu Button */}
              <button
                onClick={() => setIsMenuOpen(!isMenuOpen)}
                className="md:hidden p-2 text-gray-700 hover:text-blue-600"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  {isMenuOpen ? (
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  ) : (
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                  )}
                </svg>
              </button>
            </div>
          </div>
        </div>

        {/* Navigation */}
        <nav className="bg-gray-50 border-t">
          <div className="container mx-auto px-4">
            <div className="flex items-center justify-between">
              {/* Categories */}
              <div className="hidden lg:flex items-center space-x-6 py-4 overflow-x-auto">
                {categories.map((category) => (
                  <Link
                    key={category.slug}
                    to={`/category/${category.slug}`}
                    className="flex items-center space-x-2 text-gray-700 hover:text-blue-600 transition-colors whitespace-nowrap"
                  >
                    <span>{category.icon}</span>
                    <span className="font-medium text-sm">{category.name}</span>
                  </Link>
                ))}
              </div>

              {/* Additional Links */}
              <div className="hidden md:flex items-center space-x-6 py-4">
                <Link to="/blog" className="text-gray-700 hover:text-blue-600 transition-colors">
                  Blog
                </Link>
                <Link to="/about" className="text-gray-700 hover:text-blue-600 transition-colors">
                  About
                </Link>
                <Link to="/contact" className="text-gray-700 hover:text-blue-600 transition-colors">
                  Contact
                </Link>
              </div>
            </div>
          </div>
        </nav>

        {/* Mobile Menu */}
        {isMenuOpen && (
          <div className="md:hidden bg-white border-t">
            <div className="px-4 py-2 space-y-2">
              {/* Mobile Search */}
              <form onSubmit={handleSearch} className="mb-4">
                <div className="relative">
                  <input
                    type="text"
                    placeholder="Search..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  />
                  <div className="absolute inset-y-0 left-0 pl-3 flex items-center">
                    <svg className="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                    </svg>
                  </div>
                </div>
              </form>

              {/* Mobile Categories */}
              {categories.map((category) => (
                <Link
                  key={category.slug}
                  to={`/category/${category.slug}`}
                  className="flex items-center space-x-3 py-2 text-gray-700 hover:text-blue-600"
                  onClick={() => setIsMenuOpen(false)}
                >
                  <span>{category.icon}</span>
                  <span>{category.name}</span>
                </Link>
              ))}

              {/* Mobile Links */}
              <div className="border-t pt-2 space-y-2">
                <Link to="/blog" className="block py-2 text-gray-700 hover:text-blue-600" onClick={() => setIsMenuOpen(false)}>
                  Blog
                </Link>
                <Link to="/about" className="block py-2 text-gray-700 hover:text-blue-600" onClick={() => setIsMenuOpen(false)}>
                  About
                </Link>
                <Link to="/contact" className="block py-2 text-gray-700 hover:text-blue-600" onClick={() => setIsMenuOpen(false)}>
                  Contact
                </Link>
              </div>
            </div>
          </div>
        )}
      </header>

      {/* Cart Sidebar */}
      <CartSidebar isOpen={isCartOpen} onClose={() => setIsCartOpen(false)} />
    </>
  );
};

export default Header;