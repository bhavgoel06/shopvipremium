import React, { useState, useEffect, useRef } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import ModernProductCard from '../components/ModernProductCard';
import { Helmet } from 'react-helmet';
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
    <>
      <Helmet>
        <title>Digital Workspace Toolkit - Essential Tools for Creators | Professional Utilities</title>
        <meta name="description" content="Access curated digital productivity tools and utilities for creators, freelancers, and professionals. Comprehensive workspace resources with immediate access and 24/7 support." />
        <meta name="keywords" content="premium subscriptions, group subscriptions, cheap netflix, discount spotify, adobe creative cloud, group plans, shared subscriptions" />
        
        {/* Open Graph Tags */}
        <meta property="og:title" content="Digital Workspace Toolkit - Professional Utilities for Creators" />
        <meta property="og:description" content="Access curated productivity tools and digital utilities for modern professionals. Comprehensive workspace resources with technical support." />
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

      {/* Modern Hero Section */}
      <section className="relative min-h-screen flex items-center justify-center overflow-hidden bg-gradient-to-br from-indigo-900 via-purple-900 to-pink-900">
        {/* Background Pattern */}
        <div className="absolute inset-0 opacity-10">
          <div className="absolute inset-0" style={{
            backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.1'%3E%3Ccircle cx='7' cy='7' r='1'/%3E%3Ccircle cx='53' cy='7' r='1'/%3E%3Ccircle cx='7' cy='53' r='1'/%3E%3Ccircle cx='53' cy='53' r='1'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`,
          }} />
        </div>

        <div className="relative z-10 max-w-7xl mx-auto px-6 text-center">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="mb-8"
          >
            {/* Premium Badge */}
            <div className="inline-flex items-center gap-2 bg-white/10 backdrop-blur-sm border border-white/20 rounded-full px-6 py-3 mb-8">
              <span className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></span>
              <span className="text-white font-medium">Live • Save up to 90% on Premium Subscriptions</span>
            </div>
            
            <h1 className="text-5xl md:text-7xl lg:text-8xl font-bold mb-6">
              <span className="bg-gradient-to-r from-white via-blue-100 to-purple-100 bg-clip-text text-transparent">
                Premium
              </span>
              <br />
              <span className="bg-gradient-to-r from-blue-200 via-purple-200 to-pink-200 bg-clip-text text-transparent">
                Subscriptions
              </span>
            </h1>
            
            <p className="text-xl md:text-2xl text-gray-200 mb-8 max-w-3xl mx-auto leading-relaxed">
              Access Netflix, Spotify, Adobe Creative Suite & 50+ premium services at fraction of original cost
            </p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3, duration: 0.8 }}
            className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-12"
          >
            <Link
              to="/products"
              className="group relative px-8 py-4 bg-white text-gray-900 rounded-2xl font-semibold text-lg hover:scale-105 transition-all duration-300 shadow-2xl flex items-center gap-3 min-w-[200px] justify-center"
            >
              <svg className="w-5 h-5 group-hover:rotate-12 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
              Get Started Now
            </Link>
            
            <Link
              to="/products"
              className="group px-8 py-4 border-2 border-white/30 text-white rounded-2xl font-semibold text-lg hover:bg-white/10 transition-all duration-300 flex items-center gap-3 min-w-[200px] justify-center backdrop-blur-sm"
            >
              <svg className="w-5 h-5 group-hover:scale-110 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
              Browse Products
            </Link>
          </motion.div>

          {/* Trust Indicators Row */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.6, duration: 0.8 }}
            className="grid grid-cols-2 md:grid-cols-4 gap-8 max-w-4xl mx-auto"
          >
            <div className="text-center">
              <div className="text-3xl font-bold text-white mb-1">10K+</div>
              <div className="text-sm text-gray-300">Happy Customers</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-white mb-1">50+</div>
              <div className="text-sm text-gray-300">Premium Services</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-white mb-1">4.9⭐</div>
              <div className="text-sm text-gray-300">Customer Rating</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-white mb-1">₹5</div>
              <div className="text-sm text-gray-300">Starting Price</div>
            </div>
          </motion.div>

          {/* Floating Elements */}
          <div className="absolute top-1/4 left-1/4 w-20 h-20 bg-blue-500/20 rounded-full blur-xl animate-pulse"></div>
          <div className="absolute bottom-1/4 right-1/4 w-32 h-32 bg-purple-500/20 rounded-full blur-xl animate-pulse" style={{ animationDelay: '1s' }}></div>
        </div>

        {/* Scroll Indicator */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1, duration: 0.8 }}
          className="absolute bottom-8 left-1/2 transform -translate-x-1/2"
        >
          <motion.div
            animate={{ y: [0, 8, 0] }}
            transition={{ duration: 2, repeat: Infinity }}
            className="w-6 h-10 border-2 border-white/50 rounded-full flex justify-center"
          >
            <motion.div
              animate={{ y: [0, 16, 0] }}
              transition={{ duration: 2, repeat: Infinity }}
              className="w-1 h-3 bg-white/70 rounded-full mt-2"
            />
          </motion.div>
        </motion.div>
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

      {/* Modern Product Showcase */}
      <section className="relative py-24 bg-white">
        <div className="max-w-7xl mx-auto px-6">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            className="text-center mb-20"
          >
            <div className="inline-flex items-center gap-2 bg-blue-50 text-blue-600 rounded-full px-4 py-2 mb-6">
              <span className="w-2 h-2 bg-blue-600 rounded-full"></span>
              <span className="font-medium text-sm">Popular Services</span>
            </div>
            <h2 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
              Premium subscriptions at
              <span className="block bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                unbeatable prices
              </span>
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Get instant access to your favorite services and save up to 90% compared to official pricing
            </p>
          </motion.div>

          {/* Modern Product Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8">
            {loading ? (
              Array(12).fill(0).map((_, index) => (
                <motion.div 
                  key={index} 
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className="bg-white rounded-3xl overflow-hidden shadow-sm border border-gray-100 group hover:shadow-2xl transition-all duration-500"
                >
                  <div className="aspect-[4/3] bg-gradient-to-br from-gray-100 to-gray-200 animate-pulse" />
                  <div className="p-6 space-y-4">
                    <div className="h-6 bg-gray-200 rounded-lg animate-pulse" />
                    <div className="h-4 bg-gray-200 rounded w-3/4 animate-pulse" />
                    <div className="h-4 bg-gray-200 rounded w-1/2 animate-pulse" />
                    <div className="h-12 bg-gray-200 rounded-xl animate-pulse" />
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
                  className="group"
                >
                  <div className="bg-white rounded-3xl overflow-hidden shadow-sm border border-gray-100 group-hover:shadow-2xl group-hover:border-blue-200 transition-all duration-500 group-hover:-translate-y-2">
                    <ModernProductCard product={product} />
                  </div>
                </motion.div>
              ))
            ) : (
              <div className="col-span-full text-center py-20">
                <div className="w-24 h-24 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-6">
                  <svg className="w-12 h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
                  </svg>
                </div>
                <h3 className="text-2xl font-bold text-gray-900 mb-2">No Products Available</h3>
                <p className="text-gray-600">Check back soon for amazing deals on premium subscriptions.</p>
              </div>
            )}
          </div>

          {/* View All Button */}
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className="text-center mt-16"
          >
            <Link
              to="/products"
              className="inline-flex items-center gap-3 px-8 py-4 bg-gray-900 text-white rounded-2xl font-semibold hover:bg-gray-800 transition-all duration-300 group"
            >
              <span>View All Products</span>
              <svg className="w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
              </svg>
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
                question: "Do you offer refunds?",
                answer: "All sales are final and don't raise any dispute/chargeback, contact us to resolve any issues. Doing so will lead to report and ban from placing new orders."
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