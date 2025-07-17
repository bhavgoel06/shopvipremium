import React from 'react';

const ProfessionalLogo = ({ className = '', size = 'medium' }) => {
  const sizes = {
    small: { container: 'w-8 h-8', text: 'text-sm' },
    medium: { container: 'w-12 h-12', text: 'text-lg' },
    large: { container: 'w-16 h-16', text: 'text-xl' }
  };

  const currentSize = sizes[size];

  return (
    <div className={`flex items-center gap-3 ${className}`}>
      {/* Professional Logo Icon */}
      <div className={`${currentSize.container} relative`}>
        <svg 
          viewBox="0 0 120 120" 
          className="w-full h-full"
          xmlns="http://www.w3.org/2000/svg"
        >
          <defs>
            <linearGradient id="primaryGradient" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" style={{stopColor: '#667eea', stopOpacity: 1}} />
              <stop offset="50%" style={{stopColor: '#764ba2', stopOpacity: 1}} />
              <stop offset="100%" style={{stopColor: '#f093fb', stopOpacity: 1}} />
            </linearGradient>
            
            <linearGradient id="secondaryGradient" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" style={{stopColor: '#4facfe', stopOpacity: 1}} />
              <stop offset="100%" style={{stopColor: '#00f2fe', stopOpacity: 1}} />
            </linearGradient>
            
            <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
              <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
              <feMerge>
                <feMergeNode in="coloredBlur"/>
                <feMergeNode in="SourceGraphic"/>
              </feMerge>
            </filter>
          </defs>
          
          {/* Background Circle */}
          <circle cx="60" cy="60" r="55" fill="url(#primaryGradient)" filter="url(#glow)"/>
          
          {/* Inner Ring */}
          <circle cx="60" cy="60" r="48" fill="none" stroke="rgba(255,255,255,0.3)" strokeWidth="2"/>
          
          {/* Modern Shopping Bag Icon */}
          <g transform="translate(60, 60) scale(1.2)">
            <path 
              d="M-15 -10 L15 -10 L12 20 L-12 20 Z" 
              fill="rgba(255,255,255,0.95)"
              stroke="rgba(255,255,255,0.8)"
              strokeWidth="1"
              rx="2"
            />
            
            {/* Bag Handles */}
            <path 
              d="M-8 -10 L-8 -16 C-8 -18 -6 -20 -4 -20 L4 -20 C6 -20 8 -18 8 -16 L8 -10" 
              fill="none"
              stroke="rgba(255,255,255,0.9)"
              strokeWidth="2.5"
              strokeLinecap="round"
            />
            
            {/* Premium Star */}
            <g transform="translate(8, -12) scale(0.8)">
              <path 
                d="M0 -6 L1.8 -1.8 L6 -1.8 L2.4 1.2 L4.2 6 L0 3 L-4.2 6 L-2.4 1.2 L-6 -1.8 L-1.8 -1.8 Z"
                fill="#FFD700"
                stroke="#FFA500"
                strokeWidth="0.5"
              />
            </g>
          </g>
          
          {/* Floating Elements */}
          <g opacity="0.6">
            <circle cx="25" cy="35" r="2" fill="#FFFFFF">
              <animate attributeName="cy" values="35;25;35" dur="3s" repeatCount="indefinite"/>
              <animate attributeName="opacity" values="0.3;1;0.3" dur="3s" repeatCount="indefinite"/>
            </circle>
            <circle cx="95" cy="45" r="1.5" fill="#FFFFFF">
              <animate attributeName="cy" values="45;35;45" dur="4s" repeatCount="indefinite"/>
              <animate attributeName="opacity" values="0.5;1;0.5" dur="4s" repeatCount="indefinite"/>
            </circle>
            <circle cx="30" cy="85" r="1.8" fill="#FFFFFF">
              <animate attributeName="cy" values="85;75;85" dur="3.5s" repeatCount="indefinite"/>
              <animate attributeName="opacity" values="0.4;1;0.4" dur="3.5s" repeatCount="indefinite"/>
            </circle>
          </g>
        </svg>
      </div>
      
      {/* Brand Text */}
      <div className="flex flex-col">
        <span className={`font-bold text-gray-900 ${currentSize.text} leading-tight`}>
          Shop For Premium
        </span>
        <span className="text-xs text-gray-600 font-medium tracking-wide">
          Get More, Pay Less
        </span>
      </div>
    </div>
  );
};

export default ProfessionalLogo;