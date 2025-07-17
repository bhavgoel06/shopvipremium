import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useCurrency } from '../context/CurrencyContext';

const ModernProductCard = ({ product }) => {
  const navigate = useNavigate();
  const { currency, convertPrice } = useCurrency();
  const [imageLoaded, setImageLoaded] = useState(false);
  
  const convertedOriginalPrice = convertPrice(product.original_price);
  const convertedDiscountedPrice = convertPrice(product.discounted_price);
  
  const handleCardClick = () => {
    navigate(`/products/${product.slug}`);
  };
  
  const handleAddToCart = (e) => {
    e.stopPropagation();
    // Add to cart logic here
    console.log('Added to cart:', product.name);
  };
  
  return (
    <div 
      className="bg-white rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 cursor-pointer relative overflow-hidden group"
      onClick={handleCardClick}
    >
      {/* Gradient overlay */}
      <div className="absolute inset-0 bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
      
      {/* Badges */}
      <div className="absolute top-3 left-3 z-10 flex flex-col gap-2">
        {product.discount_percentage > 0 && (
          <span className="bg-gradient-to-r from-red-500 to-red-600 text-white px-3 py-1 rounded-full text-xs font-semibold shadow-lg">
            {product.discount_percentage}% OFF
          </span>
        )}
        {product.is_bestseller && (
          <span className="bg-gradient-to-r from-orange-500 to-orange-600 text-white px-3 py-1 rounded-full text-xs font-semibold shadow-lg">
            🔥 Bestseller
          </span>
        )}
        {product.is_featured && (
          <span className="bg-gradient-to-r from-purple-500 to-purple-600 text-white px-3 py-1 rounded-full text-xs font-semibold shadow-lg">
            ⭐ Featured
          </span>
        )}
      </div>
      
      {/* Product Image */}
      <div className="relative w-full h-48 bg-gradient-to-br from-gray-100 to-gray-200 flex items-center justify-center overflow-hidden">
        <img
          src={product.image_url || `https://via.placeholder.com/300x200?text=${encodeURIComponent(product.name)}`}
          alt={product.name}
          className={`w-full h-full object-cover transition-all duration-300 group-hover:scale-105 ${
            imageLoaded ? 'opacity-100' : 'opacity-0'
          }`}
          onLoad={() => setImageLoaded(true)}
          onError={(e) => {
            e.target.src = `https://via.placeholder.com/300x200?text=${encodeURIComponent(product.name)}`;
            setImageLoaded(true);
          }}
        />
        {!imageLoaded && (
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="animate-pulse bg-gradient-to-r from-gray-200 via-gray-300 to-gray-200 w-full h-full"></div>
          </div>
        )}
        
        {/* Stock status overlay */}
        {product.stock_quantity <= 0 && (
          <div className="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center">
            <span className="text-white font-bold text-lg">Out of Stock</span>
          </div>
        )}
      </div>
      
      {/* Product Info */}
      <div className="relative p-6">
        <h3 className="text-xl font-bold text-gray-800 mb-2 line-clamp-2 min-h-[3rem] group-hover:text-blue-600 transition-colors">
          {product.name}
        </h3>
        
        <p className="text-gray-600 text-sm mb-3 line-clamp-2">
          {product.short_description}
        </p>
        
        {/* Rating */}
        <div className="flex items-center mb-4">
          <div className="flex items-center">
            {[...Array(5)].map((_, i) => (
              <svg
                key={i}
                className={`w-4 h-4 ${
                  i < Math.floor(product.rating) ? 'text-yellow-400' : 'text-gray-300'
                }`}
                fill="currentColor"
                viewBox="0 0 20 20"
              >
                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
              </svg>
            ))}
          </div>
          <span className="text-sm text-gray-600 ml-2">
            {product.rating} ({product.total_reviews} reviews)
          </span>
        </div>
        
        {/* Price */}
        <div className="flex items-center mb-4">
          <span className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            {currency === 'USD' ? '$' : '₹'}{convertedDiscountedPrice}
          </span>
          {product.discount_percentage > 0 && (
            <span className="text-lg text-gray-500 line-through ml-3">
              {currency === 'USD' ? '$' : '₹'}{convertedOriginalPrice}
            </span>
          )}
        </div>
        
        {/* Categories */}
        <div className="flex flex-wrap gap-1 mb-4">
          <span className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full">
            {product.category.charAt(0).toUpperCase() + product.category.slice(1)}
          </span>
          {product.duration_options && product.duration_options.length > 0 && (
            <span className="px-2 py-1 bg-green-100 text-green-800 text-xs rounded-full">
              {product.duration_options[0]}
            </span>
          )}
        </div>
        
        {/* Add to Cart Button */}
        <button
          onClick={handleAddToCart}
          disabled={product.stock_quantity <= 0}
          className={`w-full py-3 px-6 rounded-xl font-semibold transition-all duration-200 transform hover:scale-105 ${
            product.stock_quantity > 0
              ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white hover:from-blue-700 hover:to-purple-700 shadow-lg hover:shadow-xl'
              : 'bg-gray-400 text-gray-600 cursor-not-allowed'
          }`}
        >
          {product.stock_quantity > 0 ? '🛒 Add to Cart' : 'Out of Stock'}
        </button>
      </div>
    </div>
  );
};

export default ModernProductCard;