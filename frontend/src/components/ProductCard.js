import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { useCart } from '../context/CartContext';
import { useCurrency } from '../context/CurrencyContext';
import { toast } from 'react-toastify';

const ProductCard = ({ product, className = '' }) => {
  const { addToCart } = useCart();
  const { formatPrice } = useCurrency();

  const handleAddToCart = (e) => {
    e.preventDefault();
    e.stopPropagation();
    
    const defaultDuration = product.duration_options[0];
    addToCart(product, defaultDuration);
    toast.success(`${product.name} added to cart!`);
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
        <span key={`empty-${i}`} className="text-gray-500 text-sm">★</span>
      );
    }
    
    return stars;
  };

  return (
    <motion.div
      whileHover={{ y: -8, scale: 1.02 }}
      transition={{ duration: 0.3 }}
      className={`bg-gray-800 border border-gray-700 rounded-2xl overflow-hidden hover:border-gray-600 transition-all duration-300 ${className}`}
    >
      <Link to={`/products/${product.slug}`}>
        <div className="relative group">
          <div className="aspect-w-16 aspect-h-9 bg-gray-700 rounded-t-2xl overflow-hidden">
            <img
              src={product.image_url}
              alt={product.name}
              className="w-full h-48 object-cover group-hover:scale-105 transition-transform duration-300"
              onError={(e) => {
                e.target.src = `https://via.placeholder.com/400x300/4F46E5/FFFFFF?text=${encodeURIComponent(product.name)}`;
              }}
            />
          </div>
          
          {/* Badges */}
          <div className="absolute top-3 left-3 flex flex-col gap-1">
            {product.is_bestseller && (
              <span className="bg-red-500 text-white px-2 py-1 rounded-full text-xs font-semibold">
                🔥 Best Seller
              </span>
            )}
            {product.is_featured && (
              <span className="bg-blue-500 text-white px-2 py-1 rounded-full text-xs font-semibold">
                ⭐ Featured
              </span>
            )}
            {product.discount_percentage > 0 && (
              <span className="bg-green-500 text-white px-2 py-1 rounded-full text-xs font-semibold">
                -{product.discount_percentage}% OFF
              </span>
            )}
          </div>

          {/* Overlay */}
          <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-20 transition-all duration-300 rounded-t-2xl" />
        </div>
      </Link>

      <div className="p-6">
        <Link to={`/products/${product.slug}`}>
          <h3 className="font-bold text-white mb-2 text-lg hover:text-blue-400 transition-colors line-clamp-2">
            {product.name}
          </h3>
        </Link>
        
        <p className="text-gray-400 mb-4 text-sm line-clamp-2">
          {product.short_description}
        </p>

        {/* Rating */}
        <div className="flex items-center mb-4">
          <div className="flex items-center">
            {renderStars(product.rating)}
          </div>
          <span className="text-sm text-gray-500 ml-2">
            ({product.total_reviews})
          </span>
        </div>

        {/* Price */}
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <span className="text-2xl font-bold text-white">
              {formatPrice(product.discounted_price)}
            </span>
            {product.original_price > product.discounted_price && (
              <span className="text-sm text-gray-500 line-through">
                {formatPrice(product.original_price)}
              </span>
            )}
          </div>
          <span className="text-sm text-green-400 font-semibold">
            Save {formatPrice(product.original_price - product.discounted_price)}
          </span>
        </div>

        {/* Features */}
        <div className="mb-4">
          <div className="flex flex-wrap gap-1">
            {product.features.slice(0, 2).map((feature, index) => (
              <span key={index} className="bg-gray-700 text-gray-300 px-2 py-1 rounded-full text-xs">
                {feature}
              </span>
            ))}
            {product.features.length > 2 && (
              <span className="bg-gray-700 text-gray-300 px-2 py-1 rounded-full text-xs">
                +{product.features.length - 2} more
              </span>
            )}
          </div>
        </div>

        {/* Stock Status */}
        <div className="mb-4">
          {product.stock_quantity > 0 ? (
            <span className="text-green-400 text-sm flex items-center">
              <span className="w-2 h-2 bg-green-400 rounded-full mr-2" />
              In Stock ({product.stock_quantity} available)
            </span>
          ) : (
            <span className="text-red-400 text-sm flex items-center">
              <span className="w-2 h-2 bg-red-400 rounded-full mr-2" />
              Out of Stock
            </span>
          )}
        </div>

        {/* Actions */}
        <div className="flex gap-2">
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={handleAddToCart}
            disabled={product.stock_quantity === 0}
            className={`flex-1 py-3 px-4 rounded-xl font-semibold transition-all duration-300 ${
              product.stock_quantity > 0
                ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white hover:from-blue-700 hover:to-purple-700'
                : 'bg-gray-600 text-gray-400 cursor-not-allowed'
            }`}
          >
            {product.stock_quantity > 0 ? '🛒 Add to Cart' : 'Out of Stock'}
          </motion.button>
          <Link
            to={`/products/${product.slug}`}
            className="px-4 py-3 border border-gray-600 rounded-xl text-gray-300 hover:bg-gray-700 hover:text-white transition-all duration-300"
          >
            👁️
          </Link>
        </div>
      </div>
    </motion.div>
  );
};

export default ProductCard;