#!/bin/bash

# Shop VIP Premium - Create All Frontend Pages
# This script creates all remaining React page components

set -e

echo "📄 Creating all frontend pages..."
echo "================================"

cd /var/www/shopvippremium/frontend

# Create src/pages directory if it doesn't exist
mkdir -p src/pages

# Create HomePage.js
cat > src/pages/HomePage.js << 'EOF'
import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Helmet } from 'react-helmet';
import axios from 'axios';
import { motion } from 'framer-motion';
import { useCurrency } from '../context/CurrencyContext';

const HomePage = () => {
  const [featuredProducts, setFeaturedProducts] = useState([]);
  const [bestsellerProducts, setBestsellerProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const { formatPrice } = useCurrency();

  const API_URL = process.env.REACT_APP_BACKEND_URL;

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    try {
      const [featuredResponse, bestsellersResponse] = await Promise.all([
        axios.get(`${API_URL}/api/products/featured`),
        axios.get(`${API_URL}/api/products/bestsellers`)
      ]);

      setFeaturedProducts(featuredResponse.data.products);
      setBestsellerProducts(bestsellersResponse.data.products);
    } catch (error) {
      console.error('Error fetching products:', error);
    } finally {
      setLoading(false);
    }
  };

  const ProductCard = ({ product }) => (
    <motion.div
      whileHover={{ y: -5 }}
      className="card-dark rounded-xl p-6 transition-all duration-300"
    >
      <div className="aspect-w-16 aspect-h-9 mb-4">
        <img
          src={product.image_url}
          alt={product.name}
          className="w-full h-48 object-cover rounded-lg"
        />
      </div>
      <h3 className="text-lg font-semibold text-white mb-2">{product.name}</h3>
      <p className="text-gray-400 text-sm mb-4 line-clamp-3">{product.description}</p>
      <div className="flex items-center justify-between">
        <span className="text-2xl font-bold text-blue-400">
          {formatPrice(product.price_usd, product.price_inr)}
        </span>
        <Link
          to={`/product/${product.id}`}
          className="btn-primary text-sm"
        >
          View Details
        </Link>
      </div>
    </motion.div>
  );

  return (
    <div>
      <Helmet>
        <title>Shop VIP Premium - Digital Workspace Toolkit</title>
        <meta name="description" content="Premium digital workspace tools and productivity software for professionals and freelancers. Get access to cutting-edge business solutions." />
      </Helmet>

      {/* Hero Section */}
      <section className="bg-gradient-dark py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <motion.h1
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
              className="text-4xl md:text-6xl font-bold text-white mb-6"
            >
              Premium Digital <span className="text-gradient">Workspace Toolkit</span>
            </motion.h1>
            <motion.p
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.2 }}
              className="text-xl text-gray-300 mb-8 max-w-3xl mx-auto"
            >
              Discover professional-grade productivity tools, business utilities, and freelancer solutions
              designed to elevate your digital workspace experience.
            </motion.p>
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.4 }}
              className="flex flex-col sm:flex-row gap-4 justify-center"
            >
              <Link to="/products" className="btn-primary text-lg px-8">
                Browse Products
              </Link>
              <Link to="/about" className="btn-secondary text-lg px-8">
                Learn More
              </Link>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 bg-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-white mb-4">Why Choose Shop VIP Premium?</h2>
            <p className="text-gray-400 max-w-2xl mx-auto">
              We provide premium digital solutions with unmatched quality and support
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <motion.div
              whileHover={{ scale: 1.05 }}
              className="text-center p-6 card-dark rounded-xl"
            >
              <div className="w-16 h-16 bg-blue-500 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-white mb-2">Premium Quality</h3>
              <p className="text-gray-400">
                Professional-grade digital tools and utilities crafted for excellence
              </p>
            </motion.div>

            <motion.div
              whileHover={{ scale: 1.05 }}
              className="text-center p-6 card-dark rounded-xl"
            >
              <div className="w-16 h-16 bg-green-500 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M2.166 4.999A11.954 11.954 0 0010 1.944 11.954 11.954 0 0017.834 5c.11.65.166 1.32.166 2.001 0 5.225-3.34 9.67-8 11.317C5.34 16.67 2 12.225 2 7c0-.682.057-1.35.166-2.001zm11.541 3.708a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"/>
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-white mb-2">Secure Payments</h3>
              <p className="text-gray-400">
                Safe and secure cryptocurrency payments for your peace of mind
              </p>
            </motion.div>

            <motion.div
              whileHover={{ scale: 1.05 }}
              className="text-center p-6 card-dark rounded-xl"
            >
              <div className="w-16 h-16 bg-purple-500 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-white" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-8-3a1 1 0 00-.867.5 1 1 0 11-1.731-1A3 3 0 0113 8a3.001 3.001 0 01-2 2.83V11a1 1 0 11-2 0v-1a1 1 0 011-1 1 1 0 100-2zm0 8a1 1 0 100-2 1 1 0 000 2z"/>
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-white mb-2">24/7 Support</h3>
              <p className="text-gray-400">
                Round-the-clock customer support via Telegram and WhatsApp
              </p>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Featured Products */}
      {!loading && featuredProducts.length > 0 && (
        <section className="py-16 bg-gray-900">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-12">
              <h2 className="text-3xl font-bold text-white mb-4">Featured Products</h2>
              <p className="text-gray-400">Discover our most popular digital workspace solutions</p>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {featuredProducts.slice(0, 3).map((product) => (
                <ProductCard key={product.id} product={product} />
              ))}
            </div>
            
            <div className="text-center mt-12">
              <Link to="/products" className="btn-primary">
                View All Products
              </Link>
            </div>
          </div>
        </section>
      )}

      {/* Bestsellers */}
      {!loading && bestsellerProducts.length > 0 && (
        <section className="py-16 bg-gray-800">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center mb-12">
              <h2 className="text-3xl font-bold text-white mb-4">Bestsellers</h2>
              <p className="text-gray-400">Top-rated products trusted by professionals</p>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {bestsellerProducts.slice(0, 3).map((product) => (
                <ProductCard key={product.id} product={product} />
              ))}
            </div>
          </div>
        </section>
      )}

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-blue-600 to-purple-600">
        <div className="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-6">
            Ready to Upgrade Your Digital Workspace?
          </h2>
          <p className="text-xl text-blue-100 mb-8">
            Join thousands of professionals who trust Shop VIP Premium for their business tools
          </p>
          <Link
            to="/products"
            className="inline-block bg-white text-blue-600 font-semibold py-4 px-8 rounded-lg hover:bg-gray-100 transition-colors text-lg"
          >
            Start Shopping Now
          </Link>
        </div>
      </section>
    </div>
  );
};

