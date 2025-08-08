import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { useCart } from '../context/CartContext';
import { useCurrency } from '../context/CurrencyContext';
import { toast } from 'react-toastify';

const ProductCard = ({ product, className = '' }) => {
  const { addToCart } = useCart();
  const { formatPrice, currency } = useCurrency();
  const [imageLoaded, setImageLoaded] = useState(false);
  const [imageError, setImageError] = useState(false);
  const [priceKey, setPriceKey] = useState(0);

  // Force re-render when currency changes
  useEffect(() => {
    setPriceKey(prev => prev + 1);
  }, [currency]);

  // Also listen to custom currency change event
  useEffect(() => {
    const handleCurrencyChange = () => {
      setPriceKey(prev => prev + 1);
    };

    window.addEventListener('currencyChanged', handleCurrencyChange);
    return () => window.removeEventListener('currencyChanged', handleCurrencyChange);
  }, []);

  const handleAddToCart = (e) => {
    e.preventDefault();
    e.stopPropagation();
    
    const defaultDuration = product.duration_options[0];
    addToCart(product, defaultDuration);
    toast.success(`${product.name} added to cart!`);
  };

  const handleImageLoad = () => {
    setImageLoaded(true);
  };

  const handleImageError = () => {
    setImageError(true);
    setImageLoaded(true);
  };

  const renderStars = (rating) => {
    const stars = [];
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 !== 0;
    
    for (let i = 0; i < fullStars; i++) {
      stars.push(
        <span key={i} className="text-yellow-400 text-sm">★</span>
      );
    }
    
    if (hasHalfStar) {
      stars.push(
        <span key="half" className="text-yellow-400 text-sm">★</span>
      );
    }
    
    // Fill remaining stars with empty stars
    for (let i = stars.length; i < 5; i++) {
      stars.push(
        <span key={`empty-${i}`} className="text-gray-400 text-sm">★</span>
      );
    }
    
    return stars;
  };

  // Generate fallback slug if missing
  const generateSlug = (name) => {
    return name.toLowerCase()
      .replace(/[^\w\s-]/g, '') // Remove special characters
      .replace(/\s+/g, '-') // Replace spaces with hyphens
      .replace(/-+/g, '-') // Replace multiple hyphens with single
      .trim(); // Remove leading/trailing spaces
  };

  const productSlug = product.slug || generateSlug(product.name);

  return (
    <Link to={`/products/${productSlug}`} className="block">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        whileHover={{ y: -8, scale: 1.02 }}
        transition={{ duration: 0.3 }}
        className={`bg-white rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 overflow-hidden group cursor-pointer ${className}`}
      >
        <div className="relative">
          {/* Product Image */}
          <div className="aspect-w-16 aspect-h-12 bg-gradient-to-br from-gray-100 to-gray-200 overflow-hidden h-48 relative">
            {!imageLoaded && (
              <div className="absolute inset-0 flex items-center justify-center">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
              </div>
            )}
            
            {imageError ? (
              <div className="absolute inset-0 flex items-center justify-center bg-gray-100">
                <div className="text-center">
                  <div className="text-4xl text-gray-400 mb-2">📦</div>
                  <div className="text-xs text-gray-500">No Image</div>
                </div>
              </div>
            ) : (
              <img
                src={product.image_url}
                alt={product.name}
                className={`w-full h-full object-contain group-hover:scale-105 transition-transform duration-300 p-4 ${
                  imageLoaded ? 'opacity-100' : 'opacity-0'
                }`}
                onLoad={handleImageLoad}
                onError={handleImageError}
              />
            )}
          </div>
          
          {/* Badges */}
          <div className="absolute top-3 left-3 flex flex-col gap-1">
            {product.is_bestseller && (
              <span className="bg-red-500 text-white px-2 py-1 rounded-full text-xs font-semibold flex items-center gap-1">
                🔥 Bestseller
              </span>
            )}
            {product.is_featured && (
              <span className="bg-blue-500 text-white px-2 py-1 rounded-full text-xs font-semibold flex items-center gap-1">
                ⭐ Featured
              </span>
            )}
            {product.discount_percentage > 0 && (
              <span className="bg-green-500 text-white px-2 py-1 rounded-full text-xs font-semibold">
                {product.discount_percentage}% OFF
              </span>
            )}
          </div>

          {/* Stock Status */}
          <div className="absolute top-3 right-3">
            {product.stock_quantity > 0 ? (
              <span className="bg-green-100 text-green-800 px-2 py-1 rounded-full text-xs font-medium">
                In Stock
              </span>
            ) : (
              <span className="bg-red-100 text-red-800 px-2 py-1 rounded-full text-xs font-medium">
                Out of Stock
              </span>
            )}
          </div>
        </div>

        <div className="p-6">
          {/* Product Name */}
          <h3 className="font-bold text-gray-900 mb-2 text-lg leading-tight line-clamp-2 min-h-[3.5rem]">
            {product.name}
          </h3>
          
          {/* Description */}
          <p className="text-gray-600 mb-4 text-sm line-clamp-2 min-h-[2.5rem]">
            {product.short_description}
          </p>

          {/* Rating */}
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-1">
              {renderStars(product.rating)}
              <span className="text-sm text-gray-500 ml-1">
                ({product.total_reviews})
              </span>
            </div>
            <span className="text-xs text-gray-500">
              {product.total_sales} sold
            </span>
          </div>

          {/* Price Section */}
          <div className="mb-6 p-4 bg-gray-50 rounded-lg" key={priceKey}>
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center gap-3">
                <span className="text-2xl font-bold text-gray-900">
                  {formatPrice(product.discounted_price)}
                </span>
                {product.original_price > product.discounted_price && (
                  <span className="text-lg text-gray-500 line-through">
                    {formatPrice(product.original_price)}
                  </span>
                )}
              </div>
              <div className="text-right">
                <span className="text-sm font-medium text-green-600 bg-green-100 px-2 py-1 rounded-full">
                  Save {formatPrice(product.original_price - product.discounted_price)}
                </span>
              </div>
            </div>
            <div className="text-xs text-gray-500">
              💰 Best price guaranteed • 🔒 Secure payment
            </div>
          </div>

          {/* Features */}
          <div className="mb-4">
            <div className="flex flex-wrap gap-1">
              {product.features.slice(0, 3).map((feature, index) => (
                <span key={index} className="bg-gray-100 text-gray-700 px-2 py-1 rounded-md text-xs">
                  {feature}
                </span>
              ))}
              {product.features.length > 3 && (
                <span className="bg-gray-100 text-gray-700 px-2 py-1 rounded-md text-xs">
                  +{product.features.length - 3} more
                </span>
              )}
            </div>
          </div>

          {/* Action Button - Only Add to Cart */}
          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={handleAddToCart}
            disabled={product.stock_quantity === 0}
            className={`w-full py-3 px-4 rounded-xl font-semibold transition-all duration-300 flex items-center justify-center gap-2 ${
              product.stock_quantity > 0
                ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white hover:from-blue-700 hover:to-purple-700 shadow-lg hover:shadow-xl'
                : 'bg-gray-300 text-gray-500 cursor-not-allowed'
            }`}
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 3h2l.4 2M7 13h10l4-8H5.4m1.6 8L6 5H5M7 13l-2.293 2.293c-.63.63-.184 1.707.707 1.707H17M17 13v6a2 2 0 01-2 2H9a2 2 0 01-2-2v-6m8 0V9a2 2 0 00-2-2H9a2 2 0 00-2 2v4.01" />
            </svg>
            {product.stock_quantity > 0 ? 'Add to Cart' : 'Out of Stock'}
          </motion.button>
        </div>
      </motion.div>
    </Link>
  );
};

export default ProductCard;