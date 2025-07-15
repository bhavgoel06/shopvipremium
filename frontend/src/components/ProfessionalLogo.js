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
          viewBox="0 0 100 100" 
          className="w-full h-full"
          xmlns="http://www.w3.org/2000/svg"
        >
          {/* Background Circle with Gradient */}
          <defs>
            <linearGradient id="bgGradient" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" style={{stopColor: '#4F46E5', stopOpacity: 1}} />
              <stop offset="50%" style={{stopColor: '#7C3AED', stopOpacity: 1}} />
              <stop offset="100%" style={{stopColor: '#EC4899', stopOpacity: 1}} />
            </linearGradient>
            
            <linearGradient id="iconGradient" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" style={{stopColor: '#FFFFFF', stopOpacity: 1}} />
              <stop offset="100%" style={{stopColor: '#F1F5F9', stopOpacity: 1}} />
            </linearGradient>
            
            <filter id="shadow" x="-50%" y="-50%" width="200%" height="200%">
              <feGaussianBlur in="SourceAlpha" stdDeviation="3"/>
              <feOffset dx="2" dy="2" result="offset"/>
              <feComponentTransfer>
                <feFuncA type="linear" slope="0.3"/>
              </feComponentTransfer>
              <feMerge> 
                <feMergeNode/>
                <feMergeNode in="SourceGraphic"/> 
              </feMerge>
            </filter>
          </defs>
          
          {/* Main Circle */}
          <circle cx="50" cy="50" r="48" fill="url(#bgGradient)" filter="url(#shadow)"/>
          
          {/* Inner Circle */}
          <circle cx="50" cy="50" r="42" fill="none" stroke="rgba(255,255,255,0.2)" strokeWidth="1"/>
          
          {/* Shopping Cart Icon */}
          <g transform="translate(25, 25) scale(0.8)">
            <path 
              d="M7 4V2C7 1.45 7.45 1 8 1H9C9.55 1 10 1.45 10 2V4H20L18 12H9L7 4Z" 
              fill="url(#iconGradient)"
              stroke="rgba(255,255,255,0.5)"
              strokeWidth="0.5"
            />
            <path 
              d="M10 12V14C10 14.55 10.45 15 11 15H17C17.55 15 18 14.55 18 14V12" 
              fill="url(#iconGradient)"
            />
            <circle cx="11" cy="18" r="1.5" fill="url(#iconGradient)"/>
            <circle cx="17" cy="18" r="1.5" fill="url(#iconGradient)"/>
          </g>
          
          {/* Premium Badge */}
          <g transform="translate(65, 15)">
            <circle cx="8" cy="8" r="6" fill="#FCD34D"/>
            <path d="M5 8L7 10L11 6" stroke="#92400E" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
          </g>
          
          {/* Sparkle Effects */}
          <g opacity="0.8">
            <circle cx="20" cy="30" r="1" fill="#FFFFFF">
              <animate attributeName="opacity" values="0.3;1;0.3" dur="2s" repeatCount="indefinite"/>
            </circle>
            <circle cx="75" cy="45" r="1.5" fill="#FFFFFF">
              <animate attributeName="opacity" values="0.5;1;0.5" dur="3s" repeatCount="indefinite"/>
            </circle>
            <circle cx="30" cy="70" r="1" fill="#FFFFFF">
              <animate attributeName="opacity" values="0.4;1;0.4" dur="2.5s" repeatCount="indefinite"/>
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