export default HomePage;
EOF

# Create ProductsPage.js
cat > src/pages/ProductsPage.js << 'EOF'
import React, { useState, useEffect } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import { Helmet } from 'react-helmet';
import axios from 'axios';
import { motion } from 'framer-motion';
import { useCurrency } from '../context/CurrencyContext';
import { MagnifyingGlassIcon, FunnelIcon } from '@heroicons/react/24/outline';

const ProductsPage = () => {
  const [products, setProducts] = useState([]);
  const [filteredProducts, setFilteredProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');
  const [searchParams, setSearchParams] = useSearchParams();
  const { formatPrice } = useCurrency();

  const API_URL = process.env.REACT_APP_BACKEND_URL;

  const categories = [
    'All',
    'Productivity',
    'Business',
    'Creative',
    'Development',
    'Marketing'
  ];

  useEffect(() => {
    fetchProducts();
    
    // Handle search params
    const search = searchParams.get('search');
    const category = searchParams.get('category');
    
    if (search) {
      setSearchTerm(search);
    }
    if (category) {
      setSelectedCategory(category);
    }
  }, [searchParams]);

  useEffect(() => {
    filterProducts();
  }, [products, searchTerm, selectedCategory]);

  const fetchProducts = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/products?limit=50`);
      setProducts(response.data.products);
    } catch (error) {
      console.error('Error fetching products:', error);
    } finally {
      setLoading(false);
    }
  };

  const filterProducts = () => {
    let filtered = products;

    // Filter by search term
    if (searchTerm) {
      filtered = filtered.filter(product =>
        product.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        product.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
        product.category.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    // Filter by category
    if (selectedCategory && selectedCategory !== 'All') {
      filtered = filtered.filter(product => product.category === selectedCategory);
    }

    setFilteredProducts(filtered);
  };

  const handleSearchChange = (e) => {
    setSearchTerm(e.target.value);
    updateSearchParams(e.target.value, selectedCategory);
  };

  const handleCategoryChange = (category) => {
    const newCategory = category === 'All' ? '' : category;
    setSelectedCategory(newCategory);
    updateSearchParams(searchTerm, newCategory);
  };

  const updateSearchParams = (search, category) => {
    const params = new URLSearchParams();
    if (search) params.set('search', search);
    if (category) params.set('category', category);
    setSearchParams(params);
  };

  const ProductCard = ({ product }) => (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={{ y: -5 }}
      className="card-dark rounded-xl p-6 transition-all duration-300"
    >
      <div className="aspect-w-16 aspect-h-9 mb-4">
        <img
          src={product.image_url}
          alt={product.name}
          className="w-full h-48 object-cover rounded-lg"
        />
      </div>
      
      <div className="flex items-center justify-between mb-2">
        <span className="text-xs font-medium text-blue-400 bg-blue-400 bg-opacity-10 px-2 py-1 rounded">
          {product.category}
        </span>
        {product.is_featured && (
          <span className="text-xs font-medium text-yellow-400 bg-yellow-400 bg-opacity-10 px-2 py-1 rounded">
            Featured
          </span>
        )}
        {product.is_bestseller && (
          <span className="text-xs font-medium text-green-400 bg-green-400 bg-opacity-10 px-2 py-1 rounded">
            Bestseller
          </span>
        )}
      </div>

      <h3 className="text-lg font-semibold text-white mb-2">{product.name}</h3>
      <p className="text-gray-400 text-sm mb-4 line-clamp-3">{product.description}</p>
      
      <div className="flex items-center justify-between">
        <span className="text-2xl font-bold text-blue-400">
          {formatPrice(product.price_usd, product.price_inr)}
        </span>
        <Link
          to={`/product/${product.id}`}
          className="btn-primary text-sm"
        >
          View Details
        </Link>
      </div>
    </motion.div>
  );

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-900 py-8">
      <Helmet>
        <title>All Products - Shop VIP Premium</title>
        <meta name="description" content="Browse our complete collection of premium digital workspace tools, productivity software, and professional utilities." />
      </Helmet>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl md:text-4xl font-bold text-white mb-4">
            All Products
          </h1>
          <p className="text-gray-400 max-w-2xl mx-auto">
            Discover our complete collection of premium digital workspace solutions
          </p>
        </div>

        {/* Filters */}
        <div className="bg-gray-800 rounded-xl p-6 mb-8">
          <div className="flex flex-col lg:flex-row gap-4">
            {/* Search Bar */}
            <div className="flex-1 relative">
              <MagnifyingGlassIcon className="h-5 w-5 text-gray-400 absolute left-3 top-1/2 transform -translate-y-1/2" />
              <input
                type="text"
                value={searchTerm}
                onChange={handleSearchChange}
                placeholder="Search products..."
                className="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-2 pl-10 text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>

            {/* Category Filter */}
            <div className="flex items-center space-x-2">
              <FunnelIcon className="h-5 w-5 text-gray-400" />
              <select
                value={selectedCategory}
                onChange={(e) => handleCategoryChange(e.target.value)}
                className="bg-gray-700 border border-gray-600 rounded-lg px-4 py-2 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                {categories.map((category) => (
                  <option key={category} value={category === 'All' ? '' : category}>
                    {category}
                  </option>
                ))}
              </select>
            </div>
          </div>

          {/* Results Summary */}
          <div className="mt-4 text-gray-400 text-sm">
            Showing {filteredProducts.length} of {products.length} products
            {searchTerm && (
              <span> for "{searchTerm}"</span>
            )}
            {selectedCategory && (
              <span> in {selectedCategory}</span>
            )}
          </div>
        </div>

        {/* Products Grid */}
        {filteredProducts.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {filteredProducts.map((product, index) => (
              <ProductCard key={product.id} product={product} />
            ))}
          </div>
        ) : (
          <div className="text-center py-16">
            <div className="text-gray-400 text-lg mb-4">
              {searchTerm || selectedCategory
                ? 'No products found matching your criteria'
                : 'No products available'}
            </div>
            {(searchTerm || selectedCategory) && (
              <button
                onClick={() => {
                  setSearchTerm('');
                  setSelectedCategory('');
                  setSearchParams({});
                }}
                className="btn-primary"
              >
                Clear Filters
              </button>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default ProductsPage;
EOF

# Create ProductDetailPage.js
cat > src/pages/ProductDetailPage.js << 'EOF'
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Helmet } from 'react-helmet';
import { toast } from 'react-toastify';
import axios from 'axios';
import { motion } from 'framer-motion';
import { useAuth } from '../context/AuthContext';
import { useCurrency } from '../context/CurrencyContext';
import { ShoppingCartIcon, StarIcon, CheckIcon } from '@heroicons/react/24/solid';

const ProductDetailPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const { user } = useAuth();
  const { formatPrice, getPrice } = useCurrency();
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);
  const [purchasing, setPurchasing] = useState(false);

  const API_URL = process.env.REACT_APP_BACKEND_URL;

  useEffect(() => {
    fetchProduct();
  }, [id]);

  const fetchProduct = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/products/${id}`);
      setProduct(response.data);
    } catch (error) {
      console.error('Error fetching product:', error);
      toast.error('Product not found');
      navigate('/products');
    } finally {
      setLoading(false);
    }
  };

  const handlePurchase = async () => {
    if (!user) {
      toast.info('Please login to make a purchase');
      navigate('/login', { state: { from: `/product/${id}` } });
      return;
    }

    setPurchasing(true);

    try {
      // Create order
      const orderData = {
        product_ids: [product.id],
        total_amount: getPrice(product.price_usd, product.price_inr),
        currency: 'USD'
      };

      const orderResponse = await axios.post(`${API_URL}/api/orders`, orderData);
      
      // Navigate to checkout
      navigate('/checkout', { 
        state: { 
          orderId: orderResponse.data.order_id,
          product: product
        } 
      });
      
    } catch (error) {
      console.error('Error creating order:', error);
      toast.error('Failed to create order. Please try again.');
    } finally {
      setPurchasing(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (!product) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-white mb-4">Product Not Found</h2>
          <button
            onClick={() => navigate('/products')}
            className="btn-primary"
          >
            Back to Products
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-900 py-8">
      <Helmet>
        <title>{product.name} - Shop VIP Premium</title>
        <meta name="description" content={product.description} />
      </Helmet>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="lg:grid lg:grid-cols-2 lg:gap-8">
          {/* Product Image */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            className="mb-8 lg:mb-0"
          >
            <div className="aspect-w-1 aspect-h-1">
              <img
                src={product.image_url}
                alt={product.name}
                className="w-full h-96 lg:h-full object-cover rounded-xl"
              />
            </div>
          </motion.div>

          {/* Product Info */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            className="space-y-6"
          >
            {/* Category and Tags */}
            <div className="flex items-center space-x-4">
              <span className="text-sm font-medium text-blue-400 bg-blue-400 bg-opacity-10 px-3 py-1 rounded-full">
                {product.category}
              </span>
              {product.is_featured && (
                <span className="text-sm font-medium text-yellow-400 bg-yellow-400 bg-opacity-10 px-3 py-1 rounded-full">
                  Featured
                </span>
              )}
              {product.is_bestseller && (
                <span className="text-sm font-medium text-green-400 bg-green-400 bg-opacity-10 px-3 py-1 rounded-full">
                  Bestseller
                </span>
              )}
            </div>

            {/* Product Name */}
            <h1 className="text-3xl lg:text-4xl font-bold text-white">
              {product.name}
            </h1>

            {/* Rating (Mock data) */}
            <div className="flex items-center space-x-2">
              <div className="flex items-center">
                {[...Array(5)].map((_, i) => (
                  <StarIcon key={i} className="h-5 w-5 text-yellow-400" />
                ))}
              </div>
              <span className="text-gray-400 text-sm">(4.8/5 - 24 reviews)</span>
            </div>

            {/* Price */}
            <div className="text-4xl font-bold text-blue-400">
              {formatPrice(product.price_usd, product.price_inr)}
            </div>

            {/* Description */}
            <div className="prose prose-invert">
              <p className="text-gray-300 text-lg leading-relaxed">
                {product.description}
              </p>
            </div>

            {/* Key Features */}
            <div className="space-y-3">
              <h3 className="text-lg font-semibold text-white">Key Features:</h3>
              <ul className="space-y-2">
                <li className="flex items-center text-gray-300">
                  <CheckIcon className="h-5 w-5 text-green-400 mr-3" />
                  Professional-grade digital workspace tools
                </li>
                <li className="flex items-center text-gray-300">
                  <CheckIcon className="h-5 w-5 text-green-400 mr-3" />
                  Complete productivity suite included
                </li>
                <li className="flex items-center text-gray-300">
                  <CheckIcon className="h-5 w-5 text-green-400 mr-3" />
                  24/7 customer support via Telegram/WhatsApp
                </li>
                <li className="flex items-center text-gray-300">
                  <CheckIcon className="h-5 w-5 text-green-400 mr-3" />
                  Instant delivery after payment confirmation
                </li>
              </ul>
            </div>

            {/* Purchase Section */}
            <div className="bg-gray-800 rounded-xl p-6 space-y-4">
              <div className="flex items-center justify-between">
                <span className="text-white font-medium">
                  {product.in_stock ? '✅ In Stock' : '❌ Out of Stock'}
                </span>
                <span className="text-gray-400 text-sm">
                  Secure payment with cryptocurrency
                </span>
              </div>

              <button
                onClick={handlePurchase}
                disabled={!product.in_stock || purchasing}
                className={`w-full flex items-center justify-center space-x-2 py-4 px-6 rounded-lg font-semibold text-lg transition-all duration-200 ${
                  product.in_stock && !purchasing
                    ? 'bg-blue-600 hover:bg-blue-700 text-white transform hover:scale-105'
                    : 'bg-gray-600 text-gray-400 cursor-not-allowed'
                }`}
              >
                <ShoppingCartIcon className="h-6 w-6" />
                <span>
                  {purchasing
                    ? 'Processing...'
                    : product.in_stock
                    ? 'Buy Now'
                    : 'Out of Stock'}
                </span>
              </button>

              <div className="text-center">
                <p className="text-gray-400 text-sm">
                  Secure checkout with cryptocurrency payments
                </p>
              </div>
            </div>

            {/* Support Info */}
            <div className="bg-gray-800 rounded-xl p-6">
              <h3 className="text-lg font-semibold text-white mb-4">Need Help?</h3>
              <div className="flex space-x-4">
                <a
                  href="https://t.me/shopvippremium"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center space-x-2 text-blue-400 hover:text-blue-300"
                >
                  <span>📱</span>
                  <span>Telegram Support</span>
                </a>
                <a
                  href="https://wa.me/1234567890"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center space-x-2 text-green-400 hover:text-green-300"
                >
                  <span>💬</span>
                  <span>WhatsApp Support</span>
                </a>
              </div>
            </div>
          </motion.div>
        </div>
      </div>
    </div>
  );
};

export default ProductDetailPage;
EOF

echo "✅ Main pages created successfully!"
echo "📄 Creating additional pages..."

# Continue with checkout and other pages...