import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { toast } from 'react-toastify';

const ModernAdminInterface = () => {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [products, setProducts] = useState([]);
  const [orders, setOrders] = useState([]);
  const [users, setUsers] = useState([]);
  const [analytics, setAnalytics] = useState({
    totalRevenue: 0,
    totalOrders: 0,
    totalProducts: 0,
    totalUsers: 0,
    recentOrders: []
  });
  const [stockOverview, setStockOverview] = useState({
    total_products: 0,
    in_stock: 0,
    out_of_stock: 0,
    total_stock_units: 0,
    low_stock_count: 0
  });
  const [lowStockProducts, setLowStockProducts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');

  const API_URL = process.env.REACT_APP_BACKEND_URL;

  // Tab configuration with icons and descriptions
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
      name: 'Users', 
      icon: '👥', 
      description: 'User Management',
      color: 'from-orange-500 to-red-500'
    },
    { 
      id: 'analytics', 
      name: 'Analytics', 
      icon: '📈', 
      description: 'Sales & Reports',
      color: 'from-indigo-500 to-purple-500'
    },
    { 
      id: 'settings', 
      name: 'Settings', 
      icon: '⚙️', 
      description: 'System Settings',
      color: 'from-gray-500 to-gray-700'
    }
  ];

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      await Promise.all([
        fetchProducts(),
        fetchOrders(),
        fetchUsers(),
        fetchStockOverview(),
        fetchLowStockProducts(),
        fetchAnalytics()
      ]);
    } catch (error) {
      console.error('Error fetching data:', error);
      toast.error('Failed to load admin data');
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

  const fetchStockOverview = async () => {
    try {
      const response = await fetch(`${API_URL}/api/admin/stock-overview`);
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
      const response = await fetch(`${API_URL}/api/admin/low-stock-products`);
      const data = await response.json();
      if (data.success) {
        setLowStockProducts(data.data || []);
      }
    } catch (error) {
      console.error('Error fetching low stock products:', error);
    }
  };

  const fetchAnalytics = async () => {
    try {
      const response = await fetch(`${API_URL}/api/admin/analytics`);
      const data = await response.json();
      if (data.success) {
        setAnalytics(data.data);
      }
    } catch (error) {
      console.error('Error fetching analytics:', error);
    }
  };

  const handleBulkStockUpdate = async (action) => {
    setLoading(true);
    try {
      const response = await fetch(`${API_URL}/api/admin/bulk-stock-update`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ action }),
      });
      
      const data = await response.json();
      if (data.success) {
        toast.success(`Bulk ${action} completed successfully!`);
        fetchData();
      } else {
        toast.error('Failed to update stock');
      }
    } catch (error) {
      console.error('Error updating stock:', error);
      toast.error('Failed to update stock');
    } finally {
      setLoading(false);
    }
  };

  const updateProductStock = async (productId, newStock) => {
    try {
      const response = await fetch(`${API_URL}/api/admin/product-stock`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ product_id: productId, stock_quantity: newStock }),
      });
      
      const data = await response.json();
      if (data.success) {
        toast.success('Stock updated successfully!');
        fetchData();
      } else {
        toast.error('Failed to update stock');
      }
    } catch (error) {
      console.error('Error updating stock:', error);
      toast.error('Failed to update stock');
    }
  };

  const deleteProduct = async (productId) => {
    if (!confirm('Are you sure you want to delete this product?')) return;
    
    try {
      const response = await fetch(`${API_URL}/api/admin/product/${productId}`, {
        method: 'DELETE',
      });
      
      const data = await response.json();
      if (data.success) {
        toast.success('Product deleted successfully!');
        fetchData();
      } else {
        toast.error('Failed to delete product');
      }
    } catch (error) {
      console.error('Error deleting product:', error);
      toast.error('Failed to delete product');
    }
  };

  const updateOrderStatus = async (orderId, newStatus) => {
    try {
      const response = await fetch(`${API_URL}/api/admin/order-status`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ order_id: orderId, status: newStatus }),
      });
      
      const data = await response.json();
      if (data.success) {
        toast.success('Order status updated successfully!');
        fetchData();
      } else {
        toast.error('Failed to update order status');
      }
    } catch (error) {
      console.error('Error updating order status:', error);
      toast.error('Failed to update order status');
    }
  };

  const renderDashboard = () => (
    <div className="space-y-6">
      {/* Analytics Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="bg-gradient-to-r from-blue-500 to-cyan-500 rounded-xl p-6 text-white"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-blue-100 text-sm">Total Revenue</p>
              <p className="text-2xl font-bold">${analytics.totalRevenue?.toLocaleString() || 0}</p>
            </div>
            <div className="text-3xl">💰</div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="bg-gradient-to-r from-green-500 to-emerald-500 rounded-xl p-6 text-white"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-green-100 text-sm">Total Orders</p>
              <p className="text-2xl font-bold">{analytics.totalOrders || 0}</p>
            </div>
            <div className="text-3xl">🛒</div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="bg-gradient-to-r from-purple-500 to-pink-500 rounded-xl p-6 text-white"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-purple-100 text-sm">Total Products</p>
              <p className="text-2xl font-bold">{stockOverview.total_products || 0}</p>
            </div>
            <div className="text-3xl">📦</div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          className="bg-gradient-to-r from-orange-500 to-red-500 rounded-xl p-6 text-white"
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-orange-100 text-sm">Total Users</p>
              <p className="text-2xl font-bold">{analytics.totalUsers || 0}</p>
            </div>
            <div className="text-3xl">👥</div>
          </div>
        </motion.div>
      </div>

      {/* Stock Overview */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="bg-white rounded-xl p-6 shadow-lg"
        >
          <h3 className="text-lg font-semibold mb-4 text-gray-800">Stock Overview</h3>
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <span className="text-gray-600">In Stock</span>
              <span className="text-green-600 font-semibold">{stockOverview.in_stock}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Out of Stock</span>
              <span className="text-red-600 font-semibold">{stockOverview.out_of_stock}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Low Stock</span>
              <span className="text-yellow-600 font-semibold">{stockOverview.low_stock_count}</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-gray-600">Total Stock Units</span>
              <span className="text-blue-600 font-semibold">{stockOverview.total_stock_units}</span>
            </div>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          className="bg-white rounded-xl p-6 shadow-lg"
        >
          <h3 className="text-lg font-semibold mb-4 text-gray-800">Quick Actions</h3>
          <div className="space-y-3">
            <button
              onClick={() => handleBulkStockUpdate('mark_all_out_of_stock')}
              disabled={loading}
              className="w-full bg-red-500 text-white py-3 rounded-lg hover:bg-red-600 transition-colors disabled:opacity-50"
            >
              {loading ? 'Processing...' : '🚫 Mark All Out of Stock'}
            </button>
            <button
              onClick={() => handleBulkStockUpdate('reset_all_stock')}
              disabled={loading}
              className="w-full bg-blue-500 text-white py-3 rounded-lg hover:bg-blue-600 transition-colors disabled:opacity-50"
            >
              {loading ? 'Processing...' : '🔄 Reset All Stock'}
            </button>
            <button
              onClick={() => fetchData()}
              disabled={loading}
              className="w-full bg-green-500 text-white py-3 rounded-lg hover:bg-green-600 transition-colors disabled:opacity-50"
            >
              {loading ? 'Refreshing...' : '🔄 Refresh Data'}
            </button>
          </div>
        </motion.div>
      </div>

      {/* Recent Orders */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="bg-white rounded-xl p-6 shadow-lg"
      >
        <h3 className="text-lg font-semibold mb-4 text-gray-800">Recent Orders</h3>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b">
                <th className="text-left py-2">Order ID</th>
                <th className="text-left py-2">Customer</th>
                <th className="text-left py-2">Amount</th>
                <th className="text-left py-2">Status</th>
                <th className="text-left py-2">Date</th>
              </tr>
            </thead>
            <tbody>
              {orders.slice(0, 5).map((order) => (
                <tr key={order.id} className="border-b">
                  <td className="py-2 font-mono text-xs">{order.id}</td>
                  <td className="py-2">{order.user_name}</td>
                  <td className="py-2">${order.total_amount}</td>
                  <td className="py-2">
                    <span className={`px-2 py-1 rounded-full text-xs ${
                      order.status === 'completed' ? 'bg-green-100 text-green-600' :
                      order.status === 'pending' ? 'bg-yellow-100 text-yellow-600' :
                      'bg-red-100 text-red-600'
                    }`}>
                      {order.status}
                    </span>
                  </td>
                  <td className="py-2">{new Date(order.created_at).toLocaleDateString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </motion.div>
    </div>
  );

  const renderProducts = () => (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-800">Product Management</h2>
        <button className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition-colors">
          ➕ Add New Product
        </button>
      </div>

      {/* Search and Filter */}
      <div className="flex gap-4 bg-white p-4 rounded-lg shadow">
        <input
          type="text"
          placeholder="Search products..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
        />
        <select
          value={selectedCategory}
          onChange={(e) => setSelectedCategory(e.target.value)}
          className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
        >
          <option value="all">All Categories</option>
          <option value="ott">OTT</option>
          <option value="software">Software</option>
          <option value="vpn">VPN</option>
          <option value="adult">Adult</option>
        </select>
      </div>

      {/* Products Table */}
      <div className="bg-white rounded-xl shadow-lg overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="text-left py-3 px-4">Product</th>
                <th className="text-left py-3 px-4">Category</th>
                <th className="text-left py-3 px-4">Price</th>
                <th className="text-left py-3 px-4">Stock</th>
                <th className="text-left py-3 px-4">Actions</th>
              </tr>
            </thead>
            <tbody>
              {products
                .filter(product => 
                  product.name.toLowerCase().includes(searchTerm.toLowerCase()) &&
                  (selectedCategory === 'all' || product.category === selectedCategory)
                )
                .map((product) => (
                <tr key={product.id} className="border-b">
                  <td className="py-3 px-4">
                    <div className="flex items-center gap-3">
                      <img 
                        src={product.image_url} 
                        alt={product.name} 
                        className="w-10 h-10 rounded-lg object-cover"
                      />
                      <div>
                        <p className="font-medium">{product.name}</p>
                        <p className="text-sm text-gray-500">{product.short_description}</p>
                      </div>
                    </div>
                  </td>
                  <td className="py-3 px-4">{product.category}</td>
                  <td className="py-3 px-4">${product.discounted_price}</td>
                  <td className="py-3 px-4">
                    <input
                      type="number"
                      value={product.stock_quantity}
                      onChange={(e) => updateProductStock(product.id, parseInt(e.target.value))}
                      className="w-20 px-2 py-1 border rounded text-center"
                      min="0"
                    />
                  </td>
                  <td className="py-3 px-4">
                    <div className="flex gap-2">
                      <button className="text-blue-500 hover:text-blue-700">✏️</button>
                      <button 
                        onClick={() => deleteProduct(product.id)}
                        className="text-red-500 hover:text-red-700"
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
                <th className="text-left py-3 px-4">Order ID</th>
                <th className="text-left py-3 px-4">Customer</th>
                <th className="text-left py-3 px-4">Items</th>
                <th className="text-left py-3 px-4">Amount</th>
                <th className="text-left py-3 px-4">Status</th>
                <th className="text-left py-3 px-4">Date</th>
                <th className="text-left py-3 px-4">Actions</th>
              </tr>
            </thead>
            <tbody>
              {orders.map((order) => (
                <tr key={order.id} className="border-b">
                  <td className="py-3 px-4 font-mono text-xs">{order.id}</td>
                  <td className="py-3 px-4">
                    <div>
                      <p className="font-medium">{order.user_name}</p>
                      <p className="text-sm text-gray-500">{order.user_email}</p>
                    </div>
                  </td>
                  <td className="py-3 px-4">{order.items?.length || 0} items</td>
                  <td className="py-3 px-4">${order.total_amount}</td>
                  <td className="py-3 px-4">
                    <select
                      value={order.status}
                      onChange={(e) => updateOrderStatus(order.id, e.target.value)}
                      className="px-2 py-1 border rounded text-sm"
                    >
                      <option value="pending">Pending</option>
                      <option value="processing">Processing</option>
                      <option value="completed">Completed</option>
                      <option value="cancelled">Cancelled</option>
                    </select>
                  </td>
                  <td className="py-3 px-4">{new Date(order.created_at).toLocaleDateString()}</td>
                  <td className="py-3 px-4">
                    <button className="text-blue-500 hover:text-blue-700 text-sm">
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

  const renderTab = () => {
    switch (activeTab) {
      case 'dashboard':
        return renderDashboard();
      case 'products':
        return renderProducts();
      case 'orders':
        return renderOrders();
      case 'users':
        return <div className="text-center py-12 text-gray-500">User management coming soon...</div>;
      case 'analytics':
        return <div className="text-center py-12 text-gray-500">Advanced analytics coming soon...</div>;
      case 'settings':
        return <div className="text-center py-12 text-gray-500">Settings panel coming soon...</div>;
      default:
        return renderDashboard();
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Shop VIP Premium Admin</h1>
              <p className="text-gray-600">Manage your e-commerce platform</p>
            </div>
            <div className="flex items-center gap-4">
              <span className="text-sm text-gray-500">
                Last updated: {new Date().toLocaleTimeString()}
              </span>
              <button
                onClick={() => window.location.href = '/'}
                className="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600 transition-colors"
              >
                🏠 Back to Site
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex gap-8">
          {/* Sidebar */}
          <div className="w-64 flex-shrink-0">
            <div className="bg-white rounded-xl shadow-lg p-6">
              <nav className="space-y-2">
                {adminTabs.map((tab) => (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id)}
                    className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-all ${
                      activeTab === tab.id
                        ? `bg-gradient-to-r ${tab.color} text-white shadow-lg`
                        : 'text-gray-700 hover:bg-gray-50'
                    }`}
                  >
                    <span className="text-xl">{tab.icon}</span>
                    <div className="text-left">
                      <p className="font-medium">{tab.name}</p>
                      <p className="text-xs opacity-75">{tab.description}</p>
                    </div>
                  </button>
                ))}
              </nav>
            </div>
          </div>

          {/* Main Content */}
          <div className="flex-1">
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

export default ModernAdminInterface;