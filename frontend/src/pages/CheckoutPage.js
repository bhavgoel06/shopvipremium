import React, { useState, useEffect } from 'react';
import { useCart } from '../context/CartContext';
import { useCurrency } from '../context/CurrencyContext';
import { toast } from 'react-toastify';
import { useNavigate } from 'react-router-dom';

const CheckoutPage = () => {
  const { items, getCartTotal, clearCart } = useCart();
  const { currency, convertPrice } = useCurrency();
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    email: '',
    firstName: '',
    lastName: '',
    phone: '',
    paymentMethod: 'card'
  });
  const [loading, setLoading] = useState(false);
  const [cryptoCurrencies, setCryptoCurrencies] = useState([]);
  const [selectedCrypto, setSelectedCrypto] = useState('BTC');
  const [usdTotal, setUsdTotal] = useState(0);

  // Calculate USD total for crypto payments
  useEffect(() => {
    if (formData.paymentMethod === 'crypto') {
      const totalInINR = getCartTotal();
      const usdAmount = totalInINR / 85; // Rough INR to USD conversion
      setUsdTotal(usdAmount);
    }
  }, [formData.paymentMethod, getCartTotal]);

  // Fetch available cryptocurrencies
  useEffect(() => {
    if (formData.paymentMethod === 'crypto') {
      fetchCryptoCurrencies();
    }
  }, [formData.paymentMethod]);

  const fetchCryptoCurrencies = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/payments/crypto/currencies`);
      if (response.ok) {
        const data = await response.json();
        if (data.success) {
          // Set common cryptocurrencies
          setCryptoCurrencies([
            { code: 'BTC', name: 'Bitcoin' },
            { code: 'ETH', name: 'Ethereum' },
            { code: 'USDT', name: 'Tether' },
            { code: 'LTC', name: 'Litecoin' },
            { code: 'XRP', name: 'Ripple' },
            { code: 'ADA', name: 'Cardano' },
            { code: 'DOT', name: 'Polkadot' },
            { code: 'DOGE', name: 'Dogecoin' }
          ]);
        }
      }
    } catch (error) {
      console.error('Error fetching crypto currencies:', error);
      setCryptoCurrencies([
        { code: 'BTC', name: 'Bitcoin' },
        { code: 'ETH', name: 'Ethereum' },
        { code: 'USDT', name: 'Tether' }
      ]);
    }
  };

  const formatPrice = (price) => {
    if (formData.paymentMethod === 'crypto') {
      return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
      }).format(price / 85); // Convert INR to USD
    }
    
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
    }).format(price);
  };

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      // Create order first
      const orderData = {
        user_id: 'guest',
        user_email: formData.email,
        user_name: `${formData.firstName} ${formData.lastName}`,
        user_phone: formData.phone,
        items: items.map(item => ({
          product_id: item.id,
          product_name: item.name,
          duration: item.duration,
          quantity: item.quantity,
          unit_price: item.price,
          total_price: item.price * item.quantity
        })),
        total_amount: getCartTotal(),
        payment_method: formData.paymentMethod,
        currency: formData.paymentMethod === 'crypto' ? 'USD' : 'INR',
        notes: `Payment method: ${formData.paymentMethod}`
      };

      const orderResponse = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/orders`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(orderData)
      });

      if (!orderResponse.ok) {
        throw new Error('Failed to create order');
      }

      const orderResult = await orderResponse.json();
      const orderId = orderResult.data.id;

      // Handle different payment methods
      if (formData.paymentMethod === 'crypto') {
        // Create crypto payment
        const cryptoPaymentData = {
          order_id: orderId,
          crypto_currency: selectedCrypto,
          amount: usdTotal,
          currency: 'USD'
        };

        const cryptoResponse = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/payments/crypto/create`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(cryptoPaymentData)
        });

        if (!cryptoResponse.ok) {
          throw new Error('Failed to create crypto payment');
        }

        const cryptoResult = await cryptoResponse.json();
        
        if (cryptoResult.success) {
          // Clear cart and redirect to payment
          clearCart();
          
          // Redirect to NOWPayments or show payment info
          if (cryptoResult.data.payment_url) {
            window.location.href = cryptoResult.data.payment_url;
          } else {
            // Show payment details
            navigate(`/order-success?order_id=${orderId}&payment_id=${cryptoResult.data.payment_id}`);
          }
        } else {
          throw new Error(cryptoResult.message || 'Failed to process crypto payment');
        }
      } else {
        // Handle card/UPI payments
        toast.success('Order placed successfully!');
        clearCart();
        navigate(`/order-success?order_id=${orderId}`);
      }
    } catch (error) {
      console.error('Error placing order:', error);
      toast.error('Failed to place order. Please try again.');
      navigate(`/order-failed?order_id=${orderId || 'unknown'}&error=${encodeURIComponent(error.message)}`);
    } finally {
      setLoading(false);
    }
  };
        notes: 'Order placed through website'
      };

      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/orders`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(orderData),
      });

      if (response.ok) {
        const result = await response.json();
        toast.success('Order placed successfully! You will receive your subscription details shortly.');
        clearCart();
        // In a real app, redirect to success page or payment gateway
      } else {
        toast.error('Failed to place order. Please try again.');
      }
    } catch (error) {
      toast.error('Failed to place order. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  if (items.length === 0) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="text-gray-400 text-6xl mb-4">🛒</div>
          <h2 className="text-2xl font-bold text-gray-800 mb-2">Your cart is empty</h2>
          <p className="text-gray-600 mb-6">Add some products to your cart to proceed with checkout.</p>
          <a
            href="/products"
            className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors"
          >
            Browse Products
          </a>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          <h1 className="text-3xl font-bold text-gray-800 mb-8">Checkout</h1>
          
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Checkout Form */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-semibold mb-6">Contact Information</h2>
              
              <form onSubmit={handleSubmit} className="space-y-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Email Address *
                  </label>
                  <input
                    type="email"
                    name="email"
                    value={formData.email}
                    onChange={handleInputChange}
                    required
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="your@email.com"
                  />
                  <p className="text-sm text-gray-500 mt-1">We'll send your subscription details to this email</p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      First Name *
                    </label>
                    <input
                      type="text"
                      name="firstName"
                      value={formData.firstName}
                      onChange={handleInputChange}
                      required
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="John"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Last Name *
                    </label>
                    <input
                      type="text"
                      name="lastName"
                      value={formData.lastName}
                      onChange={handleInputChange}
                      required
                      className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="Doe"
                    />
                  </div>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Phone Number *
                  </label>
                  <input
                    type="tel"
                    name="phone"
                    value={formData.phone}
                    onChange={handleInputChange}
                    required
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="+1 (555) 123-4567"
                  />
                  <p className="text-sm text-gray-500 mt-1">We'll send order updates via WhatsApp to this number</p>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Payment Method *
                  </label>
                  <div className="space-y-3">
                    <label className="flex items-center p-3 border border-gray-300 rounded-lg cursor-pointer hover:bg-gray-50">
                      <input
                        type="radio"
                        name="paymentMethod"
                        value="card"
                        checked={formData.paymentMethod === 'card'}
                        onChange={handleInputChange}
                        className="mr-3"
                      />
                      <div className="flex items-center">
                        <div className="text-blue-600 mr-2">
                          <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                            <path d="M4 4a2 2 0 00-2 2v1h16V6a2 2 0 00-2-2H4z"/>
                            <path fillRule="evenodd" d="M18 9H2v5a2 2 0 002 2h12a2 2 0 002-2V9zM4 13a1 1 0 011-1h1a1 1 0 110 2H5a1 1 0 01-1-1zm5-1a1 1 0 100 2h1a1 1 0 100-2H9z" clipRule="evenodd"/>
                          </svg>
                        </div>
                        <span>Credit/Debit Card</span>
                      </div>
                    </label>
                    <label className="flex items-center p-3 border border-gray-300 rounded-lg cursor-pointer hover:bg-gray-50">
                      <input
                        type="radio"
                        name="paymentMethod"
                        value="upi"
                        checked={formData.paymentMethod === 'upi'}
                        onChange={handleInputChange}
                        className="mr-3"
                      />
                      <div className="flex items-center">
                        <div className="text-purple-600 mr-2">
                          <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                            <path d="M2 6a2 2 0 012-2h5l2 2h5a2 2 0 012 2v6a2 2 0 01-2 2H4a2 2 0 01-2-2V6z"/>
                          </svg>
                        </div>
                        <span>UPI Payment</span>
                      </div>
                    </label>
                    <label className="flex items-center p-3 border border-gray-300 rounded-lg cursor-pointer hover:bg-gray-50">
                      <input
                        type="radio"
                        name="paymentMethod"
                        value="crypto"
                        checked={formData.paymentMethod === 'crypto'}
                        onChange={handleInputChange}
                        className="mr-3"
                      />
                      <div className="flex items-center">
                        <div className="text-yellow-500 mr-2">
                          <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                            <path d="M8.433 7.418c.155-.103.346-.196.567-.267v1.698a2.305 2.305 0 01-.567-.267C8.07 8.34 8.070 8.025 8.433 7.418zM11 12.849v-1.698c.22.071.412.164.567.267.364.243.364.558 0 .8-.155.103-.346.196-.567.267z"/>
                            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm-6-8a6 6 0 1112 0 6 6 0 01-12 0z" clipRule="evenodd"/>
                          </svg>
                        </div>
                        <span>Cryptocurrency</span>
                      </div>
                    </label>
                  </div>
                </div>

                <button
                  type="submit"
                  disabled={loading}
                  className="w-full bg-blue-600 text-white py-4 px-6 rounded-lg font-semibold hover:bg-blue-700 transition-colors disabled:opacity-50"
                >
                  {loading ? 'Processing...' : `Complete Order - ${formatPrice(getCartTotal())}`}
                </button>
              </form>
            </div>

            {/* Order Summary */}
            <div className="bg-white rounded-lg shadow-md p-6">
              <h2 className="text-xl font-semibold mb-6">Order Summary</h2>
              
              <div className="space-y-4">
                {items.map((item) => (
                  <div key={`${item.id}-${item.duration}`} className="flex items-start space-x-4 p-4 border rounded-lg">
                    <img
                      src={item.image}
                      alt={item.name}
                      className="w-16 h-16 object-cover rounded"
                    />
                    <div className="flex-1">
                      <h3 className="font-medium">{item.name}</h3>
                      <p className="text-sm text-gray-500">{item.duration}</p>
                      <p className="text-sm text-gray-500">Quantity: {item.quantity}</p>
                    </div>
                    <div className="text-right">
                      <p className="font-medium">{formatPrice(item.price * item.quantity)}</p>
                    </div>
                  </div>
                ))}
              </div>

              <div className="border-t pt-4 mt-6">
                <div className="flex justify-between items-center mb-2">
                  <span className="text-gray-600">Subtotal</span>
                  <span>{formatPrice(getCartTotal())}</span>
                </div>
                <div className="flex justify-between items-center mb-2">
                  <span className="text-gray-600">Discount</span>
                  <span className="text-green-600">-{formatPrice(0)}</span>
                </div>
                <div className="flex justify-between items-center text-lg font-bold border-t pt-2">
                  <span>Total</span>
                  <span>{formatPrice(getCartTotal())}</span>
                </div>
              </div>

              {/* Trust Signals */}
              <div className="mt-6 pt-6 border-t">
                <div className="grid grid-cols-3 gap-4 text-center">
                  <div className="flex flex-col items-center">
                    <div className="text-green-600 mb-1">
                      <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clipRule="evenodd"/>
                      </svg>
                    </div>
                    <span className="text-sm text-gray-600">Secure Payment</span>
                  </div>
                  <div className="flex flex-col items-center">
                    <div className="text-blue-600 mb-1">
                      <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-12a1 1 0 10-2 0v4a1 1 0 00.293.707l2.828 2.829a1 1 0 101.415-1.415L11 9.586V6z" clipRule="evenodd"/>
                      </svg>
                    </div>
                    <span className="text-sm text-gray-600">Instant Delivery</span>
                  </div>
                  <div className="flex flex-col items-center">
                    <div className="text-purple-600 mb-1">
                      <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M2 3a1 1 0 011-1h2.153a1 1 0 01.986.836l.74 4.435a1 1 0 01-.54 1.06l-1.548.773a11.037 11.037 0 006.105 6.105l.774-1.548a1 1 0 011.059-.54l4.435.74a1 1 0 01.836.986V17a1 1 0 01-1 1h-2C7.82 18 2 12.18 2 5V3z"/>
                      </svg>
                    </div>
                    <span className="text-sm text-gray-600">24/7 Support</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CheckoutPage;