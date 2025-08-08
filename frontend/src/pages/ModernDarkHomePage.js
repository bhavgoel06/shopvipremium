import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { useCurrency } from '../context/CurrencyContext';
import '../styles/ai-tech-theme.css';
import { 
  PlayIcon, 
  MusicalNoteIcon, 
  ShieldCheckIcon, 
  SparklesIcon,
  ClockIcon,
  StarIcon,
  CheckCircleIcon,
  FireIcon,
  TagIcon,
  BoltIcon,
  HeartIcon,
  RocketLaunchIcon
} from '@heroicons/react/24/solid';

const ModernDarkHomePage = () => {
  const { formatPrice, currency } = useCurrency();
  const [timeLeft, setTimeLeft] = useState(3600); // 1 hour countdown
  const [featuredProducts, setFeaturedProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [priceKey, setPriceKey] = useState(0);

  // Force re-render when currency changes
  useEffect(() => {
    setPriceKey(prev => prev + 1);
  }, [currency]);

  useEffect(() => {
    fetchFeaturedProducts();
    const timer = setInterval(() => {
      setTimeLeft((prev) => prev > 0 ? prev - 1 : 3600);
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  const fetchFeaturedProducts = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/products/featured`);
      const data = await response.json();
      if (data.success) {
        setFeaturedProducts(data.data);
      }
    } catch (error) {
      console.error('Error fetching featured products:', error);
    } finally {
      setLoading(false);
    }
  };

  const formatTime = (seconds) => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-purple-900 to-violet-900 relative overflow-hidden text-white">
      {/* AI Neural Background */}
      <div className="ai-neural-bg"></div>
      {/* Header */}
      <header className="bg-gray-800 border-b border-gray-700 sticky top-0 z-50">
        <nav className="container mx-auto px-4 py-4">
          <div className="flex justify-between items-center">
            <Link to="/" className="text-2xl font-bold bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent">
              Shop VIP Premium
            </Link>
            <ul className="flex space-x-8">
              <li><Link to="/" className="text-gray-300 hover:text-purple-400 font-semibold transition-colors">Home</Link></li>
              <li><Link to="/products" className="text-gray-300 hover:text-purple-400 font-semibold transition-colors">Products</Link></li>
              <li><Link to="/contact" className="text-gray-300 hover:text-purple-400 font-semibold transition-colors">Contact</Link></li>
            </ul>
          </div>
        </nav>
      </header>

      {/* Hero Section with AI/Tech Styling */}
      <section className="relative py-20 px-4 text-center">
        <div className="relative z-10 max-w-4xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <div className="inline-flex items-center bg-red-500 text-white px-4 py-2 rounded-full mb-6 animate-pulse">
              <FireIcon className="w-5 h-5 mr-2" />
              <span className="font-semibold">VIP DEALS - UP TO 70% OFF!</span>
            </div>
            
            <h1 className="text-5xl md:text-7xl font-bold mb-6 leading-tight">
              <span className="ai-text-glow">Shop VIP Premium</span>
            </h1>
            
            <p className="text-xl md:text-2xl mb-8 text-gray-300 leading-relaxed max-w-3xl mx-auto">
              🚀 Next-Gen Digital Workspace Solutions | AI-Powered Premium Tools | 
              <span className="text-cyan-400 font-semibold"> 90+ Professional Utilities</span>
            </p>

            <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-8">
              <Link 
                to="/products"
                className="ai-neon-button text-lg px-8 py-4 flex items-center gap-3"
              >
                <RocketLaunchIcon className="w-6 h-6" />
                Explore Premium Tools
              </Link>
              <Link 
                to="/about"
                className="ai-glass-card px-8 py-4 text-white font-semibold hover:text-cyan-300 transition-colors flex items-center gap-3"
              >
                <PlayIcon className="w-5 h-5" />
                Watch Demo
              </Link>
            </div>
            
            {/* Trust Indicators */}
            <div className="flex flex-wrap justify-center items-center gap-8 text-sm opacity-90">
              <div className="flex items-center">
                <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                <span className="ml-2">99.9% Uptime</span>
              </div>
              <div className="flex items-center">
                <div className="w-2 h-2 bg-blue-400 rounded-full animate-pulse"></div>
                <span className="ml-2">24/7 AI Support</span>
              </div>
              <div className="flex items-center">
                <div className="w-2 h-2 bg-purple-400 rounded-full animate-pulse"></div>
                <span className="ml-2">Instant Delivery</span>
              </div>
              <div className="flex items-center">
                <div className="w-2 h-2 bg-cyan-400 rounded-full animate-pulse"></div>
                <span className="ml-2">Crypto Ready</span>
              </div>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Featured Products */}
      <section className="py-20 px-4">
        <div className="container mx-auto">
          <div className="text-center mb-16">
            <div className="inline-flex items-center bg-red-100 text-red-800 px-4 py-2 rounded-full mb-4">
              <TagIcon className="w-5 h-5 mr-2" />
              <span className="font-semibold">VIP COLLECTION</span>
            </div>
            <h2 className="text-4xl font-bold mb-6">Our VIP Premium Products</h2>
            <p className="text-xl text-gray-400">Hand-picked subscriptions with the biggest savings</p>
          </div>

          {loading ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
              {[...Array(8)].map((_, i) => (
                <div key={i} className="bg-gray-800 h-80 rounded-2xl animate-pulse"></div>
              ))}
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
              {featuredProducts.slice(0, 8).map((product) => (
                <motion.div
                  key={product.id}
                  initial={{ opacity: 0, scale: 0.9 }}
                  whileInView={{ opacity: 1, scale: 1 }}
                  whileHover={{ y: -10 }}
                  className="bg-gray-800 rounded-2xl p-6 border border-gray-700 hover:border-purple-500 transition-all duration-300 group relative overflow-hidden"
                >
                  {product.discount_percentage > 50 && (
                    <div className="absolute top-0 right-0 bg-red-500 text-white px-3 py-1 font-bold text-sm rounded-bl-lg">
                      -{product.discount_percentage}%
                    </div>
                  )}
                  
                  <div className="text-center">
                    <img 
                      src={product.image_url} 
                      alt={product.name}
                      className="w-20 h-20 object-contain mx-auto mb-4 rounded-lg"
                    />

                    <h3 className="text-xl font-bold mb-2 text-white group-hover:text-purple-400 transition-colors">
                      {product.name}
                    </h3>
                    
                    <div className="flex items-center justify-center mb-3">
                      {[...Array(5)].map((_, i) => (
                        <StarIcon 
                          key={i} 
                          className={`w-4 h-4 ${i < Math.floor(product.average_rating || 4.5) ? 'text-yellow-400' : 'text-gray-600'}`}
                        />
                      ))}
                      <span className="text-sm text-gray-400 ml-2">({product.review_count || '100+'})</span>
                    </div>

                    <div className="mb-4" key={priceKey}>
                      <div className="flex items-center justify-center space-x-2">
                        <span className="text-2xl font-bold text-purple-400">{formatPrice(product.discounted_price)}</span>
                        <span className="text-lg text-gray-500 line-through">{formatPrice(product.original_price)}</span>
                      </div>
                      <p className="text-sm text-gray-400 mt-1">{product.short_description}</p>
                    </div>

                    <Link
                      to={`/products/${product.id}`}
                      className="w-full bg-gradient-to-r from-purple-500 to-blue-600 hover:from-purple-600 hover:to-blue-700 text-white py-3 px-6 rounded-full font-semibold transition-all duration-300 transform group-hover:scale-105 inline-block"
                    >
                      Buy Now
                    </Link>
                  </div>
                </motion.div>
              ))}
            </div>
          )}

          <div className="text-center mt-12">
            <Link
              to="/products"
              className="inline-flex items-center bg-gray-800 border border-purple-500 text-purple-400 px-8 py-4 rounded-full font-bold text-lg hover:bg-purple-500 hover:text-white transition-colors"
            >
              View All Products
              <svg className="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            </Link>
          </div>
        </div>
      </section>

      {/* Why Choose Us */}
      <section className="bg-gray-800 py-20 px-4">
        <div className="container mx-auto text-center">
          <h2 className="text-4xl font-bold mb-16">Why Choose Shop VIP Premium?</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              className="p-8"
            >
              <BoltIcon className="w-16 h-16 text-purple-400 mx-auto mb-4" />
              <h3 className="text-2xl font-bold mb-4">Immediate Access</h3>
              <p className="text-gray-400">Get access to your digital toolkit resources immediately after account setup.</p>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
              className="p-8"
            >
              <ShieldCheckIcon className="w-16 h-16 text-purple-400 mx-auto mb-4" />
              <h3 className="text-2xl font-bold mb-4">Full Warranty</h3>
              <p className="text-gray-400">We provide a full warranty for the entire duration of your plan.</p>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="p-8"
            >
              <HeartIcon className="w-16 h-16 text-purple-400 mx-auto mb-4" />
              <h3 className="text-2xl font-bold mb-4">24/7 Support</h3>
              <p className="text-gray-400">Our support team is always here to help you with any issues.</p>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Trust Section */}
      <section className="py-20 px-4">
        <div className="container mx-auto text-center">
          <h2 className="text-3xl font-bold mb-12">Trusted by 8,500+ Customers Worldwide</h2>
          
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8 mb-16">
            {[
              { label: 'Happy Customers', value: '8,500+', icon: '😊' },
              { label: 'Orders Delivered', value: '12,000+', icon: '📦' },
              { label: 'Countries Served', value: '25+', icon: '🌍' },
              { label: 'Success Rate', value: '99.8%', icon: '🎯' }
            ].map((stat, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className="bg-gray-800 p-6 rounded-2xl border border-gray-700"
              >
                <div className="text-4xl mb-2">{stat.icon}</div>
                <div className="text-3xl font-bold text-purple-400 mb-2">{stat.value}</div>
                <div className="text-sm text-gray-400">{stat.label}</div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 bg-gradient-to-r from-purple-600 to-blue-600">
        <div className="container mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
          >
            <h2 className="text-4xl md:text-5xl font-bold mb-6">
              Ready to Enhance Your Digital Workspace?
            </h2>
            <p className="text-xl mb-8 max-w-3xl mx-auto">
              Join over 8,500+ customers who trust us for their premium account needs. 
              Immediate Access, 24/7 support, and professional resources guaranteed.
            </p>
            
            <Link
              to="/products"
              className="inline-flex items-center bg-white text-purple-600 px-10 py-4 rounded-full font-bold text-xl hover:bg-gray-100 transition-colors shadow-xl"
            >
              🛍️ Start Shopping Now
              <svg className="w-6 h-6 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </Link>
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 border-t border-gray-700 text-center py-8 px-4">
        <p className="text-gray-400">&copy; 2025 Shop VIP Premium. All Rights Reserved.</p>
      </footer>
    </div>
  );
};

export default ModernDarkHomePage;