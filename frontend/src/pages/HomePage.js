import React, { useState, useEffect, useMemo } from 'react';
import { Link } from 'react-router-dom';
import ProductCard from '../components/ProductCard';
import { useCurrency } from '../context/CurrencyContext';
import { toast } from 'react-toastify';

const HomePage = () => {
  const [featuredProducts, setFeaturedProducts] = useState([]);
  const [bestsellerProducts, setBestsellerProducts] = useState([]);
  const [blogPosts, setBlogPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [newsletterEmail, setNewsletterEmail] = useState('');
  const [newsletterLoading, setNewsletterLoading] = useState(false);
  const { currency, getCurrencySymbol } = useCurrency();
  
  const [stats, setStats] = useState({
    total_products: 0,
    total_orders: 0,
    total_users: 0,
    today_visitors: 0
  });

  // Loading skeleton component
  const ProductSkeleton = () => (
    <div className="bg-white rounded-lg shadow-md p-4 animate-pulse">
      <div className="loading-shimmer h-48 bg-gray-200 rounded-lg mb-4"></div>
      <div className="loading-shimmer h-4 bg-gray-200 rounded mb-2"></div>
      <div className="loading-shimmer h-3 bg-gray-200 rounded mb-3 w-3/4"></div>
      <div className="loading-shimmer h-6 bg-gray-200 rounded mb-2 w-1/2"></div>
      <div className="loading-shimmer h-8 bg-gray-200 rounded"></div>
    </div>
  );

  // Memoized hero content for better performance
  const heroContent = useMemo(() => ({
    title: "Premium Subscriptions at Unbeatable Prices",
    subtitle: "Get access to Netflix, Adobe, Microsoft, VPNs and more at 70% OFF",
    benefits: [
      "✅ Instant Digital Delivery",
      "✅ 100% Genuine Products", 
      "✅ Money Back Guarantee",
      "✅ 24/7 Customer Support"
    ]
  }), []);

  useEffect(() => {
    fetchHomeData();
  }, []);

  const fetchHomeData = async () => {
    try {
      const [featuredRes, bestsellerRes] = await Promise.all([
        fetch(`${process.env.REACT_APP_BACKEND_URL}/api/products/featured?limit=8`),
        fetch(`${process.env.REACT_APP_BACKEND_URL}/api/products/bestsellers?limit=8`)
      ]);

      const [featuredData, bestsellerData] = await Promise.all([
        featuredRes.json(),
        bestsellerRes.json()
      ]);

      if (featuredData.success) setFeaturedProducts(featuredData.data);
      if (bestsellerData.success) setBestsellerProducts(bestsellerData.data);
      
      // Set mock stats for better UX
      setStats({
        total_products: 83,
        total_orders: 2547,
        total_users: 1089,
        today_visitors: 234
      });
    } catch (error) {
      console.error('Error fetching home data:', error);
      toast.error('Failed to load some content. Please refresh the page.');
    } finally {
      setLoading(false);
    }
  };

  const handleNewsletterSubmit = async (e) => {
    e.preventDefault();
    if (!newsletterEmail.trim()) {
      toast.error('Please enter a valid email address');
      return;
    }
    
    setNewsletterLoading(true);
    try {
      // Simulate API call for newsletter subscription
      await new Promise(resolve => setTimeout(resolve, 1000));
      toast.success('Successfully subscribed to newsletter! 🎉');
      setNewsletterEmail('');
    } catch (error) {
      toast.error('Failed to subscribe. Please try again.');
    } finally {
      setNewsletterLoading(false);
    }
  };

  const categories = [
    {
      name: 'OTT Platforms',
      slug: 'ott',
      icon: '📺',
      description: 'Netflix, Amazon Prime, Disney+',
      color: 'bg-red-500'
    },
    {
      name: 'Software & Tools',
      slug: 'software',
      icon: '💻',
      description: 'Adobe, Microsoft Office, Canva',
      color: 'bg-blue-500'
    },
    {
      name: 'VPN & Security',
      slug: 'vpn',
      icon: '🔒',
      description: 'ExpressVPN, NordVPN, Security',
      color: 'bg-green-500'
    },
    {
      name: 'Professional',
      slug: 'professional',
      icon: '🎓',
      description: 'LinkedIn, Coursera, Learning',
      color: 'bg-purple-500'
    },
    {
      name: 'Gaming',
      slug: 'gaming',
      icon: '🎮',
      description: 'Steam, Gaming Platforms',
      color: 'bg-orange-500'
    }
  ];

  const features = [
    {
      icon: '⚡',
      title: 'Instant Delivery',
      description: 'Get your subscription details instantly via WhatsApp or email'
    },
    {
      icon: '🔒',
      title: '100% Secure',
      description: 'SSL encrypted payments and secure checkout process'
    },
    {
      icon: '💰',
      title: 'Best Prices',
      description: 'Save up to 70% on premium subscription services'
    },
    {
      icon: '🎯',
      title: 'Genuine Accounts',
      description: 'All subscriptions are 100% genuine and legally obtained'
    },
    {
      icon: '📞',
      title: '24/7 Support',
      description: 'Round-the-clock customer support via WhatsApp and email'
    },
    {
      icon: '✅',
      title: 'Money Back Guarantee',
      description: '30-day money-back guarantee if not satisfied'
    }
  ];

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading amazing deals...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <section className="relative bg-gradient-to-br from-blue-600 via-purple-600 to-blue-800 text-white py-20 overflow-hidden">
        <div className="absolute inset-0 bg-black opacity-10"></div>
        <div className="container mx-auto px-4 relative z-10">
          <div className="max-w-4xl mx-auto text-center">
            <div className="mb-6">
              <span className="inline-block bg-yellow-400 text-black px-4 py-2 rounded-full text-sm font-bold mb-4">
                🔥 LIMITED TIME OFFER - Up to 70% OFF
              </span>
            </div>
            <h1 className="responsive-heading font-bold mb-6 leading-tight">
              {heroContent.title}
            </h1>
            <p className="text-xl mb-8 opacity-90 max-w-2xl mx-auto">
              {heroContent.subtitle}
            </p>
            
            {/* Trust indicators */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8 text-sm">
              {heroContent.benefits.map((benefit, index) => (
                <div key={index} className="flex items-center justify-center">
                  <span className="text-green-400 mr-2">✓</span>
                  <span>{benefit.replace('✅ ', '')}</span>
                </div>
              ))}
            </div>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                to="/products"
                className="btn-primary transform hover:scale-105"
              >
                🛍️ Browse All Deals
              </Link>
              <Link
                to="/category/ott"
                className="btn-secondary text-white border-white hover:bg-white hover:text-blue-600"
              >
                📺 OTT Platforms
              </Link>
            </div>
            
            {/* Current currency display */}
            <div className="mt-6 text-sm opacity-75">
              <span>💰 Prices shown in {currency} • Switch currency anytime</span>
            </div>
          </div>
        </div>
        
        {/* Enhanced floating elements */}
        <div className="absolute top-10 left-10 animate-bounce hidden md:block">
          <div className="bg-white bg-opacity-20 p-4 rounded-xl shadow-lg">
            <span className="text-3xl">📺</span>
          </div>
        </div>
        <div className="absolute bottom-10 right-10 animate-bounce hidden md:block" style={{ animationDelay: '0.5s' }}>
          <div className="bg-white bg-opacity-20 p-4 rounded-xl shadow-lg">
            <span className="text-3xl">💻</span>
          </div>
        </div>
        <div className="absolute top-1/2 left-5 animate-pulse hidden lg:block" style={{ animationDelay: '1s' }}>
          <div className="bg-white bg-opacity-15 p-3 rounded-lg">
            <span className="text-2xl">🔒</span>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-12 bg-white">
        <div className="container mx-auto px-4">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
            <div className="text-center">
              <div className="text-3xl font-bold text-blue-600 mb-2">{stats.total_products}+</div>
              <div className="text-gray-600">Premium Products</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-green-600 mb-2">{stats.total_orders}+</div>
              <div className="text-gray-600">Happy Customers</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-purple-600 mb-2">70%</div>
              <div className="text-gray-600">Max Savings</div>
            </div>
            <div className="text-center">
              <div className="text-3xl font-bold text-orange-600 mb-2">24/7</div>
              <div className="text-gray-600">Support Available</div>
            </div>
          </div>
        </div>
      </section>

      {/* Categories Section */}
      <section className="py-16 bg-gray-50">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-800 mb-4">Browse by Category</h2>
            <p className="text-gray-600">Find the perfect subscription for your needs</p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-6">
            {categories.map((category) => (
              <Link
                key={category.slug}
                to={`/category/${category.slug}`}
                className="group bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300 overflow-hidden"
              >
                <div className={`${category.color} p-6 text-center text-white`}>
                  <div className="text-4xl mb-2">{category.icon}</div>
                  <h3 className="text-lg font-semibold mb-1">{category.name}</h3>
                  <p className="text-sm opacity-90">{category.description}</p>
                </div>
                <div className="p-4 text-center">
                  <span className="text-blue-600 font-semibold group-hover:text-blue-800 transition-colors">
                    View Products →
                  </span>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </section>

      {/* Featured Products */}
      <section className="py-16 bg-white">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-800 mb-4">Featured Products</h2>
            <p className="text-gray-600">Hand-picked premium subscriptions at amazing prices</p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {loading ? (
              // Loading skeletons
              Array(8).fill(0).map((_, index) => (
                <ProductSkeleton key={index} />
              ))
            ) : (
              featuredProducts.map((product) => (
                <ProductCard key={product.id} product={product} />
              ))
            )}
          </div>
          <div className="text-center mt-8">
            <Link
              to="/products?featured=true"
              className="bg-blue-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
            >
              View All Featured Products
            </Link>
          </div>
        </div>
      </section>

      {/* Bestsellers */}
      <section className="py-16 bg-gray-50">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-800 mb-4">Best Sellers</h2>
            <p className="text-gray-600">Most popular subscriptions among our customers</p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {bestsellerProducts.map((product) => (
              <ProductCard key={product.id} product={product} />
            ))}
          </div>
          <div className="text-center mt-8">
            <Link
              to="/products?bestseller=true"
              className="bg-green-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-green-700 transition-colors"
            >
              View All Best Sellers
            </Link>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 bg-white">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-gray-800 mb-4">Why Choose Premium Shop?</h2>
            <p className="text-gray-600">We make premium subscriptions accessible to everyone</p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <div key={index} className="text-center p-6 bg-gray-50 rounded-lg">
                <div className="text-4xl mb-4">{feature.icon}</div>
                <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
                <p className="text-gray-600">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Blog Section */}
      {blogPosts.length > 0 && (
        <section className="py-16 bg-gray-50">
          <div className="container mx-auto px-4">
            <div className="text-center mb-12">
              <h2 className="text-3xl font-bold text-gray-800 mb-4">Latest from Our Blog</h2>
              <p className="text-gray-600">Tips, guides, and news about premium subscriptions</p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {blogPosts.map((post) => (
                <Link
                  key={post.id}
                  to={`/blog/${post.slug}`}
                  className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300 overflow-hidden group"
                >
                  <img
                    src={post.featured_image}
                    alt={post.title}
                    className="w-full h-48 object-cover group-hover:scale-105 transition-transform duration-300"
                  />
                  <div className="p-6">
                    <div className="flex items-center text-sm text-gray-500 mb-2">
                      <span>{post.category}</span>
                      <span className="mx-2">•</span>
                      <span>{new Date(post.created_at).toLocaleDateString()}</span>
                    </div>
                    <h3 className="text-xl font-semibold mb-2 group-hover:text-blue-600 transition-colors">
                      {post.title}
                    </h3>
                    <p className="text-gray-600 line-clamp-3">{post.excerpt}</p>
                  </div>
                </Link>
              ))}
            </div>
            <div className="text-center mt-8">
              <Link
                to="/blog"
                className="bg-purple-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-purple-700 transition-colors"
              >
                Read More Articles
              </Link>
            </div>
          </div>
        </section>
      )}

      {/* CTA Section */}
      <section className="py-16 bg-gradient-to-r from-green-600 to-blue-600 text-white">
        <div className="container mx-auto px-4">
          <div className="max-w-4xl mx-auto text-center">
            <h2 className="text-3xl font-bold mb-4">Ready to Save Big on Premium Subscriptions?</h2>
            <p className="text-xl mb-8 opacity-90">
              Join thousands of satisfied customers who are already saving money with our premium subscription deals.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                to="/products"
                className="bg-white text-blue-600 px-8 py-4 rounded-lg font-semibold hover:bg-gray-100 transition-colors"
              >
                Start Shopping Now
              </Link>
              <Link
                to="/contact"
                className="border-2 border-white text-white px-8 py-4 rounded-lg font-semibold hover:bg-white hover:text-blue-600 transition-colors"
              >
                Contact Support
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Newsletter Section */}
      <section className="py-16 bg-gray-800 text-white">
        <div className="container mx-auto px-4">
          <div className="max-w-2xl mx-auto text-center">
            <h2 className="text-3xl font-bold mb-4">Never Miss a Deal</h2>
            <p className="text-gray-300 mb-8">
              Subscribe to our newsletter and get exclusive discounts, new product alerts, and money-saving tips.
            </p>
            <form onSubmit={handleNewsletterSubmit} className="flex flex-col sm:flex-row gap-4">
              <input
                type="email"
                value={newsletterEmail}
                onChange={(e) => setNewsletterEmail(e.target.value)}
                placeholder="Enter your email address"
                required
                disabled={newsletterLoading}
                className="flex-1 px-4 py-3 rounded-lg text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
              />
              <button
                type="submit"
                disabled={newsletterLoading}
                className="bg-blue-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {newsletterLoading ? (
                  <span className="flex items-center">
                    <div className="loading-spinner mr-2"></div>
                    Subscribing...
                  </span>
                ) : (
                  'Subscribe'
                )}
              </button>
            </form>
            <p className="text-sm text-gray-400 mt-4">
              We respect your privacy. Unsubscribe at any time.
            </p>
          </div>
        </div>
      </section>
    </div>
  );
};

export default HomePage;