import React, { useState, useEffect, useRef } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import ProductCard from '../components/ProductCard';
import { useCurrency } from '../context/CurrencyContext';
import { toast } from 'react-toastify';

const ModernHomePage = () => {
  const [featuredProducts, setFeaturedProducts] = useState([]);
  const [bestsellerProducts, setBestsellerProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [adultProducts, setAdultProducts] = useState([]);
  const [currentSlide, setCurrentSlide] = useState(0);
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });
  const heroRef = useRef(null);
  const { currency, getCurrencySymbol } = useCurrency();
  const navigate = useNavigate();

  // Hero slides data
  const heroSlides = [
    {
      id: 1,
      title: "Premium Subscriptions",
      subtitle: "at Unbeatable Prices",
      description: "Get access to Netflix, Spotify, LinkedIn, and 100+ premium services at up to 90% off",
      image: "https://images.unsplash.com/photo-1611224923853-80b023f02d71?w=1200&h=800&fit=crop",
      gradient: "from-purple-600 via-pink-600 to-blue-600",
      cta: "Explore Deals",
      ctaLink: "/products"
    },
    {
      id: 2,
      title: "AI-Powered Tools",
      subtitle: "for Modern Professionals",
      description: "Perplexity AI, ChatGPT Plus, and cutting-edge AI tools to boost your productivity",
      image: "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=1200&h=800&fit=crop",
      gradient: "from-blue-600 via-cyan-600 to-teal-600",
      cta: "Get AI Tools",
      ctaLink: "/category/software"
    },
    {
      id: 3,
      title: "Entertainment Hub",
      subtitle: "All Your Favorites",
      description: "Netflix, Disney+, Amazon Prime, Spotify, and more - all in one place",
      image: "https://images.unsplash.com/photo-1489599843090-79946b0b2034?w=1200&h=800&fit=crop",
      gradient: "from-red-600 via-orange-600 to-yellow-600",
      cta: "Stream Now",
      ctaLink: "/category/ott"
    }
  ];

  // Stats data
  const stats = [
    { number: "50,000+", label: "Happy Customers", icon: "👥" },
    { number: "100+", label: "Premium Services", icon: "🏆" },
    { number: "90%", label: "Max Savings", icon: "💰" },
    { number: "24/7", label: "Support", icon: "🔧" }
  ];

  // Categories data
  const categories = [
    { 
      name: 'OTT Platforms', 
      slug: 'ott', 
      icon: '📺',
      gradient: 'from-red-500 to-red-700',
      description: 'Netflix, Disney+, Amazon Prime',
      count: '17+ platforms'
    },
    { 
      name: 'Software & Tools', 
      slug: 'software', 
      icon: '💻',
      gradient: 'from-blue-500 to-blue-700',
      description: 'Adobe, Microsoft, Canva',
      count: '10+ tools'
    },
    { 
      name: 'VPN & Security', 
      slug: 'vpn', 
      icon: '🔒',
      gradient: 'from-green-500 to-green-700',
      description: 'NordVPN, ExpressVPN',
      count: '4+ services'
    },
    { 
      name: 'Adult Content', 
      slug: 'adult', 
      icon: '🔞',
      gradient: 'from-pink-500 to-red-700',
      description: 'Premium adult subscriptions',
      count: '11+ sites'
    },
    { 
      name: 'Education', 
      slug: 'education', 
      icon: '📚',
      gradient: 'from-yellow-500 to-orange-700',
      description: 'Coursera, Udemy, LeetCode',
      count: '4+ platforms'
    },
    { 
      name: 'Gaming', 
      slug: 'gaming', 
      icon: '🎮',
      gradient: 'from-purple-500 to-purple-700',
      description: 'Steam, Epic Games',
      count: '2+ stores'
    },
    { 
      name: 'Social Media', 
      slug: 'social_media', 
      icon: '💝',
      gradient: 'from-pink-500 to-purple-700',
      description: 'Tinder, Bumble',
      count: '3+ apps'
    },
    { 
      name: 'Professional', 
      slug: 'professional', 
      icon: '🎓',
      gradient: 'from-indigo-500 to-blue-700',
      description: 'LinkedIn, Business tools',
      count: '2+ services'
    }
  ];

  // Fetch data
  useEffect(() => {
    fetchHomeData();
  }, []);

  // Remove mouse tracking - not needed
  // const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });

  // Remove mouse movement tracking
  // useEffect(() => {
  //   const handleMouseMove = (e) => {
  //     if (window.innerWidth > 768) {
  //       setMousePosition({ x: e.clientX, y: e.clientY });
  //     }
  //   };
  //   window.addEventListener('mousemove', handleMouseMove);
  //   return () => window.removeEventListener('mousemove', handleMouseMove);
  // }, []);

  // Auto-slide effect
  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentSlide((prev) => (prev + 1) % heroSlides.length);
    }, 5000);

    return () => clearInterval(interval);
  }, [heroSlides.length]);

  const fetchHomeData = async () => {
    try {
      setLoading(true);
      const [featuredRes, bestsellerRes, adultRes] = await Promise.all([
        fetch(`${process.env.REACT_APP_BACKEND_URL}/api/products/featured?limit=12`),
        fetch(`${process.env.REACT_APP_BACKEND_URL}/api/products/bestsellers?limit=8`),
        fetch(`${process.env.REACT_APP_BACKEND_URL}/api/products/category/adult?limit=8`)
      ]);

      if (featuredRes.ok) {
        const featuredData = await featuredRes.json();
        if (featuredData.success) setFeaturedProducts(featuredData.data);
      }

      if (bestsellerRes.ok) {
        const bestsellerData = await bestsellerRes.json();
        if (bestsellerData.success) setBestsellerProducts(bestsellerData.data);
      }

      if (adultRes.ok) {
        const adultData = await adultRes.json();
        if (adultData.success) setAdultProducts(adultData.data);
      }
    } catch (error) {
      console.error('Error fetching home data:', error);
      // Don't show error toast for failed requests, just continue with empty data
    } finally {
      setLoading(false);
    }
  };

  const currentSlideData = heroSlides[currentSlide];

  return (
    <div className="min-h-screen bg-black text-white overflow-hidden">
      {/* Remove cursor follower completely */}

      {/* Hero Section */}
      <section className="relative h-screen flex items-center justify-center overflow-hidden">
        {/* Background */}
        <div className="absolute inset-0">
          <AnimatePresence mode="wait">
            <motion.div
              key={currentSlide}
              className={`absolute inset-0 bg-gradient-to-br ${currentSlideData.gradient} opacity-90`}
              initial={{ opacity: 0, scale: 1.1 }}
              animate={{ opacity: 0.9, scale: 1 }}
              exit={{ opacity: 0, scale: 0.9 }}
              transition={{ duration: 1 }}
            />
          </AnimatePresence>
          
          {/* Floating shapes */}
          <div className="absolute inset-0">
            {[...Array(6)].map((_, i) => (
              <motion.div
                key={i}
                className="absolute w-64 h-64 bg-white opacity-5 rounded-full"
                style={{
                  left: `${Math.random() * 100}%`,
                  top: `${Math.random() * 100}%`,
                }}
                animate={{
                  y: [0, -30, 0],
                  x: [0, 20, 0],
                  rotate: [0, 360],
                }}
                transition={{
                  duration: 20 + Math.random() * 10,
                  repeat: Infinity,
                  ease: "linear",
                }}
              />
            ))}
          </div>
        </div>

        {/* Content */}
        <div className="relative z-10 max-w-7xl mx-auto px-4 text-center">
          <AnimatePresence mode="wait">
            <motion.div
              key={currentSlide}
              initial={{ opacity: 0, y: 50 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -50 }}
              transition={{ duration: 0.8 }}
              className="space-y-8"
            >
              <motion.h1
                className="text-6xl md:text-8xl font-bold bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent"
                animate={{ 
                  backgroundPosition: ['0% 50%', '100% 50%', '0% 50%'],
                }}
                transition={{ 
                  duration: 3,
                  repeat: Infinity,
                  ease: "linear"
                }}
              >
                {currentSlideData.title}
              </motion.h1>
              
              <motion.h2
                className="text-4xl md:text-6xl font-light text-gray-200"
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 }}
              >
                {currentSlideData.subtitle}
              </motion.h2>
              
              <motion.p
                className="text-xl md:text-2xl text-gray-300 max-w-3xl mx-auto"
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.4 }}
              >
                {currentSlideData.description}
              </motion.p>
              
              <motion.div
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.6 }}
                className="flex flex-col sm:flex-row gap-6 justify-center items-center"
              >
                <Link
                  to={currentSlideData.ctaLink}
                  className="group relative px-8 py-4 bg-white text-black rounded-full font-semibold text-lg overflow-hidden transition-all duration-300 hover:scale-105"
                >
                  <span className="relative z-10">{currentSlideData.cta}</span>
                  <motion.div
                    className="absolute inset-0 bg-gradient-to-r from-blue-500 to-purple-500"
                    initial={{ scale: 0, opacity: 0 }}
                    whileHover={{ scale: 1, opacity: 1 }}
                    transition={{ duration: 0.3 }}
                  />
                </Link>
                
                <div className="flex items-center gap-4 text-white">
                  <span className="text-lg">Prices in {currency}</span>
                  <div className="flex items-center gap-2">
                    <span className="text-3xl font-bold">{getCurrencySymbol()}5</span>
                    <span className="text-lg text-gray-300">starting from</span>
                  </div>
                </div>
              </motion.div>
            </motion.div>
          </AnimatePresence>
        </div>

        {/* Slide indicators */}
        <div className="absolute bottom-10 left-1/2 transform -translate-x-1/2 flex gap-3">
          {heroSlides.map((_, index) => (
            <button
              key={index}
              onClick={() => setCurrentSlide(index)}
              className={`w-3 h-3 rounded-full transition-all duration-300 ${
                index === currentSlide ? 'bg-white scale-125' : 'bg-white/50'
              }`}
            />
          ))}
        </div>
      </section>

      {/* Stats Section */}
      <section className="relative py-24 bg-gradient-to-b from-black to-gray-900">
        <div className="max-w-7xl mx-auto px-6">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-12">
            {stats.map((stat, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                viewport={{ once: true }}
                className="text-center group"
              >
                <motion.div
                  className="text-5xl mb-6"
                  whileHover={{ scale: 1.2, rotate: 360 }}
                  transition={{ duration: 0.5 }}
                >
                  {stat.icon}
                </motion.div>
                <div className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent mb-3">
                  {stat.number}
                </div>
                <div className="text-gray-400 text-lg">{stat.label}</div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Categories Section */}
      <section className="relative py-24 bg-gray-50">
        <div className="max-w-7xl mx-auto px-6">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-20"
          >
            <h2 className="text-5xl md:text-7xl font-bold bg-gradient-to-r from-gray-900 to-gray-600 bg-clip-text text-transparent mb-6">
              Choose Categories
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Discover premium subscriptions across all major platforms
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {categories.map((category, index) => (
              <motion.div
                key={category.slug}
                initial={{ opacity: 0, y: 50 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                viewport={{ once: true }}
                whileHover={{ scale: 1.05 }}
                className="group cursor-pointer"
              >
                <Link to={`/category/${category.slug}`}>
                  <div className={`relative p-8 rounded-2xl bg-gradient-to-br ${category.gradient} overflow-hidden shadow-lg hover:shadow-xl transition-all duration-300`}>
                    <div className="absolute inset-0 bg-black/20 group-hover:bg-black/10 transition-all duration-300" />
                    <div className="relative z-10 text-center">
                      <div className="text-4xl mb-4">{category.icon}</div>
                      <h3 className="text-xl font-bold text-white mb-2">{category.name}</h3>
                      <p className="text-white/80 text-sm mb-4">{category.description}</p>
                      <div className="flex items-center justify-center">
                        <span className="text-white/90 text-sm">{category.count}</span>
                      </div>
                    </div>
                  </div>
                </Link>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Adult Content Section */}
      <section className="relative py-24 bg-gradient-to-r from-red-900 via-pink-900 to-purple-900">
        <div className="max-w-7xl mx-auto px-6">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-20"
          >
            <h2 className="text-5xl md:text-7xl font-bold bg-gradient-to-r from-white to-gray-200 bg-clip-text text-transparent mb-6">
              Adult Content
            </h2>
            <p className="text-xl text-gray-200 max-w-2xl mx-auto mb-6">
              Premium adult subscriptions with instant access
            </p>
            <div className="bg-yellow-900 bg-opacity-50 rounded-lg p-4 max-w-lg mx-auto">
              <p className="text-yellow-200 text-sm">
                <strong>⚠️ 18+ Only:</strong> Must be 18 or older to access adult content
              </p>
            </div>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8">
            {loading ? (
              Array(8).fill(0).map((_, index) => (
                <div key={index} className="bg-white/10 rounded-2xl p-6 animate-pulse">
                  <div className="h-32 bg-white/20 rounded mb-4" />
                  <div className="h-4 bg-white/20 rounded mb-2" />
                  <div className="h-3 bg-white/20 rounded w-2/3" />
                </div>
              ))
            ) : (
              adultProducts.map((product, index) => (
                <motion.div
                  key={product.id}
                  initial={{ opacity: 0, y: 50 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                  viewport={{ once: true }}
                >
                  <ProductCard product={product} />
                </motion.div>
              ))
            )}
          </div>
        </div>
      </section>

      {/* Featured Products Section */}
      <section className="relative py-24 bg-gradient-to-b from-gray-900 to-black">
        <div className="max-w-7xl mx-auto px-6">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-20"
          >
            <h2 className="text-5xl md:text-7xl font-bold bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent mb-6">
              Featured Deals
            </h2>
            <p className="text-xl text-gray-400 max-w-2xl mx-auto">
              Hand-picked premium subscriptions at unbeatable prices
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-10">
            {loading ? (
              Array(12).fill(0).map((_, index) => (
                <motion.div 
                  key={index} 
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className="bg-white rounded-2xl overflow-hidden shadow-lg animate-pulse"
                >
                  <div className="h-48 bg-gray-200" />
                  <div className="p-6 space-y-3">
                    <div className="h-6 bg-gray-200 rounded" />
                    <div className="h-4 bg-gray-200 rounded w-3/4" />
                    <div className="h-4 bg-gray-200 rounded w-1/2" />
                    <div className="h-10 bg-gray-200 rounded" />
                  </div>
                </motion.div>
              ))
            ) : featuredProducts.length > 0 ? (
              featuredProducts.map((product, index) => (
                <motion.div
                  key={product.id}
                  initial={{ opacity: 0, y: 50 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                  viewport={{ once: true }}
                >
                  <ProductCard product={product} />
                </motion.div>
              ))
            ) : (
              <div className="col-span-full text-center py-16">
                <div className="text-6xl mb-4">🔍</div>
                <h3 className="text-2xl font-bold text-gray-300 mb-2">No Products Found</h3>
                <p className="text-gray-400">Please check back later for featured products.</p>
              </div>
            )}
          </div>

          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mt-12"
          >
            <Link
              to="/products"
              className="inline-flex items-center gap-3 px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-full font-semibold text-lg hover:scale-105 transition-all duration-300"
            >
              View All Products
              <span>→</span>
            </Link>
          </motion.div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="relative py-24 bg-gradient-to-r from-purple-900 via-blue-900 to-purple-900">
        <div className="max-w-5xl mx-auto px-6 text-center">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="space-y-10"
          >
            <h2 className="text-5xl md:text-7xl font-bold bg-gradient-to-r from-white to-gray-200 bg-clip-text text-transparent">
              Ready to Save Big?
            </h2>
            <p className="text-xl text-gray-300 max-w-3xl mx-auto leading-relaxed">
              Join thousands of satisfied customers who are already saving money with our premium subscription deals.
            </p>
            <div className="flex flex-col sm:flex-row gap-8 justify-center">
              <Link
                to="/products"
                className="px-10 py-5 bg-white text-black rounded-full font-semibold text-lg hover:scale-105 transition-all duration-300 shadow-lg"
              >
                Start Shopping Now
              </Link>
              <Link
                to="/contact"
                className="px-10 py-5 border-2 border-white text-white rounded-full font-semibold text-lg hover:bg-white hover:text-black transition-all duration-300"
              >
                Contact Support
              </Link>
            </div>
          </motion.div>
        </div>
      </section>
    </div>
  );
};

export default ModernHomePage;