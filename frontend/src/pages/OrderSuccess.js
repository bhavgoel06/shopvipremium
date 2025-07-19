import React, { useState, useEffect } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import { 
  CheckCircleIcon, 
  ClockIcon, 
  CreditCardIcon,
  ShieldCheckIcon, 
  TruckIcon, 
  EnvelopeIcon,
  ExclamationTriangleIcon
} from '@heroicons/react/24/solid';

const OrderSuccess = () => {
  const [searchParams] = useSearchParams();
  const [orderStatus, setOrderStatus] = useState(null);
  const [loading, setLoading] = useState(true);
  const [statusPolling, setStatusPolling] = useState(null);
  
  const orderId = searchParams.get('order_id');
  const paymentId = searchParams.get('payment_id');
  const nowpaymentsId = searchParams.get('NP_id'); // NOWPayments payment ID
  
  useEffect(() => {
    if (orderId) {
      fetchOrderStatus();
      startStatusPolling();
    } else if (nowpaymentsId) {
      // NOWPayments successful redirect - show immediate success
      showNowPaymentsSuccess();
    } else {
      // No parameters - show error
      setLoading(false);
    }
  }, [orderId, nowpaymentsId]);

  const showNowPaymentsSuccess = () => {
    // NOWPayments redirected here, meaning payment was successful
    setOrderStatus({
      order_id: nowpaymentsId,
      order_status: 'confirmed',
      payment_status: 'finished',
      status_message: '🎉 Payment Successful! Order Confirmed',
      order_details: {
        total_amount: 'Paid',
        currency: 'Crypto',
        payment_method: 'cryptocurrency',
        items: [{ 
          product_name: 'Premium Subscription Purchase', 
          duration: 'As Selected', 
          quantity: 1, 
          total_price: 'Paid Successfully' 
        }]
      },
      payment_details: {
        nowpayments_id: nowpaymentsId,
        payment_method: 'Cryptocurrency'
      },
      created_at: new Date().toISOString()
    });
    
    // Clear cart since payment was successful
    if (typeof window !== 'undefined' && window.localStorage) {
      localStorage.removeItem('cart');
      // Dispatch storage event to update other components
      window.dispatchEvent(new Event('storage'));
    }
    
    setLoading(false);
  };

  const startStatusPolling = () => {
    // Start polling for status updates every 10 seconds
    const interval = setInterval(fetchOrderStatus, 10000);
    setStatusPolling(interval);
    
    // Clean up polling on unmount
    return () => {
      if (interval) clearInterval(interval);
    };
  };

  const fetchOrderStatus = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/orders/${orderId}/status`);
      if (response.ok) {
        const data = await response.json();
        setOrderStatus(data.data);
        
        // Stop polling if order is confirmed or failed
        if (data.data.order_status === 'confirmed' || data.data.order_status === 'failed') {
          if (statusPolling) {
            clearInterval(statusPolling);
            setStatusPolling(null);
          }
        }
      }
    } catch (error) {
      console.error('Error fetching order status:', error);
    } finally {
      setLoading(false);
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'confirmed':
        return <CheckCircleIcon className="w-8 h-8 text-green-500" />;
      case 'confirming':
        return <ClockIcon className="w-8 h-8 text-blue-500 animate-spin" />;
      case 'waiting_payment':
        return <CreditCardIcon className="w-8 h-8 text-yellow-500" />;
      case 'failed':
        return <ExclamationTriangleIcon className="w-8 h-8 text-red-500" />;
      default:
        return <ClockIcon className="w-8 h-8 text-gray-500" />;
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'confirmed':
        return 'bg-green-100 text-green-800';
      case 'confirming':
        return 'bg-blue-100 text-blue-800';
      case 'waiting_payment':
        return 'bg-yellow-100 text-yellow-800';
      case 'failed':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <ClockIcon className="w-12 h-12 text-blue-500 animate-spin mx-auto mb-4" />
          <p className="text-gray-600">Loading order details...</p>
        </div>
      </div>
    );
  }

  if (!orderStatus) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <ExclamationTriangleIcon className="w-12 h-12 text-red-500 mx-auto mb-4" />
          <h2 className="text-xl font-semibold text-gray-800 mb-2">Order Not Found</h2>
          <p className="text-gray-600 mb-4">We couldn't find your order details.</p>
          <Link 
            to="/products"
            className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700"
          >
            Continue Shopping
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Status Header */}
        <div className="text-center mb-12">
          <div className="mx-auto flex items-center justify-center h-16 w-16 rounded-full bg-white shadow-lg mb-6">
            {getStatusIcon(orderStatus.order_status)}
          </div>
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            {orderStatus.order_status === 'confirmed' ? 'Order Confirmed!' : 'Order Received!'}
          </h1>
          <p className="text-lg text-gray-600 mb-4">{orderStatus.status_message}</p>
          
          {/* Live Status Badge */}
          <div className="inline-flex items-center space-x-2">
            <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(orderStatus.order_status)}`}>
              {orderStatus.order_status === 'waiting_payment' && '⏳ '}
              {orderStatus.order_status === 'confirming' && '🔄 '}
              {orderStatus.order_status === 'confirmed' && '✅ '}
              {orderStatus.order_status === 'failed' && '❌ '}
              {orderStatus.status_message}
            </span>
            {(orderStatus.order_status === 'waiting_payment' || orderStatus.order_status === 'confirming') && (
              <span className="text-sm text-gray-500">
                (Updates automatically)
              </span>
            )}
          </div>
        </div>

        {/* Order Summary Card */}
        <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
          <div className="border-b border-gray-200 pb-6 mb-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">Order Details</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <span className="text-sm text-gray-500">Order ID:</span>
                <p className="font-medium text-gray-900 font-mono">{orderStatus.order_id}</p>
              </div>
              <div>
                <span className="text-sm text-gray-500">Payment Method:</span>
                <p className="font-medium text-gray-900 capitalize">{orderStatus.order_details.payment_method}</p>
              </div>
              <div>
                <span className="text-sm text-gray-500">Order Date:</span>
                <p className="font-medium text-gray-900">{new Date(orderStatus.created_at).toLocaleString()}</p>
              </div>
              <div>
                <span className="text-sm text-gray-500">Total Amount:</span>
                <p className="font-medium text-gray-900">
                  ₹{orderStatus.order_details.total_amount} ({orderStatus.order_details.currency})
                </p>
              </div>
            </div>
          </div>

          {/* Order Items */}
          {orderStatus.order_details.items && (
            <div className="mb-6">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Items Ordered</h3>
              <div className="space-y-3">
                {orderStatus.order_details.items.map((item, index) => (
                  <div key={index} className="flex justify-between items-center p-4 bg-gray-50 rounded-lg">
                    <div>
                      <h4 className="font-medium text-gray-900">{item.product_name}</h4>
                      <p className="text-sm text-gray-600">Plan: {item.duration}</p>
                      <p className="text-sm text-gray-600">Quantity: {item.quantity}</p>
                    </div>
                    <div className="text-right">
                      <p className="font-medium text-gray-900">₹{item.total_price}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Payment Status Progress */}
          <div className="border-t border-gray-200 pt-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Payment Progress</h3>
            <div className="space-y-3">
              {/* Step 1: Payment Initiated */}
              <div className="flex items-center space-x-3">
                <CheckCircleIcon className="w-5 h-5 text-green-500" />
                <span className="text-sm text-gray-900">Payment initiated</span>
              </div>
              
              {/* Step 2: Waiting/Confirming */}
              <div className="flex items-center space-x-3">
                {orderStatus.order_status === 'waiting_payment' ? (
                  <ClockIcon className="w-5 h-5 text-yellow-500 animate-pulse" />
                ) : orderStatus.order_status === 'confirming' ? (
                  <ClockIcon className="w-5 h-5 text-blue-500 animate-spin" />
                ) : orderStatus.order_status === 'confirmed' ? (
                  <CheckCircleIcon className="w-5 h-5 text-green-500" />
                ) : (
                  <div className="w-5 h-5 border-2 border-gray-300 rounded-full" />
                )}
                <span className={`text-sm ${orderStatus.order_status === 'confirmed' ? 'text-gray-900' : 'text-gray-600'}`}>
                  {orderStatus.order_status === 'waiting_payment' ? 'Waiting for payment confirmation...' :
                   orderStatus.order_status === 'confirming' ? 'Payment being confirmed...' :
                   orderStatus.order_status === 'confirmed' ? 'Payment confirmed' : 'Payment confirmation'}
                </span>
              </div>
              
              {/* Step 3: Order Processing */}
              <div className="flex items-center space-x-3">
                {orderStatus.order_status === 'confirmed' ? (
                  <TruckIcon className="w-5 h-5 text-blue-500" />
                ) : (
                  <div className="w-5 h-5 border-2 border-gray-300 rounded-full" />
                )}
                <span className={`text-sm ${orderStatus.order_status === 'confirmed' ? 'text-gray-900' : 'text-gray-400'}`}>
                  Order processing & delivery
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* What's Next Section */}
        {orderStatus.order_status === 'confirmed' && (
          <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
            <h2 className="text-xl font-semibold text-gray-900 mb-6">What's Next?</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="text-center">
                <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-blue-100 mb-4">
                  <EnvelopeIcon className="h-6 w-6 text-blue-600" />
                </div>
                <h3 className="text-lg font-medium text-gray-900 mb-2">Check Your Email</h3>
                <p className="text-gray-600 text-sm">
                  Login credentials will be sent to your email within 30 minutes
                </p>
              </div>
              <div className="text-center">
                <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-green-100 mb-4">
                  <ShieldCheckIcon className="h-6 w-6 text-green-600" />
                </div>
                <h3 className="text-lg font-medium text-gray-900 mb-2">Instant Activation</h3>
                <p className="text-gray-600 text-sm">
                  Your premium account will be activated immediately upon delivery
                </p>
              </div>
              <div className="text-center">
                <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-purple-100 mb-4">
                  <TruckIcon className="h-6 w-6 text-purple-600" />
                </div>
                <h3 className="text-lg font-medium text-gray-900 mb-2">24/7 Support</h3>
                <p className="text-gray-600 text-sm">
                  Contact us anytime if you need help with your order
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Action Buttons */}
        <div className="text-center space-y-4">
          {orderStatus.order_status === 'failed' && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
              <p className="text-red-800">
                Payment failed. Please try again or contact support if the issue persists.
              </p>
            </div>
          )}
          
          <Link 
            to="/products"
            className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 mr-4"
          >
            Continue Shopping
          </Link>
          
          {orderStatus.order_status === 'confirmed' && (
            <a 
              href="mailto:support@shopforpremium.com"
              className="inline-flex items-center px-6 py-3 border border-gray-300 text-base font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
            >
              Contact Support
            </a>
          )}
        </div>
      </div>
    </div>
  );
};

export default OrderSuccess;