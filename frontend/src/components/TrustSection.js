import React from 'react';
import { 
  CheckCircleIcon, 
  StarIcon, 
  ShieldCheckIcon,
  CreditCardIcon,
  ClockIcon,
  HeartIcon
} from '@heroicons/react/24/solid';

const TrustSection = () => {
  const trustIndicators = [
    {
      icon: CheckCircleIcon,
      title: 'SSL Secured',
      description: '256-bit SSL encryption protects your data',
      color: 'text-green-500'
    },
    {
      icon: StarIcon,
      title: '4.8/5 Rating',
      description: 'Based on 8,500+ customer reviews',
      color: 'text-yellow-500'
    },
    {
      icon: ShieldCheckIcon,
      title: 'Trusted Provider',
      description: 'Serving customers since 2017',
      color: 'text-blue-500'
    },
    {
      icon: CreditCardIcon,
      title: 'Secure Payments',
      description: 'UPI, Cards, Crypto payments accepted',
      color: 'text-purple-500'
    },
    {
      icon: ClockIcon,
      title: 'Instant Delivery',
      description: 'Automated delivery within minutes',
      color: 'text-indigo-500'
    },
    {
      icon: HeartIcon,
      title: '24/7 Support',
      description: 'WhatsApp & Telegram support available',
      color: 'text-red-500'
    }
  ];

  const testimonials = [
    {
      name: 'Akshay Vankariant',
      rating: 5,
      text: 'Absolutely legit and super fast. Got Netflix 4 screen for ₹200. Delivery was super quick. Payment method was UPI so secure. 100% recommended!',
      verified: true,
      platform: 'Netflix Premium'
    },
    {
      name: 'Chirag Taparia', 
      rating: 5,
      text: 'This was my first purchase and it was a good experience got the account within promised time. Account details working absolutely fine. Will definitely do business again.',
      verified: true,
      platform: 'Disney+ Hotstar'
    },
    {
      name: 'Chaitanya CH',
      rating: 5,
      text: 'The best site ever to buy premium accounts. I have purchased several accounts past one year. Best user experience, reacts immediately and resolves any problems.',
      verified: true,
      badge: 'VIP Customer',
      platform: 'Multiple Services'
    }
  ];

  const stats = [
    { label: 'Happy Customers', value: '8,500+', icon: '😊' },
    { label: 'Orders Delivered', value: '12,000+', icon: '📦' },
    { label: 'Countries Served', value: '25+', icon: '🌍' },
    { label: 'Success Rate', value: '99.8%', icon: '🎯' }
  ];

  return (
    <div className="bg-gray-50 py-16">
      <div className="container mx-auto px-4">
        {/* Trust Indicators */}
        <div className="text-center mb-16">
          <h2 className="text-3xl font-bold text-gray-900 mb-4">Why 8,500+ Customers Trust Us</h2>
          <p className="text-lg text-gray-600 mb-12">We've been the most trusted premium service provider since 2017</p>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {trustIndicators.map((indicator, index) => (
              <div key={index} className="bg-white p-6 rounded-2xl shadow-lg hover:shadow-xl transition-shadow">
                <div className={`w-12 h-12 ${indicator.color} mx-auto mb-4`}>
                  <indicator.icon className="w-12 h-12" />
                </div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">{indicator.title}</h3>
                <p className="text-gray-600 text-sm">{indicator.description}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8 mb-16">
          {stats.map((stat, index) => (
            <div key={index} className="text-center bg-white p-6 rounded-2xl shadow-lg">
              <div className="text-4xl mb-2">{stat.icon}</div>
              <div className="text-3xl font-bold text-blue-600 mb-2">{stat.value}</div>
              <div className="text-sm text-gray-600">{stat.label}</div>
            </div>
          ))}
        </div>

        {/* Customer Reviews */}
        <div className="text-center mb-8">
          <h3 className="text-2xl font-bold text-gray-900 mb-2">Customer Reviews</h3>
          <p className="text-gray-600">See what our customers have to say about us</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {testimonials.map((testimonial, index) => (
            <div key={index} className="bg-white p-6 rounded-2xl shadow-lg hover:shadow-xl transition-shadow">
              <div className="flex items-center mb-4">
                {[...Array(5)].map((_, i) => (
                  <StarIcon 
                    key={i} 
                    className={`w-4 h-4 ${i < testimonial.rating ? 'text-yellow-400' : 'text-gray-300'}`}
                  />
                ))}
                <span className="ml-2 text-sm text-gray-600">({testimonial.rating}/5)</span>
              </div>
              
              <p className="text-gray-700 mb-4 italic">"{testimonial.text}"</p>
              
              <div className="border-t pt-4">
                <div className="flex items-center justify-between">
                  <div>
                    <div className="font-semibold text-gray-900">{testimonial.name}</div>
                    <div className="text-sm text-gray-600">{testimonial.platform}</div>
                    {testimonial.verified && (
                      <div className="flex items-center text-green-600 text-sm mt-1">
                        <CheckCircleIcon className="w-4 h-4 mr-1" />
                        Verified Purchase
                      </div>
                    )}
                    {testimonial.badge && (
                      <div className="bg-purple-100 text-purple-800 px-2 py-1 rounded-full text-xs font-semibold mt-1 inline-block">
                        {testimonial.badge}
                      </div>
                    )}
                  </div>
                  <div className="w-12 h-12 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center text-white font-bold">
                    {testimonial.name.charAt(0)}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Money Back Guarantee */}
        <div className="mt-16 text-center">
          <div className="bg-gradient-to-r from-green-500 to-emerald-600 text-white p-8 rounded-2xl inline-block">
            <ShieldCheckIcon className="w-16 h-16 mx-auto mb-4" />
            <h3 className="text-2xl font-bold mb-2">100% Satisfaction Guarantee</h3>
            <p className="text-lg opacity-90">
              We're so confident in our service quality that we offer a satisfaction guarantee. 
              Your trust is our priority!
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TrustSection;