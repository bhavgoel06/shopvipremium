import React, { useState, useEffect, useRef } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import ProductCard from '../components/ProductCard';
import { Helmet } from 'react-helmet';
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
    <>
      <Helmet>
        <title>Shop For Premium - Access Premium Services at 70% Less Cost | Group Subscriptions</title>
        <meta name="description" content="Get Netflix, Disney+, Spotify, Adobe & more premium subscriptions at fraction of original price. Trusted by 10,000+ users. Instant delivery, 30-day warranty." />
        <meta name="keywords" content="premium subscriptions, group subscriptions, cheap netflix, discount spotify, adobe creative cloud, group plans, shared subscriptions" />
        
        {/* Open Graph Tags */}
        <meta property="og:title" content="Shop For Premium - Group Subscriptions at 70% Discount" />
        <meta property="og:description" content="Access premium services like Netflix, Spotify, Adobe at fraction of cost. Secure, legal, instant delivery." />
        <meta property="og:image" content="/logo-social.png" />
        <meta property="og:url" content="https://shopforpremium.com" />
        <meta property="og:type" content="website" />
        
        {/* Twitter Card Tags */}
        <meta name="twitter:card" content="summary_large_image" />
        <meta name="twitter:title" content="Shop For Premium - Premium Subscriptions 70% Off" />
        <meta name="twitter:description" content="Get Netflix, Spotify, Adobe & more at incredible discounts. Secure group subscriptions." />
        <meta name="twitter:image" content="/logo-social.png" />
        
        {/* Additional Meta Tags */}
        <meta name="author" content="Shop For Premium" />
        <meta name="robots" content="index, follow" />
        <link rel="canonical" href="https://shopforpremium.com" />
      </Helmet>

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
                Access Premium Services at a Fraction of the Price – Group Subscriptions for Everyone
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
                className="flex flex-col sm:flex-row items-center justify-center gap-6 mb-8"
              >
                <Link
                  to="/products"
                  className="px-10 py-4 bg-white text-gray-900 rounded-full font-semibold text-lg hover:scale-105 transition-all duration-300 shadow-lg flex items-center gap-2"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                  Start Your Subscription
                </Link>
                <Link
                  to="/products"
                  className="px-10 py-4 border-2 border-white text-white rounded-full font-semibold text-lg hover:bg-white hover:text-gray-900 transition-all duration-300 flex items-center gap-2"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                  </svg>
                  Browse Available Subscriptions
                </Link>
              </motion.div>

              {/* Social Proof */}
              <div className="flex flex-col items-center gap-4">
                <div className="flex items-center gap-6 text-sm text-gray-200">
                  <div className="flex items-center gap-2">
                    <svg className="w-4 h-4 text-green-400" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd"/>
                    </svg>
                    <span>Trusted by 10,000+ users</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <svg className="w-4 h-4 text-blue-400" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clipRule="evenodd"/>
                    </svg>
                    <span>Secured with SSL</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <svg className="w-4 h-4 text-yellow-400" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z"/>
                    </svg>
                    <span>4.8/5 Rating</span>
                  </div>
                </div>
                <div className="text-center">
                  <span className="text-lg text-gray-200">Prices in {currency}</span>
                  <div className="text-4xl font-bold text-white">{getCurrencySymbol()}5</div>
                  <span className="text-sm text-gray-300">starting from</span>
                </div>
              </div>
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

      {/* Testimonials Section */}
      <section className="relative py-24 bg-gray-900">
        <div className="max-w-7xl mx-auto px-6">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-20"
          >
            <h2 className="text-5xl md:text-7xl font-bold bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent mb-6">
              What Our Users Say
            </h2>
            <p className="text-xl text-gray-400 max-w-2xl mx-auto">
              Join thousands of satisfied customers saving money on premium subscriptions
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              {
                name: "Sarah Johnson",
                role: "Digital Marketing Manager",
                content: "I've saved over $300 this year using Shop For Premium! The group subscriptions work perfectly and the service is incredibly reliable.",
                rating: 5,
                avatar: "💼",
                date: "2 days ago"
              },
              {
                name: "Michael Chen",
                role: "Software Developer",
                content: "Finally found a trustworthy platform for premium subscriptions. The Netflix and Spotify accounts work flawlessly. Highly recommended!",
                rating: 5,
                avatar: "👨‍💻",
                date: "1 week ago"
              },
              {
                name: "Emma Rodriguez",
                role: "Content Creator",
                content: "Game changer! I get access to all the creative tools I need at 70% less cost. The support team is amazing and delivery is instant.",
                rating: 5,
                avatar: "🎨",
                date: "3 days ago"
              }
            ].map((testimonial, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 50 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                viewport={{ once: true }}
                className="bg-gray-800 rounded-2xl p-8 shadow-xl"
              >
                <div className="flex items-center mb-4">
                  {[...Array(testimonial.rating)].map((_, i) => (
                    <span key={i} className="text-yellow-400 text-lg">★</span>
                  ))}
                </div>
                <p className="text-gray-300 mb-6 text-lg leading-relaxed">
                  "{testimonial.content}"
                </p>
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div className="w-12 h-12 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center text-xl">
                      {testimonial.avatar}
                    </div>
                    <div>
                      <p className="font-semibold text-white">{testimonial.name}</p>
                      <p className="text-gray-400 text-sm">{testimonial.role}</p>
                    </div>
                  </div>
                  <div className="text-gray-500 text-sm">{testimonial.date}</div>
                </div>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Trust & Safety Section */}
      <section className="relative py-24 bg-gradient-to-br from-blue-900 to-purple-900">
        <div className="max-w-7xl mx-auto px-6">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-20"
          >
            <h2 className="text-5xl md:text-7xl font-bold bg-gradient-to-r from-white to-gray-200 bg-clip-text text-transparent mb-6">
              Trust & Safety
            </h2>
            <p className="text-xl text-gray-200 max-w-2xl mx-auto">
              Your security and satisfaction are our top priorities
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {[
              {
                icon: "🔒",
                title: "Secure Transactions",
                description: "All payments are encrypted and processed through secure gateways. Your financial information is never stored."
              },
              {
                icon: "🛡️",
                title: "No Password Sharing",
                description: "We never share your personal passwords. Each subscription is managed through secure, dedicated channels."
              },
              {
                icon: "💰",
                title: "Money Back Guarantee",
                description: "30-day full refund policy. If you're not satisfied, we'll refund your money, no questions asked."
              },
              {
                icon: "🚀",
                title: "Instant Delivery",
                description: "Get your subscriptions activated within minutes. Our automated system ensures immediate access to your services."
              }
            ].map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 50 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                viewport={{ once: true }}
                className="bg-white/10 backdrop-blur-sm rounded-2xl p-6 text-center hover:bg-white/20 transition-all duration-300"
              >
                <div className="text-4xl mb-4">{feature.icon}</div>
                <h3 className="text-xl font-bold text-white mb-3">{feature.title}</h3>
                <p className="text-gray-200 text-sm leading-relaxed">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* FAQ Section */}
      <section className="relative py-24 bg-gray-50">
        <div className="max-w-4xl mx-auto px-6">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-20"
          >
            <h2 className="text-5xl md:text-6xl font-bold bg-gradient-to-r from-gray-900 to-gray-600 bg-clip-text text-transparent mb-6">
              Frequently Asked Questions
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Everything you need to know about our service
            </p>
          </motion.div>

          <div className="space-y-6">
            {[
              {
                question: "How do group subscriptions work?",
                answer: "We purchase family or group plans from official providers and share access with multiple users. Each user gets their own profile/account within the subscription, ensuring privacy and security."
              },
              {
                question: "Are the subscriptions legal and safe?",
                answer: "Yes, absolutely! We purchase legitimate family and group plans directly from official providers. All subscriptions are legal and comply with the terms of service of respective platforms."
              },
              {
                question: "What if my subscription stops working?",
                answer: "We provide 30-day warranty on all subscriptions. If your subscription stops working, we'll immediately provide a replacement or issue a full refund. Our support team is available 24/7."
              },
              {
                question: "How quickly will I receive my subscription?",
                answer: "Most subscriptions are delivered instantly after payment. In some cases, it may take up to 30 minutes. You'll receive all login details via WhatsApp or email."
              },
              {
                question: "Can I change or cancel my subscription?",
                answer: "Yes, you can request changes or cancellations within the first 30 days. We offer flexible terms and will work with you to find the best solution."
              },
              {
                question: "Do you offer refunds?",
                answer: "Yes, we offer a 30-day money-back guarantee. If you're not satisfied with our service, we'll provide a full refund, no questions asked."
              }
            ].map((faq, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                viewport={{ once: true }}
                className="bg-white rounded-2xl p-6 shadow-lg"
              >
                <h3 className="text-xl font-bold text-gray-800 mb-3">{faq.question}</h3>
                <p className="text-gray-600 leading-relaxed">{faq.answer}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>
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
    </>
  );
};

export default ModernHomePage;