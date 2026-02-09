
import React from 'react';

interface LeapLogoProps {
  className?: string;
}

export const LeapLogo = ({ className = "" }: LeapLogoProps) => {
  return (
    <svg 
      width="300" 
      height="120" 
      viewBox="0 0 300 120" 
      className={`animate-bounce ${className}`}
      xmlns="http://www.w3.org/2000/svg"
    >
      <style>
        {`
          @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@700&display=swap');
        `}
      </style>
      <text
        x="10"
        y="90"
        fill="#00A676"
        style={{
          fontSize: '100px',
          fontFamily: 'Outfit, sans-serif',
          fontWeight: 'bold',
        }}
      >
        <tspan style={{ fontSize: '110px' }}>L</tspan>
        <tspan x="75" y="90">eap</tspan>
      </text>
    </svg>
  );
};

export default LeapLogo;
