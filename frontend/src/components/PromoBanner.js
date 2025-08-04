import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { XMarkIcon, FireIcon, ClockIcon } from '@heroicons/react/24/solid';

const PromoBanner = () => {
  const [isVisible, setIsVisible] = useState(true);
  const [timeLeft, setTimeLeft] = useState(3600); // 1 hour in seconds

  useEffect(() => {
    const timer = setInterval(() => {
      setTimeLeft((prev) => prev > 0 ? prev - 1 : 3600); // Reset after countdown
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  const formatTime = (seconds) => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  if (!isVisible) return null;

  return (
    <div className="bg-gradient-to-r from-red-600 to-red-700 text-white py-3 px-4 relative overflow-hidden">
      <div className="absolute inset-0 bg-black opacity-10"></div>
      <div className="relative z-10 container mx-auto">
        <div className="flex flex-col md:flex-row items-center justify-center text-center md:text-left gap-4">
          {/* Mobile Layout */}
          <div className="md:hidden flex flex-col items-center space-y-2">
            <div className="flex items-center space-x-2">
              <FireIcon className="w-5 h-5 animate-pulse" />
              <span className="font-bold text-lg">⚡ ChatGPT Plus Offer!</span>
            </div>
            <div className="text-sm">
              Now on Shop VIP Premium. Only <span className="font-bold">₹589</span> or <span className="font-bold">$12/month</span>
            </div>
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-1">
                <ClockIcon className="w-4 h-4" />
                <span className="text-sm">Offer ends in: <span className="font-mono font-bold">{formatTime(timeLeft)}</span></span>
              </div>
              <Link
                to="/products?search=chatgpt"
                className="bg-white text-red-600 px-4 py-1 rounded-full text-sm font-bold hover:bg-gray-100 transition-colors"
              >
                SHOP NOW!
              </Link>
            </div>
          </div>

          {/* Desktop Layout */}
          <div className="hidden md:flex items-center justify-center space-x-6 w-full">
            <div className="flex items-center space-x-2">
              <FireIcon className="w-6 h-6 animate-pulse" />
              <span className="font-bold text-lg">⚡ ChatGPT Plus Offer!</span>
            </div>
            
            <div className="text-sm">
              Now on Shop VIP Premium. Unlock fast, advanced AI features with priority access.
            </div>
            
            <div className="font-bold">
              Only <span className="text-yellow-300">₹589</span> or <span className="text-yellow-300">$12/month</span>
            </div>
            
            <div className="flex items-center space-x-1">
              <ClockIcon className="w-4 h-4" />
              <span className="text-sm">Offer ends in: <span className="font-mono font-bold text-yellow-300">{formatTime(timeLeft)}</span></span>
            </div>
            
            <Link
              to="/products?search=chatgpt"
              className="bg-white text-red-600 px-6 py-2 rounded-full font-bold hover:bg-gray-100 transition-colors animate-pulse"
            >
              SHOP NOW!
            </Link>
          </div>
          
          <button
            onClick={() => setIsVisible(false)}
            className="absolute right-4 top-1/2 transform -translate-y-1/2 hover:bg-white/20 rounded-full p-1 transition-colors"
          >
            <XMarkIcon className="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default PromoBanner;