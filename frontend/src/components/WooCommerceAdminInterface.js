import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

const WooCommerceAdminInterface = () => {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [products, setProducts] = useState([]);
  const [orders, setOrders] = useState([]);
  const [users, setUsers] = useState([]);
  const [dashboardStats, setDashboardStats] = useState({
    totalRevenue: 0,
    totalOrders: 0,
    totalProducts: 0,
    totalUsers: 0,
    recentOrders: []
  });
  const [loading, setLoading] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [editingProduct, setEditingProduct] = useState(null);
  const [newProduct, setNewProduct] = useState({
    name: '',
    description: '',
    category: 'ott',
    original_price: '',
    discounted_price: '',
    stock_quantity: 100,
    image_url: 'https://images.unsplash.com/photo-1557804506-669a67965ba0?w=500&h=300&fit=crop'
  });

  const API_URL = process.env.REACT_APP_BACKEND_URL;

  const adminTabs = [
    { 
      id: 'dashboard', 
      name: 'Dashboard', 
      icon: '📊', 
      description: 'Overview & Analytics',
      color: 'from-blue-500 to-cyan-500'
    },
    { 
      id: 'products', 
      name: 'Products', 
      icon: '📦', 
      description: 'Manage Inventory',
      color: 'from-green-500 to-emerald-500'
    },
    { 
      id: 'orders', 
      name: 'Orders', 
      icon: '🛒', 
      description: 'Order Management',
      color: 'from-purple-500 to-pink-500'
    },
    { 
      id: 'users', 
      name: 'Customers', 
      icon: '👥', 
      description: 'User Management',
      color: 'from-orange-500 to-red-500'
    },
    { 
      id: 'add-product', 
      name: 'Add Product', 
      icon: '➕', 
      description: 'Create New',
      color: 'from-indigo-500 to-purple-500'
    },
    { 
      id: 'settings', 
      name: 'Settings', 
      icon: '⚙️', 
      description: 'System Config',
      color: 'from-gray-500 to-gray-700'
    }
  ];

  useEffect(() => {
    fetchAllData();
  }, []);

  const fetchAllData = async () => {
    setLoading(true);
    try {
      await Promise.all([
        fetchDashboardStats(),
        fetchProducts(),
        fetchOrders(),
        fetchUsers()
      ]);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchDashboardStats = async () => {
    try {
      const response = await fetch(`${API_URL}/api/admin/dashboard-stats`);
      const data = await response.json();
      if (data.success) {
        setDashboardStats(data.data);
      }
    } catch (error) {
      console.error('Error fetching dashboard stats:', error);
    }
  };

  const fetchProducts = async () => {
    try {
      const response = await fetch(`${API_URL}/api/products?per_page=100`);
      const data = await response.json();
      if (data.success) {
        console.log('Products data sample:', data.data[0]); // Debug log
        setProducts(data.data);
      }
    } catch (error) {
      console.error('Error fetching products:', error);
    }
  };

  const fetchOrders = async () => {
    try {
      const response = await fetch(`${API_URL}/api/orders?per_page=50`);
      const data = await response.json();
      if (data.success) {
        setOrders(data.data || []);
      }
    } catch (error) {
      console.error('Error fetching orders:', error);
    }
  };

  const fetchUsers = async () => {
    try {
      const response = await fetch(`${API_URL}/api/users?per_page=50`);
      const data = await response.json();
      if (data.success) {
        setUsers(data.data || []);
      }
    } catch (error) {
      console.error('Error fetching users:', error);
    }
  };

  const handleAddProduct = async (e) => {
    e.preventDefault();
    setLoading(true);
    
    try {
      const productData = {
        name: newProduct.name,
        description: newProduct.description,
        short_description: newProduct.description.substring(0, 100),
        category: newProduct.category,
        original_price: parseFloat(newProduct.original_price),
        discounted_price: parseFloat(newProduct.discounted_price),
        duration_options: ["1 month", "3 months", "6 months", "1 year"],
        features: ["Premium access", "24/7 support", "Instant delivery", "No ads"],
        image_url: newProduct.image_url,
        stock_quantity: parseInt(newProduct.stock_quantity),
        seo_title: `${newProduct.name} - Premium Subscription`,
        seo_description: `Get ${newProduct.name} at discounted price. Premium subscription with instant delivery.`,
        seo_keywords: [newProduct.name.toLowerCase(), "premium", "subscription", newProduct.category]
      };

      const response = await fetch(`${API_URL}/api/admin/products`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(productData),
      });

      if (response.ok) {
        alert('✅ Product added successfully!');
        setNewProduct({
          name: '', description: '', category: 'ott', 
          original_price: '', discounted_price: '', stock_quantity: 100,
          image_url: 'https://images.unsplash.com/photo-1557804506-669a67965ba0?w=500&h=300&fit=crop'
        });
        fetchAllData();
      } else {
        alert('❌ Failed to add product');
      }
    } catch (error) {
      alert('❌ Error adding product');
    } finally {
      setLoading(false);
    }
  };

  const updateProductStock = async (productId, newStock) => {
    try {
      const response = await fetch(`${API_URL}/api/admin/product-stock`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ product_id: productId, stock_quantity: newStock }),
      });
      
      if (response.ok) {
        fetchProducts();
      }
    } catch (error) {
      console.error('Error updating stock:', error);
    }
  };

  const deleteProduct = async (productId) => {
    if (!confirm('⚠️ Are you sure you want to delete this product?')) return;
    
    try {
      const response = await fetch(`${API_URL}/api/admin/product/${productId}`, {
        method: 'DELETE',
      });
      
      if (response.ok) {
        alert('✅ Product deleted successfully!');
        fetchProducts();
        fetchDashboardStats();
      } else {
        alert('❌ Failed to delete product');
      }
    } catch (error) {
      alert('❌ Error deleting product');
    }
  };

  const updateOrderStatus = async (orderId, newStatus) => {
    try {
      const response = await fetch(`${API_URL}/api/admin/order-status`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ order_id: orderId, status: newStatus }),
      });
      
      if (response.ok) {
        fetchOrders();
      }
    } catch (error) {
      console.error('Error updating order status:', error);
    }
  };

  const handleBulkStockUpdate = async (action) => {
    if (!confirm(`⚠️ Are you sure you want to ${action.replace('_', ' ')} for all products?`)) return;
    
    setLoading(true);
    try {
      const response = await fetch(`${API_URL}/api/admin/bulk-stock-update`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action }),
      });
      
      if (response.ok) {
        alert('✅ Bulk update completed!');
        fetchProducts();
      }
    } catch (error) {
      alert('❌ Error in bulk update');
    } finally {
      setLoading(false);
    }
  };

  const formatPrice = (price) => {
    // Ensure price is a number and format as INR
    const numPrice = typeof price === 'string' ? parseFloat(price) : price;
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      maximumFractionDigits: 0, // No decimal places for INR
    }).format(numPrice || 0);
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed': case 'confirmed': return 'bg-green-100 text-green-800';
      case 'processing': return 'bg-blue-100 text-blue-800';
      case 'pending': return 'bg-yellow-100 text-yellow-800';
      case 'cancelled': case 'failed': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const renderDashboard = () => (
    <div className="space-y-6">
      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-gradient-to-r from-emerald-500 to-green-500 rounded-xl p-6 text-white shadow-lg"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-green-100 text-sm font-medium">Total Revenue</p>
              <p className="text-3xl font-bold">{formatPrice(dashboardStats.totalRevenue)}</p>
              <p className="text-green-100 text-xs mt-1">+12% from last month</p>
            </div>
            <div className="text-4xl opacity-80">💰</div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="bg-gradient-to-r from-blue-500 to-cyan-500 rounded-xl p-6 text-white shadow-lg"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-blue-100 text-sm font-medium">Total Orders</p>
              <p className="text-3xl font-bold">{dashboardStats.totalOrders}</p>
              <p className="text-blue-100 text-xs mt-1">+8% from last month</p>
            </div>
            <div className="text-4xl opacity-80">🛒</div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="bg-gradient-to-r from-purple-500 to-pink-500 rounded-xl p-6 text-white shadow-lg"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-purple-100 text-sm font-medium">Products</p>
              <p className="text-3xl font-bold">{dashboardStats.totalProducts}</p>
              <p className="text-purple-100 text-xs mt-1">Across 11 categories</p>
            </div>
            <div className="text-4xl opacity-80">📦</div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="bg-gradient-to-r from-orange-500 to-red-500 rounded-xl p-6 text-white shadow-lg"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-orange-100 text-sm font-medium">Customers</p>
              <p className="text-3xl font-bold">{dashboardStats.totalUsers}</p>
              <p className="text-orange-100 text-xs mt-1">Active users</p>
            </div>
            <div className="text-4xl opacity-80">👥</div>
          </div>
        </motion.div>
      </div>

      {/* Quick Actions */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-xl p-6 shadow-lg">
          <h3 className="text-lg font-semibold mb-4 text-gray-800">Quick Actions</h3>
          <div className="space-y-3">
            <button
              onClick={() => setActiveTab('add-product')}
              className="w-full bg-gradient-to-r from-blue-500 to-blue-600 text-white py-3 rounded-lg hover:from-blue-600 hover:to-blue-700 transition-all font-medium"
            >
              ➕ Add New Product
            </button>
            <button
              onClick={() => handleBulkStockUpdate('reset_all_stock')}
              className="w-full bg-gradient-to-r from-green-500 to-green-600 text-white py-3 rounded-lg hover:from-green-600 hover:to-green-700 transition-all font-medium"
              disabled={loading}
            >
              🔄 Reset All Stock (100 units)
            </button>
            <button
              onClick={() => handleBulkStockUpdate('mark_all_out_of_stock')}
              className="w-full bg-gradient-to-r from-red-500 to-red-600 text-white py-3 rounded-lg hover:from-red-600 hover:to-red-700 transition-all font-medium"
              disabled={loading}
            >
              🚫 Mark All Out of Stock
            </button>
          </div>
        </div>

        <div className="bg-white rounded-xl p-6 shadow-lg">
          <h3 className="text-lg font-semibold mb-4 text-gray-800">Recent Orders</h3>
          <div className="space-y-3 max-h-48 overflow-y-auto">
            {dashboardStats.recentOrders?.slice(0, 5).map((order) => (
              <div key={order.id} className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                <div>
                  <p className="font-medium text-sm">{order.user_name || 'Customer'}</p>
                  <p className="text-xs text-gray-500 font-mono">{order.id}</p>
                </div>
                <div className="text-right">
                  <p className="font-medium text-sm">{formatPrice(order.total_amount)}</p>
                  <span className={`px-2 py-1 text-xs rounded-full ${getStatusColor(order.status)}`}>
                    {order.status}
                  </span>
                </div>
              </div>
            ))}
            {(!dashboardStats.recentOrders || dashboardStats.recentOrders.length === 0) && (
              <p className="text-gray-500 text-center py-4">No recent orders</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );

  const renderProducts = () => (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-800">Product Management</h2>
        <button 
          onClick={() => setActiveTab('add-product')}
          className="bg-gradient-to-r from-blue-500 to-blue-600 text-white px-6 py-3 rounded-lg hover:from-blue-600 hover:to-blue-700 transition-all font-medium shadow-lg"
        >
          ➕ Add New Product
        </button>
      </div>

      {/* Search and Filter */}
      <div className="bg-white p-6 rounded-xl shadow-lg">
        <div className="flex flex-col sm:flex-row gap-4">
          <input
            type="text"
            placeholder="🔍 Search products..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
          <select
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
            className="px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="all">All Categories</option>
            <option value="ott">OTT Platforms</option>
            <option value="software">Software & Tools</option>
            <option value="vpn">VPN & Security</option>
            <option value="adult">Adult Content</option>
            <option value="education">Education</option>
            <option value="gaming">Gaming</option>
          </select>
        </div>
      </div>

      {/* Products Table */}
      <div className="bg-white rounded-xl shadow-lg overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="text-left py-4 px-6 font-semibold text-gray-700">Product</th>
                <th className="text-left py-4 px-6 font-semibold text-gray-700">Category</th>
                <th className="text-left py-4 px-6 font-semibold text-gray-700">Price (₹)</th>
                <th className="text-left py-4 px-6 font-semibold text-gray-700">Stock</th>
                <th className="text-left py-4 px-6 font-semibold text-gray-700">Status</th>
                <th className="text-left py-4 px-6 font-semibold text-gray-700">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {products
                .filter(product => 
                  product.name.toLowerCase().includes(searchTerm.toLowerCase()) &&
                  (selectedCategory === 'all' || product.category === selectedCategory)
                )
                .map((product) => (
                <tr key={product.id} className="hover:bg-gray-50 transition-colors">
                  <td className="py-4 px-6">
                    <div className="flex items-center gap-4">
                      <img 
                        src={product.image_url} 
                        alt={product.name} 
                        className="w-12 h-12 rounded-lg object-cover"
                      />
                      <div>
                        <p className="font-medium text-gray-900">{product.name}</p>
                        <p className="text-sm text-gray-500 max-w-xs truncate">{product.short_description}</p>
                      </div>
                    </div>
                  </td>
                  <td className="py-4 px-6">
                    <span className="px-3 py-1 text-xs font-medium bg-blue-100 text-blue-800 rounded-full capitalize">
                      {product.category.replace('_', ' ')}
                    </span>
                  </td>
                  <td className="py-4 px-6">
                    <div>
                      <p className="font-medium text-green-600">{formatPrice(product.discounted_price)}</p>
                      <p className="text-sm text-gray-500 line-through">{formatPrice(product.original_price)}</p>
                    </div>
                  </td>
                  <td className="py-4 px-6">
                    <input
                      type="number"
                      value={product.stock_quantity}
                      onChange={(e) => updateProductStock(product.id, parseInt(e.target.value))}
                      className="w-20 px-3 py-1 border rounded-lg text-center focus:ring-2 focus:ring-blue-500"
                      min="0"
                    />
                  </td>
                  <td className="py-4 px-6">
                    <span className={`px-3 py-1 text-xs font-medium rounded-full ${
                      product.stock_quantity > 50 ? 'bg-green-100 text-green-800' :
                      product.stock_quantity > 10 ? 'bg-yellow-100 text-yellow-800' :
                      product.stock_quantity > 0 ? 'bg-orange-100 text-orange-800' :
                      'bg-red-100 text-red-800'
                    }`}>
                      {product.stock_quantity > 50 ? 'In Stock' :
                       product.stock_quantity > 10 ? 'Low Stock' :
                       product.stock_quantity > 0 ? 'Very Low' : 'Out of Stock'}
                    </span>
                  </td>
                  <td className="py-4 px-6">
                    <div className="flex gap-2">
                      <button className="text-blue-500 hover:text-blue-700 p-2 hover:bg-blue-50 rounded-lg transition-all">
                        ✏️
                      </button>
                      <button 
                        onClick={() => deleteProduct(product.id)}
                        className="text-red-500 hover:text-red-700 p-2 hover:bg-red-50 rounded-lg transition-all"
                      >
                        🗑️
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );

  const renderOrders = () => (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-gray-800">Order Management</h2>
      
      <div className="bg-white rounded-xl shadow-lg overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="text-left py-4 px-6 font-semibold text-gray-700">Order ID</th>
                <th className="text-left py-4 px-6 font-semibold text-gray-700">Customer</th>
                <th className="text-left py-4 px-6 font-semibold text-gray-700">Amount (₹)</th>
                <th className="text-left py-4 px-6 font-semibold text-gray-700">Status</th>
                <th className="text-left py-4 px-6 font-semibold text-gray-700">Date</th>
                <th className="text-left py-4 px-6 font-semibold text-gray-700">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {orders.map((order) => (
                <tr key={order.id} className="hover:bg-gray-50 transition-colors">
                  <td className="py-4 px-6">
                    <span className="font-mono text-sm bg-gray-100 px-2 py-1 rounded">
                      {order.id}
                    </span>
                  </td>
                  <td className="py-4 px-6">
                    <div>
                      <p className="font-medium text-gray-900">{order.user_name || 'Customer'}</p>
                      <p className="text-sm text-gray-500">{order.user_email}</p>
                    </div>
                  </td>
                  <td className="py-4 px-6">
                    <p className="font-medium text-green-600">{formatPrice(order.total_amount)}</p>
                    <p className="text-xs text-gray-500">INR</p>
                  </td>
                  <td className="py-4 px-6">
                    <select
                      value={order.status}
                      onChange={(e) => updateOrderStatus(order.id, e.target.value)}
                      className={`px-3 py-1 text-sm rounded-lg border focus:ring-2 focus:ring-blue-500 ${getStatusColor(order.status)}`}
                    >
                      <option value="pending">Pending</option>
                      <option value="processing">Processing</option>
                      <option value="confirmed">Confirmed</option>
                      <option value="completed">Completed</option>
                      <option value="cancelled">Cancelled</option>
                    </select>
                  </td>
                  <td className="py-4 px-6">
                    <p className="text-sm text-gray-600">
                      {new Date(order.created_at).toLocaleDateString()}
                    </p>
                  </td>
                  <td className="py-4 px-6">
                    <button className="text-blue-500 hover:text-blue-700 text-sm font-medium hover:bg-blue-50 px-3 py-1 rounded-lg transition-all">
                      View Details
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );

  const renderUsers = () => (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-gray-800">Customer Management</h2>
      
      <div className="bg-white rounded-xl shadow-lg overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="text-left py-4 px-6 font-semibold text-gray-700">Customer</th>
                <th className="text-left py-4 px-6 font-semibold text-gray-700">Email</th>
                <th className="text-left py-4 px-6 font-semibold text-gray-700">Joined</th>
                <th className="text-left py-4 px-6 font-semibold text-gray-700">Status</th>
                <th className="text-left py-4 px-6 font-semibold text-gray-700">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {users.map((user) => (
                <tr key={user.id} className="hover:bg-gray-50 transition-colors">
                  <td className="py-4 px-6">
                    <div className="flex items-center gap-3">
                      <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center text-white font-medium">
                        {user.name?.charAt(0).toUpperCase() || user.email?.charAt(0).toUpperCase()}
                      </div>
                      <div>
                        <p className="font-medium text-gray-900">{user.name || 'User'}</p>
                        <p className="text-sm text-gray-500">Customer #{user.id.slice(0, 8)}</p>
                      </div>
                    </div>
                  </td>
                  <td className="py-4 px-6">
                    <p className="text-gray-900">{user.email}</p>
                  </td>
                  <td className="py-4 px-6">
                    <p className="text-sm text-gray-600">
                      {new Date(user.created_at).toLocaleDateString()}
                    </p>
                  </td>
                  <td className="py-4 px-6">
                    <span className="px-3 py-1 text-xs font-medium bg-green-100 text-green-800 rounded-full">
                      Active
                    </span>
                  </td>
                  <td className="py-4 px-6">
                    <button className="text-blue-500 hover:text-blue-700 text-sm font-medium hover:bg-blue-50 px-3 py-1 rounded-lg transition-all">
                      View Profile
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );

  const renderAddProduct = () => (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-gray-800">Add New Product</h2>
      
      <div className="bg-white rounded-xl shadow-lg p-8">
        <form onSubmit={handleAddProduct} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Product Name *
              </label>
              <input
                type="text"
                value={newProduct.name}
                onChange={(e) => setNewProduct({ ...newProduct, name: e.target.value })}
                required
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="e.g., Netflix Premium 4K UHD"
              />
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Category *
              </label>
              <select
                value={newProduct.category}
                onChange={(e) => setNewProduct({ ...newProduct, category: e.target.value })}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="ott">OTT Platforms</option>
                <option value="software">Software & Tools</option>
                <option value="vpn">VPN & Security</option>
                <option value="adult">Adult Content</option>
                <option value="education">Education</option>
                <option value="gaming">Gaming</option>
                <option value="professional">Professional</option>
                <option value="health">Health & Fitness</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Original Price (₹) *
              </label>
              <input
                type="number"
                value={newProduct.original_price}
                onChange={(e) => setNewProduct({ ...newProduct, original_price: e.target.value })}
                required
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="e.g., 1199"
              />
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Discounted Price (₹) *
              </label>
              <input
                type="number"
                value={newProduct.discounted_price}
                onChange={(e) => setNewProduct({ ...newProduct, discounted_price: e.target.value })}
                required
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="e.g., 799"
              />
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Stock Quantity *
              </label>
              <input
                type="number"
                value={newProduct.stock_quantity}
                onChange={(e) => setNewProduct({ ...newProduct, stock_quantity: e.target.value })}
                required
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="e.g., 100"
              />
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Image URL
              </label>
              <input
                type="url"
                value={newProduct.image_url}
                onChange={(e) => setNewProduct({ ...newProduct, image_url: e.target.value })}
                className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                placeholder="https://images.unsplash.com/..."
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Product Description *
            </label>
            <textarea
              value={newProduct.description}
              onChange={(e) => setNewProduct({ ...newProduct, description: e.target.value })}
              required
              rows={6}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              placeholder="Detailed product description with features and benefits..."
            />
          </div>

          <div className="flex gap-4 pt-6">
            <button
              type="submit"
              disabled={loading}
              className="flex-1 bg-gradient-to-r from-blue-500 to-blue-600 text-white py-4 px-6 rounded-lg font-semibold hover:from-blue-600 hover:to-blue-700 disabled:opacity-50 transition-all shadow-lg"
            >
              {loading ? 'Adding Product...' : '✅ Add Product'}
            </button>
            <button
              type="button"
              onClick={() => setActiveTab('products')}
              className="px-6 py-4 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  );

  const renderSettings = () => (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-gray-800">Settings & Configuration</h2>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Store Settings */}
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h3 className="text-lg font-semibold mb-4 text-gray-800 flex items-center">
            <span className="text-2xl mr-3">🏪</span>
            Store Settings
          </h3>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Store Name</label>
              <input
                type="text"
                defaultValue="Shop For Premium"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Store Description</label>
              <textarea
                defaultValue="Premium digital subscriptions at unbeatable prices"
                rows={3}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Contact Email</label>
              <input
                type="email"
                defaultValue="support@shopforpremium.com"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <button className="w-full bg-blue-500 text-white py-2 rounded-lg hover:bg-blue-600 transition-colors">
              Save Store Settings
            </button>
          </div>
        </div>

        {/* Payment Settings */}
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h3 className="text-lg font-semibold mb-4 text-gray-800 flex items-center">
            <span className="text-2xl mr-3">💳</span>
            Payment Settings
          </h3>
          <div className="space-y-4">
            <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div>
                <p className="font-medium">Nowpayments (Crypto)</p>
                <p className="text-sm text-gray-600">Bitcoin, Ethereum, USDT, etc.</p>
              </div>
              <span className="px-3 py-1 bg-green-100 text-green-800 text-sm rounded-full">Active</span>
            </div>
            <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div>
                <p className="font-medium">UPI Payments</p>
                <p className="text-sm text-gray-600">PhonePe, Google Pay, Paytm</p>
              </div>
              <span className="px-3 py-1 bg-green-100 text-green-800 text-sm rounded-full">Active</span>
            </div>
            <div className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
              <div>
                <p className="font-medium">Card Payments</p>
                <p className="text-sm text-gray-600">Visa, Mastercard, Rupay</p>
              </div>
              <span className="px-3 py-1 bg-green-100 text-green-800 text-sm rounded-full">Active</span>
            </div>
            <button className="w-full bg-purple-500 text-white py-2 rounded-lg hover:bg-purple-600 transition-colors">
              Configure Payment Methods
            </button>
          </div>
        </div>

        {/* Contact & Support */}
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h3 className="text-lg font-semibold mb-4 text-gray-800 flex items-center">
            <span className="text-2xl mr-3">📞</span>
            Contact & Support
          </h3>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">WhatsApp Number</label>
              <input
                type="text"
                defaultValue="+91 9876543210"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Telegram Handle</label>
              <input
                type="text"
                defaultValue="@shopforpremium"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Support Hours</label>
              <input
                type="text"
                defaultValue="24/7 Available"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <button className="w-full bg-green-500 text-white py-2 rounded-lg hover:bg-green-600 transition-colors">
              Update Contact Info
            </button>
          </div>
        </div>

        {/* SEO Settings */}
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h3 className="text-lg font-semibold mb-4 text-gray-800 flex items-center">
            <span className="text-2xl mr-3">🔍</span>
            SEO Settings
          </h3>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Meta Title</label>
              <input
                type="text"
                defaultValue="Shop For Premium - Best Digital Subscriptions"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Meta Description</label>
              <textarea
                defaultValue="Get premium digital subscriptions at unbeatable prices. Netflix, Spotify, Adobe, VPN and more with instant delivery and 24/7 support."
                rows={3}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Keywords</label>
              <input
                type="text"
                defaultValue="premium subscriptions, digital products, netflix, spotify, adobe"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <button className="w-full bg-indigo-500 text-white py-2 rounded-lg hover:bg-indigo-600 transition-colors">
              Update SEO Settings
            </button>
          </div>
        </div>

        {/* Security Settings */}
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h3 className="text-lg font-semibold mb-4 text-gray-800 flex items-center">
            <span className="text-2xl mr-3">🔐</span>
            Security Settings
          </h3>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Admin Password</label>
              <input
                type="password"
                defaultValue="admin123"
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              />
              <p className="text-xs text-gray-500 mt-1">⚠️ Change default password for security</p>
            </div>
            <div className="flex items-center justify-between">
              <div>
                <p className="font-medium">Two-Factor Authentication</p>
                <p className="text-sm text-gray-600">Add extra security to admin login</p>
              </div>
              <label className="relative inline-flex items-center cursor-pointer">
                <input type="checkbox" className="sr-only peer" />
                <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-blue-600"></div>
              </label>
            </div>
            <button className="w-full bg-red-500 text-white py-2 rounded-lg hover:bg-red-600 transition-colors">
              Update Security Settings
            </button>
          </div>
        </div>

        {/* Data Management */}
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h3 className="text-lg font-semibold mb-4 text-gray-800 flex items-center">
            <span className="text-2xl mr-3">📊</span>
            Data Management
          </h3>
          <div className="space-y-4">
            <button className="w-full bg-blue-500 text-white py-3 rounded-lg hover:bg-blue-600 transition-colors">
              📥 Export All Products
            </button>
            <button className="w-full bg-green-500 text-white py-3 rounded-lg hover:bg-green-600 transition-colors">
              📥 Export All Orders
            </button>
            <button className="w-full bg-purple-500 text-white py-3 rounded-lg hover:bg-purple-600 transition-colors">
              📥 Export Customer Data
            </button>
            <button className="w-full bg-orange-500 text-white py-3 rounded-lg hover:bg-orange-600 transition-colors">
              📊 Generate Analytics Report
            </button>
            <hr className="my-4" />
            <button className="w-full bg-red-100 text-red-700 py-3 rounded-lg hover:bg-red-200 transition-colors border border-red-300">
              ⚠️ Backup Database
            </button>
          </div>
        </div>
      </div>

      {/* System Information */}
      <div className="bg-white rounded-xl shadow-lg p-6">
        <h3 className="text-lg font-semibold mb-4 text-gray-800 flex items-center">
          <span className="text-2xl mr-3">ℹ️</span>
          System Information
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="text-center p-4 bg-gray-50 rounded-lg">
            <p className="text-2xl font-bold text-blue-600">{dashboardStats.totalProducts}</p>
            <p className="text-sm text-gray-600">Total Products</p>
          </div>
          <div className="text-center p-4 bg-gray-50 rounded-lg">
            <p className="text-2xl font-bold text-green-600">{dashboardStats.totalOrders}</p>
            <p className="text-sm text-gray-600">Total Orders</p>
          </div>
          <div className="text-center p-4 bg-gray-50 rounded-lg">
            <p className="text-2xl font-bold text-purple-600">{dashboardStats.totalUsers}</p>
            <p className="text-sm text-gray-600">Total Users</p>
          </div>
        </div>
        <div className="mt-4 p-4 bg-blue-50 rounded-lg">
          <p className="text-sm text-gray-700">
            <strong>Platform:</strong> FastAPI + React + MongoDB<br />
            <strong>Version:</strong> 2.0.0<br />
            <strong>Last Updated:</strong> {new Date().toLocaleDateString()}
          </p>
        </div>
      </div>
    </div>
  );

  const renderTab = () => {
    switch (activeTab) {
      case 'dashboard': return renderDashboard();
      case 'products': return renderProducts();
      case 'orders': return renderOrders();
      case 'users': return renderUsers();
      case 'add-product': return renderAddProduct();
      case 'settings': return renderSettings();
      default: return renderDashboard();
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div>
              <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                Shop For Premium Admin
              </h1>
              <p className="text-gray-600 mt-1">Professional E-commerce Management Dashboard</p>
            </div>
            <div className="flex items-center gap-4">
              <button
                onClick={() => fetchAllData()}
                disabled={loading}
                className="flex items-center gap-2 bg-gray-100 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-200 transition-colors"
              >
                <span className={loading ? 'animate-spin' : ''}>🔄</span>
                {loading ? 'Refreshing...' : 'Refresh'}
              </button>
              <button
                onClick={() => window.location.href = '/'}
                className="bg-gradient-to-r from-blue-500 to-blue-600 text-white px-4 py-2 rounded-lg hover:from-blue-600 hover:to-blue-700 transition-all shadow-lg"
              >
                🏠 Back to Store
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex gap-8">
          {/* Sidebar */}
          <div className="w-80 flex-shrink-0">
            <div className="bg-white rounded-xl shadow-lg p-6 sticky top-8">
              <nav className="space-y-2">
                {adminTabs.map((tab) => (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`w-full flex items-center gap-4 px-4 py-4 rounded-xl transition-all duration-200 ${
                      activeTab === tab.id
                        ? `bg-gradient-to-r ${tab.color} text-white shadow-lg transform scale-105`
                        : 'text-gray-700 hover:bg-gray-50 hover:scale-102'
                    }`}
                  >
                    <span className="text-2xl">{tab.icon}</span>
                    <div className="text-left">
                      <p className="font-semibold">{tab.name}</p>
                      <p className="text-xs opacity-75">{tab.description}</p>
                    </div>
                  </button>
                ))}
              </nav>
            </div>
          </div>

          {/* Main Content */}
          <div className="flex-1 min-h-screen">
            <AnimatePresence mode="wait">
              <motion.div
                key={activeTab}
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
                transition={{ duration: 0.2 }}
              >
                {renderTab()}
              </motion.div>
            </AnimatePresence>
          </div>
        </div>
      </div>
    </div>
  );
};

export default WooCommerceAdminInterface;