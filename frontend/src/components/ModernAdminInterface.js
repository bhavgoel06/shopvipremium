import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { toast } from 'react-toastify';

const ModernAdminInterface = () => {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [products, setProducts] = useState([]);
  const [stockOverview, setStockOverview] = useState({
    total_products: 0,
    in_stock: 0,
    out_of_stock: 0,
    total_stock_units: 0
  });
  const [lowStockProducts, setLowStockProducts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');

  const API_URL = process.env.REACT_APP_BACKEND_URL;

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      await Promise.all([
        fetchProducts(),
        fetchStockOverview(),
        fetchLowStockProducts()
      ]);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchProducts = async () => {
    try {
      const response = await fetch(`${API_URL}/api/products?per_page=100`);
      const data = await response.json();
      if (data.success) {
        setProducts(data.data);
      }
    } catch (error) {
      console.error('Error fetching products:', error);
    }
  };

  const fetchStockOverview = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${API_URL}/api/admin/stock/overview`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      const data = await response.json();
      if (data.success) {
        setStockOverview(data.data);
      }
    } catch (error) {
      console.error('Error fetching stock overview:', error);
    }
  };

  const fetchLowStockProducts = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${API_URL}/api/admin/stock/low-stock`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      const data = await response.json();
      if (data.success) {
        setLowStockProducts(data.data);
      }
    } catch (error) {
      console.error('Error fetching low stock products:', error);
    }
  };

  const handleSetAllOutOfStock = async () => {
    if (!window.confirm('Are you sure you want to set ALL products to OUT OF STOCK? This action cannot be undone.')) {
      return;
    }

    setLoading(true);
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${API_URL}/api/admin/stock/set-all-out-of-stock`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      const data = await response.json();
      
      if (data.success) {
        toast.success(`Successfully set ${data.data.updated_count} products to out of stock`);
        await fetchData();
      } else {
        toast.error('Failed to update products');
      }
    } catch (error) {
      console.error('Error setting all out of stock:', error);
      toast.error('Error setting products to out of stock');
    } finally {
      setLoading(false);
    }
  };

  const handleSetAllInStock = async () => {
    const defaultStock = prompt('Enter default stock quantity for all products:', '100');
    if (!defaultStock || isNaN(defaultStock)) {
      toast.error('Invalid stock quantity');
      return;
    }

    setLoading(true);
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${API_URL}/api/admin/stock/set-all-in-stock?default_stock=${defaultStock}`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      const data = await response.json();
      
      if (data.success) {
        toast.success(`Successfully set ${data.data.updated_count} products to in stock with ${defaultStock} units`);
        await fetchData();
      } else {
        toast.error('Failed to update products');
      }
    } catch (error) {
      console.error('Error setting all in stock:', error);
      toast.error('Error setting products to in stock');
    } finally {
      setLoading(false);
    }
  };

  const handleSetProductStock = async (productId, currentStock) => {
    const newStock = prompt(`Enter new stock quantity for this product:`, currentStock.toString());
    if (newStock === null || isNaN(newStock)) {
      return;
    }

    setLoading(true);
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${API_URL}/api/admin/stock/set-product-stock`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          product_id: productId,
          stock_quantity: parseInt(newStock)
        })
      });
      const data = await response.json();
      
      if (data.success) {
        toast.success('Stock updated successfully');
        await fetchData();
      } else {
        toast.error('Failed to update stock');
      }
    } catch (error) {
      console.error('Error updating stock:', error);
      toast.error('Error updating stock');
    } finally {
      setLoading(false);
    }
  };

  const filteredProducts = products.filter(product => {
    const matchesSearch = product.name.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCategory = selectedCategory === 'all' || product.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  const categories = [...new Set(products.map(p => p.category))];

  const TabButton = ({ tab, label, icon }) => (
    <motion.button
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      onClick={() => setActiveTab(tab)}
      className={`flex items-center gap-2 px-6 py-3 rounded-lg font-semibold transition-all ${
        activeTab === tab
          ? 'bg-blue-600 text-white shadow-lg'
          : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
      }`}
    >
      <span className="text-xl">{icon}</span>
      {label}
    </motion.button>
  );

  const StockCard = ({ title, value, subtitle, color, icon }) => (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className={`bg-gradient-to-r ${color} p-6 rounded-xl text-white shadow-lg`}
    >
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-3xl font-bold">{value}</h3>
          <p className="text-white/80">{title}</p>
          {subtitle && <p className="text-sm text-white/60">{subtitle}</p>}
        </div>
        <div className="text-4xl opacity-80">{icon}</div>
      </div>
    </motion.div>
  );

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent mb-2">
            Admin Dashboard
          </h1>
          <p className="text-gray-400">Manage your premium subscription store</p>
        </div>

        {/* Navigation */}
        <div className="flex gap-4 mb-8 overflow-x-auto pb-2">
          <TabButton tab="dashboard" label="Dashboard" icon="📊" />
          <TabButton tab="stock" label="Stock Management" icon="📦" />
          <TabButton tab="products" label="Products" icon="🛍️" />
          <TabButton tab="orders" label="Orders" icon="📋" />
          <TabButton tab="analytics" label="Analytics" icon="📈" />
        </div>

        {/* Content */}
        <AnimatePresence mode="wait">
          {activeTab === 'dashboard' && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="space-y-6"
            >
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <StockCard
                  title="Total Products"
                  value={stockOverview.total_products}
                  color="from-blue-500 to-blue-600"
                  icon="🛍️"
                />
                <StockCard
                  title="In Stock"
                  value={stockOverview.in_stock}
                  subtitle={`${stockOverview.total_products > 0 ? ((stockOverview.in_stock / stockOverview.total_products) * 100).toFixed(1) : 0}%`}
                  color="from-green-500 to-green-600"
                  icon="✅"
                />
                <StockCard
                  title="Out of Stock"
                  value={stockOverview.out_of_stock}
                  subtitle={`${stockOverview.total_products > 0 ? ((stockOverview.out_of_stock / stockOverview.total_products) * 100).toFixed(1) : 0}%`}
                  color="from-red-500 to-red-600"
                  icon="❌"
                />
                <StockCard
                  title="Total Stock Units"
                  value={stockOverview.total_stock_units}
                  color="from-purple-500 to-purple-600"
                  icon="📦"
                />
              </div>

              {/* Low Stock Alert */}
              {lowStockProducts.length > 0 && (
                <div className="bg-yellow-900/20 border border-yellow-500/50 rounded-xl p-6">
                  <h3 className="text-xl font-bold text-yellow-400 mb-4 flex items-center gap-2">
                    ⚠️ Low Stock Alert
                  </h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {lowStockProducts.map((product) => (
                      <div key={product.id} className="bg-gray-800 rounded-lg p-4">
                        <h4 className="font-semibold text-white mb-2">{product.name}</h4>
                        <p className="text-yellow-400 text-sm mb-2">
                          Only {product.stock_quantity} units left
                        </p>
                        <p className="text-gray-400 text-sm">
                          Category: {product.category}
                        </p>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </motion.div>
          )}

          {activeTab === 'stock' && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="space-y-6"
            >
              {/* Stock Management Controls */}
              <div className="bg-gray-800 rounded-xl p-6">
                <h3 className="text-2xl font-bold mb-6">Stock Management Controls</h3>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={handleSetAllOutOfStock}
                    disabled={loading}
                    className="bg-red-600 hover:bg-red-700 text-white px-6 py-4 rounded-lg font-semibold transition-colors flex items-center justify-center gap-2"
                  >
                    <span className="text-2xl">⚠️</span>
                    Set All Products OUT OF STOCK
                  </motion.button>

                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={handleSetAllInStock}
                    disabled={loading}
                    className="bg-green-600 hover:bg-green-700 text-white px-6 py-4 rounded-lg font-semibold transition-colors flex items-center justify-center gap-2"
                  >
                    <span className="text-2xl">✅</span>
                    Set All Products IN STOCK
                  </motion.button>
                </div>

                <div className="mt-6 p-4 bg-gray-700 rounded-lg">
                  <h4 className="font-semibold mb-2">⚠️ Important Notes:</h4>
                  <ul className="text-sm text-gray-300 space-y-1">
                    <li>• Use "Set All OUT OF STOCK" when you need to prevent new orders immediately</li>
                    <li>• Use "Set All IN STOCK" to restore inventory after resolving issues</li>
                    <li>• You can also manage individual product stock in the Products tab</li>
                    <li>• Changes take effect immediately on the frontend</li>
                  </ul>
                </div>
              </div>

              {/* Stock Overview */}
              <div className="bg-gray-800 rounded-xl p-6">
                <h3 className="text-2xl font-bold mb-6">Current Stock Status</h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                  <div className="text-center">
                    <div className="text-3xl font-bold text-blue-400 mb-2">
                      {stockOverview.total_products}
                    </div>
                    <div className="text-gray-400">Total Products</div>
                  </div>
                  <div className="text-center">
                    <div className="text-3xl font-bold text-green-400 mb-2">
                      {stockOverview.in_stock}
                    </div>
                    <div className="text-gray-400">In Stock</div>
                  </div>
                  <div className="text-center">
                    <div className="text-3xl font-bold text-red-400 mb-2">
                      {stockOverview.out_of_stock}
                    </div>
                    <div className="text-gray-400">Out of Stock</div>
                  </div>
                </div>
              </div>
            </motion.div>
          )}

          {activeTab === 'products' && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="space-y-6"
            >
              {/* Filters */}
              <div className="bg-gray-800 rounded-xl p-6">
                <div className="flex flex-col md:flex-row gap-4">
                  <div className="flex-1">
                    <input
                      type="text"
                      placeholder="Search products..."
                      value={searchTerm}
                      onChange={(e) => setSearchTerm(e.target.value)}
                      className="w-full bg-gray-700 text-white px-4 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                  </div>
                  <select
                    value={selectedCategory}
                    onChange={(e) => setSelectedCategory(e.target.value)}
                    className="bg-gray-700 text-white px-4 py-2 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="all">All Categories</option>
                    {categories.map(cat => (
                      <option key={cat} value={cat}>{cat}</option>
                    ))}
                  </select>
                </div>
              </div>

              {/* Products List */}
              <div className="bg-gray-800 rounded-xl p-6">
                <h3 className="text-2xl font-bold mb-6">Products ({filteredProducts.length})</h3>
                
                <div className="overflow-x-auto">
                  <table className="w-full text-left">
                    <thead>
                      <tr className="border-b border-gray-700">
                        <th className="pb-3 text-gray-400">Product</th>
                        <th className="pb-3 text-gray-400">Category</th>
                        <th className="pb-3 text-gray-400">Price</th>
                        <th className="pb-3 text-gray-400">Stock</th>
                        <th className="pb-3 text-gray-400">Status</th>
                        <th className="pb-3 text-gray-400">Actions</th>
                      </tr>
                    </thead>
                    <tbody>
                      {filteredProducts.map((product) => (
                        <tr key={product.id} className="border-b border-gray-700/50">
                          <td className="py-4">
                            <div className="flex items-center gap-3">
                              <img
                                src={product.image_url}
                                alt={product.name}
                                className="w-12 h-12 rounded-lg object-cover"
                                onError={(e) => {
                                  e.target.src = `https://via.placeholder.com/48x48/4F46E5/FFFFFF?text=${product.name.charAt(0)}`;
                                }}
                              />
                              <div>
                                <div className="font-semibold">{product.name}</div>
                                <div className="text-sm text-gray-400">{product.short_description}</div>
                              </div>
                            </div>
                          </td>
                          <td className="py-4">
                            <span className="bg-gray-700 text-gray-300 px-2 py-1 rounded text-sm">
                              {product.category}
                            </span>
                          </td>
                          <td className="py-4">
                            <div className="font-semibold">₹{product.discounted_price}</div>
                            {product.original_price > product.discounted_price && (
                              <div className="text-sm text-gray-400 line-through">
                                ₹{product.original_price}
                              </div>
                            )}
                          </td>
                          <td className="py-4">
                            <div className={`font-semibold ${product.stock_quantity > 0 ? 'text-green-400' : 'text-red-400'}`}>
                              {product.stock_quantity} units
                            </div>
                          </td>
                          <td className="py-4">
                            <span className={`px-2 py-1 rounded text-sm ${
                              product.stock_quantity > 0 
                                ? 'bg-green-900 text-green-300' 
                                : 'bg-red-900 text-red-300'
                            }`}>
                              {product.stock_quantity > 0 ? 'In Stock' : 'Out of Stock'}
                            </span>
                          </td>
                          <td className="py-4">
                            <motion.button
                              whileHover={{ scale: 1.05 }}
                              whileTap={{ scale: 0.95 }}
                              onClick={() => handleSetProductStock(product.id, product.stock_quantity)}
                              className="bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 rounded text-sm font-semibold transition-colors"
                            >
                              Update Stock
                            </motion.button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </motion.div>
          )}

          {activeTab === 'orders' && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="bg-gray-800 rounded-xl p-6"
            >
              <h3 className="text-2xl font-bold mb-6">Orders Management</h3>
              <p className="text-gray-400">Order management features coming soon...</p>
            </motion.div>
          )}

          {activeTab === 'analytics' && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              className="bg-gray-800 rounded-xl p-6"
            >
              <h3 className="text-2xl font-bold mb-6">Analytics & Reports</h3>
              <p className="text-gray-400">Analytics dashboard coming soon...</p>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Loading Overlay */}
        {loading && (
          <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
            <div className="bg-gray-800 rounded-lg p-6 flex items-center gap-3">
              <div className="w-6 h-6 border-2 border-blue-400 border-t-transparent rounded-full animate-spin"></div>
              <span className="text-white">Processing...</span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ModernAdminInterface;