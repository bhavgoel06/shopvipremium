import React, { useState, useEffect } from 'react';
import { useCart } from '../context/CartContext';
import { useCurrency } from '../context/CurrencyContext';
import { toast } from 'react-toastify';
import { useNavigate } from 'react-router-dom';

const CheckoutPage = () => {
  const { items, getCartTotal, clearCart } = useCart();
  const { currency, formatPrice, exchangeRate } = useCurrency();
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    email: '',
    firstName: '',
    lastName: '',
    phone: '',
    paymentMethod: 'card'
  });
  const [loading, setLoading] = useState(false);
  const [priceKey, setPriceKey] = useState(0);

  // Force re-render when currency changes
  useEffect(() => {
    setPriceKey(prev => prev + 1);
  }, [currency, formData.paymentMethod]);

  const calculatePricing = () => {
    const totalINR = getCartTotal();
    const totalUSD = totalINR / exchangeRate;
    
    return {
      inr: Math.round(totalINR),
      usd: Math.round(totalUSD * 100) / 100,
      formatted: {
        inr: new Intl.NumberFormat('en-IN', {
          style: 'currency',
          currency: 'INR',
          minimumFractionDigits: 0,
          maximumFractionDigits: 0
        }).format(totalINR),
        usd: new Intl.NumberFormat('en-US', {
          style: 'currency',
          currency: 'USD',
          minimumFractionDigits: 2,
          maximumFractionDigits: 2
        }).format(totalUSD)
      }
    };
  };

  const pricing = calculatePricing();

  const getDisplayPrice = () => {
    if (formData.paymentMethod === 'crypto') {
      return pricing.formatted.usd;
    } else if (formData.paymentMethod === 'card') {
      return `${pricing.formatted.inr} / ${pricing.formatted.usd}`;
    } else {
      return formatPrice(pricing.inr);
    }
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
          // Check if we have an invoice URL for redirection
          if (cryptoResult.data.invoice_url) {
            // DON'T clear cart until after successful payment
            // User will see cart contents until they complete payment
            
            // Redirect to NOWPayments hosted payment page
            window.location.href = cryptoResult.data.invoice_url;
          } else {
            // Fallback to success page with payment details
            clearCart(); // Only clear cart if not redirecting
            navigate('/order-success', {
              state: {
                orderId: orderResult.data.id,
                paymentMethod: 'crypto',
                paymentId: cryptoResult.data.payment_id,
                amount: usdTotal,
                currency: 'USD'
              }
            });
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
      navigate(`/order-failed?error=${encodeURIComponent(error.message)}`);
    } finally {
      setLoading(false);
    }
  };

  if (items.length === 0) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Your cart is empty</h2>
          <p className="text-gray-600 mb-8">Add some products to your cart to proceed with checkout.</p>
          <button
            onClick={() => navigate('/products')}
            className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors"
          >
            Shop Now
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Checkout</h1>
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Order Form */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-6">Order Information</h2>
            
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    First Name
                  </label>
                  <input
                    type="text"
                    name="firstName"
                    value={formData.firstName}
                    onChange={handleInputChange}
                    required
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Last Name
                  </label>
                  <input
                    type="text"
                    name="lastName"
                    value={formData.lastName}
                    onChange={handleInputChange}
                    required
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Email Address
                </label>
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleInputChange}
                  required
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Phone Number
                </label>
                <input
                  type="tel"
                  name="phone"
                  value={formData.phone}
                  onChange={handleInputChange}
                  required
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Payment Method
                </label>
                <div className="space-y-3">
                  <label className="flex items-center">
                    <input
                      type="radio"
                      name="paymentMethod"
                      value="card"
                      checked={formData.paymentMethod === 'card'}
                      onChange={handleInputChange}
                      className="mr-3"
                    />
                    <span>Credit/Debit Card</span>
                  </label>
                  <label className="flex items-center">
                    <input
                      type="radio"
                      name="paymentMethod"
                      value="upi"
                      checked={formData.paymentMethod === 'upi'}
                      onChange={handleInputChange}
                      className="mr-3"
                    />
                    <span>UPI Payment</span>
                  </label>
                  <label className="flex items-center">
                    <input
                      type="radio"
                      name="paymentMethod"
                      value="crypto"
                      checked={formData.paymentMethod === 'crypto'}
                      onChange={handleInputChange}
                      className="mr-3"
                    />
                    <span>Cryptocurrency</span>
                  </label>
                </div>
              </div>

              {formData.paymentMethod === 'crypto' && (
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-4">
                  <p className="text-sm text-blue-800">
                    <span className="font-medium">Cryptocurrency Payment:</span> You'll be redirected to our secure payment page where you can choose from Bitcoin, Ethereum, Tether, and other cryptocurrencies.
                  </p>
                </div>
              )}

              <button
                type="submit"
                disabled={loading}
                className="w-full bg-blue-600 text-white py-3 px-6 rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                {loading ? 'Processing...' : 'Place Order'}
              </button>
            </form>
          </div>

          {/* Order Summary */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-xl font-semibold text-gray-900 mb-6">Order Summary</h2>
            
            <div className="space-y-4">
              {items.map((item) => (
                <div key={`${item.id}-${item.duration}`} className="flex justify-between items-center py-3 border-b border-gray-200">
                  <div>
                    <h3 className="font-medium text-gray-900">{item.name}</h3>
                    <p className="text-sm text-gray-600">Duration: {item.duration}</p>
                    <p className="text-sm text-gray-600">Quantity: {item.quantity}</p>
                  </div>
                  <div className="text-right">
                    <p className="font-medium text-gray-900">
                      {formatPrice(item.price * item.quantity)}
                    </p>
                  </div>
                </div>
              ))}
            </div>

            <div className="border-t border-gray-200 pt-4 mt-6">
              <div className="flex justify-between items-center text-lg font-semibold text-gray-900">
                <span>Total:</span>
                <span className="text-2xl">
                  {formatPrice(getCartTotal())}
                </span>
              </div>
              {formData.paymentMethod === 'crypto' && (
                <p className="text-sm text-gray-600 mt-2">
                  Crypto payment amount: ${usdTotal.toFixed(2)} USD
                </p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CheckoutPage;