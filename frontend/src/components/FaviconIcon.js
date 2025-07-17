import React from 'react';

const FaviconIcon = () => {
  return (
    <svg width="32" height="32" viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="faviconGradient" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" style={{stopColor: '#667eea'}} />
          <stop offset="50%" style={{stopColor: '#764ba2'}} />
          <stop offset="100%" style={{stopColor: '#f093fb'}} />
        </linearGradient>
      </defs>
      
      <rect width="32" height="32" rx="6" fill="url(#faviconGradient)" />
      
      {/* Shopping bag icon */}
      <g transform="translate(16, 16) scale(0.8)">
        <path 
          d="M-6 -4 L6 -4 L5 8 L-5 8 Z" 
          fill="rgba(255,255,255,0.95)"
          stroke="rgba(255,255,255,0.8)"
          strokeWidth="0.5"
          rx="1"
        />
        
        {/* Bag handles */}
        <path 
          d="M-3 -4 L-3 -6 C-3 -7 -2 -8 -1 -8 L1 -8 C2 -8 3 -7 3 -6 L3 -4" 
          fill="none"
          stroke="rgba(255,255,255,0.9)"
          strokeWidth="1"
          strokeLinecap="round"
        />
        
        {/* Premium star */}
        <g transform="translate(3, -5) scale(0.4)">
          <path 
            d="M0 -3 L1 -1 L3 -1 L1.5 0.5 L2 3 L0 1.5 L-2 3 L-1.5 0.5 L-3 -1 L-1 -1 Z"
            fill="#FFD700"
            stroke="#FFA500"
            strokeWidth="0.2"
          />
        </g>
      </g>
    </svg>
  );
};

export default FaviconIcon;