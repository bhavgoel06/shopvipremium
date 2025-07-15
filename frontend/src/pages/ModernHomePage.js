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
      name: "OTT Platforms",
      slug: "ott",
      icon: "🎬",
      description: "Netflix, Disney+, Amazon Prime",
      gradient: "from-red-500 to-pink-500",
      count: "25+ Services"
    },
    {
      name: "AI & Software",
      slug: "software",
      icon: "🤖",
      description: "ChatGPT, Perplexity, Dev Tools",
      gradient: "from-blue-500 to-cyan-500",
      count: "30+ Tools"
    },
    {
      name: "Professional",
      slug: "professional",
      icon: "💼",
      description: "LinkedIn, Career Tools",
      gradient: "from-purple-500 to-indigo-500",
      count: "15+ Services"
    },
    {
      name: "Music & Audio",
      slug: "music",
      icon: "🎵",
      description: "Spotify, Apple Music, YouTube",
      gradient: "from-green-500 to-teal-500",
      count: "10+ Platforms"
    },
    {
      name: "Education",
      slug: "education",
      icon: "📚",
      description: "Courses, Certifications",
      gradient: "from-orange-500 to-red-500",
      count: "20+ Courses"
    },
    {
      name: "Social & Dating",
      slug: "social",
      icon: "💝",
      description: "Tinder, Premium Features",
      gradient: "from-pink-500 to-rose-500",
      count: "8+ Apps"
    }
  ];

  // Fetch data
  useEffect(() => {
    fetchHomeData();
  }, []);

  // Mouse movement tracking
  useEffect(() => {
    const handleMouseMove = (e) => {
      setMousePosition({ x: e.clientX, y: e.clientY });
    };

    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, []);

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
      const [featuredRes, bestsellerRes] = await Promise.all([
        fetch(`${process.env.REACT_APP_BACKEND_URL}/api/products/featured?limit=12`),
        fetch(`${process.env.REACT_APP_BACKEND_URL}/api/products/bestsellers?limit=8`)
      ]);

      if (featuredRes.ok) {
        const featuredData = await featuredRes.json();
        if (featuredData.success) setFeaturedProducts(featuredData.data);
      }

      if (bestsellerRes.ok) {
        const bestsellerData = await bestsellerRes.json();
        if (bestsellerData.success) setBestsellerProducts(bestsellerData.data);
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
      {/* Cursor follower */}
      <motion.div
        className="fixed w-6 h-6 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full pointer-events-none z-50 mix-blend-difference"
        animate={{
          x: mousePosition.x - 12,
          y: mousePosition.y - 12,
        }}
        transition={{
          type: "spring",
          stiffness: 500,
          damping: 28,
        }}
      />

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
                    <span className="text-3xl font-bold">{getCurrencySymbol()}99</span>
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
      <section className="relative py-20 bg-gradient-to-b from-black to-gray-900">
        <div className="max-w-7xl mx-auto px-4">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
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
                  className="text-4xl mb-4"
                  whileHover={{ scale: 1.2, rotate: 360 }}
                  transition={{ duration: 0.5 }}
                >
                  {stat.icon}
                </motion.div>
                <div className="text-3xl md:text-4xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent mb-2">
                  {stat.number}
                </div>
                <div className="text-gray-400">{stat.label}</div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Categories Section */}
      <section className="relative py-20 bg-gray-900">
        <div className="max-w-7xl mx-auto px-4">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-6xl font-bold bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent mb-4">
              Explore Categories
            </h2>
            <p className="text-xl text-gray-400">
              Discover premium subscriptions across all major platforms
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
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
                  <div className={`relative p-8 rounded-3xl bg-gradient-to-br ${category.gradient} overflow-hidden`}>
                    <div className="absolute inset-0 bg-black/20 group-hover:bg-black/10 transition-all duration-300" />
                    <div className="relative z-10">
                      <div className="text-4xl mb-4">{category.icon}</div>
                      <h3 className="text-2xl font-bold text-white mb-2">{category.name}</h3>
                      <p className="text-white/80 mb-4">{category.description}</p>
                      <div className="flex items-center justify-between">
                        <span className="text-white/60">{category.count}</span>
                        <motion.div
                          className="w-8 h-8 bg-white/20 rounded-full flex items-center justify-center"
                          whileHover={{ scale: 1.1 }}
                        >
                          <span className="text-white">→</span>
                        </motion.div>
                      </div>
                    </div>
                  </div>
                </Link>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Featured Products Section */}
      <section className="relative py-20 bg-gradient-to-b from-gray-900 to-black">
        <div className="max-w-7xl mx-auto px-4">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl md:text-6xl font-bold bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent mb-4">
              Featured Deals
            </h2>
            <p className="text-xl text-gray-400">
              Hand-picked premium subscriptions at unbeatable prices
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8">
            {loading ? (
              Array(12).fill(0).map((_, index) => (
                <motion.div 
                  key={index} 
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className="bg-gray-800 rounded-3xl overflow-hidden"
                >
                  <div className="aspect-w-16 aspect-h-9 bg-gray-700 animate-pulse">
                    <div className="h-48 bg-gradient-to-r from-gray-700 to-gray-600 rounded-t-3xl" />
                  </div>
                  <div className="p-6 space-y-3">
                    <div className="h-6 bg-gray-700 rounded animate-pulse" />
                    <div className="h-4 bg-gray-700 rounded w-3/4 animate-pulse" />
                    <div className="h-4 bg-gray-700 rounded w-1/2 animate-pulse" />
                    <div className="h-10 bg-gray-700 rounded animate-pulse" />
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
                  <ProductCard product={product} className="bg-gray-800 border-gray-700 hover:border-gray-600 transition-all duration-300" />
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
      <section className="relative py-20 bg-gradient-to-r from-purple-900 via-blue-900 to-purple-900">
        <div className="max-w-4xl mx-auto px-4 text-center">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="space-y-8"
          >
            <h2 className="text-4xl md:text-6xl font-bold bg-gradient-to-r from-white to-gray-200 bg-clip-text text-transparent">
              Ready to Save Big?
            </h2>
            <p className="text-xl text-gray-300 max-w-2xl mx-auto">
              Join thousands of satisfied customers who are already saving money with our premium subscription deals.
            </p>
            <div className="flex flex-col sm:flex-row gap-6 justify-center">
              <Link
                to="/products"
                className="px-8 py-4 bg-white text-black rounded-full font-semibold text-lg hover:scale-105 transition-all duration-300"
              >
                Start Shopping Now
              </Link>
              <Link
                to="/contact"
                className="px-8 py-4 border-2 border-white text-white rounded-full font-semibold text-lg hover:bg-white hover:text-black transition-all duration-300"
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