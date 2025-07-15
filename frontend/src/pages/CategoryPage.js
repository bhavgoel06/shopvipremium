import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import ProductCard from '../components/ProductCard';

const CategoryPage = () => {
  const { category } = useParams();
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [categoryInfo, setCategoryInfo] = useState(null);

  useEffect(() => {
    fetchCategoryProducts();
  }, [category]);

  const fetchCategoryProducts = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/products?category=${category}`);
      const data = await response.json();
      
      if (data.success) {
        setProducts(data.data);
      }
    } catch (error) {
      console.error('Error fetching category products:', error);
    } finally {
      setLoading(false);
    }
  };

  const getCategoryInfo = (categorySlug) => {
    const categories = {
      ott: {
        name: 'OTT Platforms',
        description: 'Stream your favorite movies and TV shows with premium OTT subscriptions at discounted prices.',
        icon: '📺',
        color: 'bg-red-500'
      },
      software: {
        name: 'Software & Tools',
        description: 'Professional software and creative tools for designers, developers, and businesses.',
        icon: '💻',
        color: 'bg-blue-500'
      },
      vpn: {
        name: 'VPN & Security',
        description: 'Secure your online privacy and access geo-restricted content with premium VPN services.',
        icon: '🔒',
        color: 'bg-green-500'
      },
      professional: {
        name: 'Professional Development',
        description: 'Advance your career with professional development courses and networking tools.',
        icon: '🎓',
        color: 'bg-purple-500'
      },
      gaming: {
        name: 'Gaming & Entertainment',
        description: 'Gaming platforms, music streaming, and entertainment subscriptions at great prices.',
        icon: '🎮',
        color: 'bg-orange-500'
      }
    };
    
    return categories[categorySlug] || {
      name: 'Category',
      description: 'Discover amazing products in this category.',
      icon: '🏷️',
      color: 'bg-gray-500'
    };
  };

  useEffect(() => {
    setCategoryInfo(getCategoryInfo(category));
  }, [category]);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading products...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Category Header */}
      <div className={`${categoryInfo?.color} text-white py-16`}>
        <div className="container mx-auto px-4">
          <div className="text-center">
            <div className="text-6xl mb-4">{categoryInfo?.icon}</div>
            <h1 className="text-4xl font-bold mb-4">{categoryInfo?.name}</h1>
            <p className="text-xl opacity-90 max-w-2xl mx-auto">
              {categoryInfo?.description}
            </p>
          </div>
        </div>
      </div>

      {/* Products Section */}
      <div className="container mx-auto px-4 py-12">
        <div className="flex justify-between items-center mb-8">
          <h2 className="text-2xl font-bold text-gray-800">
            {products.length} Product{products.length !== 1 ? 's' : ''} Found
          </h2>
        </div>

        {products.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {products.map((product) => (
              <ProductCard key={product.id} product={product} />
            ))}
          </div>
        ) : (
          <div className="text-center py-12">
            <div className="text-gray-400 text-6xl mb-4">📦</div>
            <h3 className="text-xl font-semibold text-gray-800 mb-2">No products found</h3>
            <p className="text-gray-600 mb-6">
              We're working on adding more products to this category. Check back soon!
            </p>
            <a
              href="/products"
              className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors"
            >
              Browse All Products
            </a>
          </div>
        )}
      </div>
    </div>
  );
};

export default CategoryPage;