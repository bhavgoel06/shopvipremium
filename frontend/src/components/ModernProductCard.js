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
  
  const getProductImage = () => {
    if (product.image_url && product.image_url !== 'https://via.placeholder.com/300x200') {
      return product.image_url;
    }
    
    // Use product name to get better placeholder
    const productName = product.name.toLowerCase();
    if (productName.includes('netflix')) return 'https://logos-world.net/wp-content/uploads/2020/04/Netflix-Logo.png';
    if (productName.includes('spotify')) return 'https://logos-world.net/wp-content/uploads/2020/06/Spotify-Logo.png';
    if (productName.includes('amazon')) return 'https://logos-world.net/wp-content/uploads/2020/04/Amazon-Logo.png';
    if (productName.includes('disney')) return 'https://logos-world.net/wp-content/uploads/2020/11/Disney-Logo.png';
    if (productName.includes('youtube')) return 'https://logos-world.net/wp-content/uploads/2020/04/YouTube-Logo.png';
    if (productName.includes('office')) return 'https://logos-world.net/wp-content/uploads/2020/09/Microsoft-Office-Logo.png';
    if (productName.includes('canva')) return 'https://logos-world.net/wp-content/uploads/2021/08/Canva-Logo.png';
    if (productName.includes('chatgpt')) return 'https://logos-world.net/wp-content/uploads/2023/02/ChatGPT-Logo.png';
    if (productName.includes('onlyfans')) return 'https://logos-world.net/wp-content/uploads/2021/04/OnlyFans-Logo.png';
    if (productName.includes('hbo')) return 'https://logos-world.net/wp-content/uploads/2022/01/HBO-Max-Logo.png';
    if (productName.includes('hulu')) return 'https://logos-world.net/wp-content/uploads/2020/05/Hulu-Logo.png';
    if (productName.includes('coursera')) return 'https://logos-world.net/wp-content/uploads/2021/11/Coursera-Logo.png';
    if (productName.includes('udemy')) return 'https://logos-world.net/wp-content/uploads/2020/11/Udemy-Logo.png';
    if (productName.includes('linkedin')) return 'https://logos-world.net/wp-content/uploads/2020/04/LinkedIn-Logo.png';
    
    return `https://via.placeholder.com/300x200?text=${encodeURIComponent(product.name)}`;
  };
  
  return (
    <div 
      className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300 cursor-pointer relative overflow-hidden"
      onClick={handleCardClick}
    >
      {/* Badges */}
      <div className="absolute top-2 left-2 z-10 flex flex-col gap-1">
        {product.discount_percentage > 0 && (
          <span className="bg-red-500 text-white px-2 py-1 rounded text-xs font-medium">
            -{product.discount_percentage}%
          </span>
        )}
        {product.is_bestseller && (
          <span className="bg-orange-500 text-white px-2 py-1 rounded text-xs font-medium">
            Bestseller
          </span>
        )}
      </div>
      
      {/* Stock status */}
      <div className="absolute top-2 right-2 z-10">
        {product.stock_quantity > 0 ? (
          <span className="bg-green-500 text-white px-2 py-1 rounded text-xs font-medium">
            In Stock
          </span>
        ) : (
          <span className="bg-red-500 text-white px-2 py-1 rounded text-xs font-medium">
            Out of stock
          </span>
        )}
      </div>
      
      {/* Product Image */}
      <div className="w-full h-48 bg-gray-100 flex items-center justify-center overflow-hidden">
        <img
          src={getProductImage()}
          alt={product.name}
          className={`w-full h-full object-contain transition-opacity duration-300 ${
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
            <div className="animate-pulse bg-gray-200 w-full h-full"></div>
          </div>
        )}
      </div>
      
      {/* Product Info */}
      <div className="p-4">
        <h3 className="text-lg font-semibold text-gray-800 mb-2 line-clamp-2 min-h-[3rem]">
          {product.name}
        </h3>
        
        {/* Rating */}
        <div className="flex items-center mb-2">
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
            ({product.total_reviews})
          </span>
        </div>
        
        {/* Price */}
        <div className="flex items-center mb-4">
          <span className="text-2xl font-bold text-gray-900">
            {currency === 'USD' ? '$' : '₹'}{currency === 'USD' ? convertedDiscountedPrice.toFixed(2) : Math.round(convertedDiscountedPrice)}
          </span>
          {product.discount_percentage > 0 && (
            <span className="text-lg text-gray-500 line-through ml-2">
              {currency === 'USD' ? '$' : '₹'}{currency === 'USD' ? convertedOriginalPrice.toFixed(2) : Math.round(convertedOriginalPrice)}
            </span>
          )}
        </div>
        
        {/* Categories */}
        <div className="text-xs text-gray-500 mb-3">
          {product.category.charAt(0).toUpperCase() + product.category.slice(1)} • 
          {product.duration_options && product.duration_options.length > 0 
            ? ` ${product.duration_options[0]}` 
            : ' Multiple Options'}
        </div>
        
        {/* Add to Cart Button */}
        <button
          onClick={handleAddToCart}
          disabled={product.stock_quantity <= 0}
          className={`w-full py-3 px-4 rounded-lg font-medium transition-colors duration-200 ${
            product.stock_quantity > 0
              ? 'bg-blue-600 text-white hover:bg-blue-700 focus:ring-2 focus:ring-blue-500'
              : 'bg-gray-400 text-gray-600 cursor-not-allowed'
          }`}
        >
          {product.stock_quantity > 0 ? 'Add to Cart' : 'Out of Stock'}
        </button>
      </div>
    </div>
  );
};

export default ModernProductCard;