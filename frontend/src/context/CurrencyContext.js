import React, { createContext, useContext, useState, useEffect } from 'react';

const CurrencyContext = createContext();

export const CurrencyProvider = ({ children }) => {
  const [currency, setCurrency] = useState('INR');
  const [exchangeRate, setExchangeRate] = useState(90); // 1 USD = 90 INR (fixed rate)

  useEffect(() => {
    const savedCurrency = localStorage.getItem('currency');
    if (savedCurrency) {
      setCurrency(savedCurrency);
    }
  }, []);

  const switchCurrency = (newCurrency) => {
    setCurrency(newCurrency);
    localStorage.setItem('currency', newCurrency);
    // Force a small delay to ensure state update propagates
    setTimeout(() => {
      window.dispatchEvent(new CustomEvent('currencyChanged', { detail: newCurrency }));
    }, 10);
  };

  const formatPrice = (priceInINR) => {
    if (currency === 'USD') {
      const priceInUSD = priceInINR / exchangeRate;
      return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
      }).format(priceInUSD);
    } else {
      return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
      }).format(Math.round(priceInINR));
    }
  };

  const convertPrice = (priceInINR) => {
    if (currency === 'USD') {
      return Math.round((priceInINR / exchangeRate) * 100) / 100;
    }
    return Math.round(priceInINR);
  };

  const getCurrencySymbol = () => {
    return currency === 'USD' ? '$' : '₹';
  };

  const value = {
    currency,
    exchangeRate,
    switchCurrency,
    formatPrice,
    convertPrice,
    getCurrencySymbol
  };

  return (
    <CurrencyContext.Provider value={value}>
      {children}
    </CurrencyContext.Provider>
  );
};

export const useCurrency = () => {
  const context = useContext(CurrencyContext);
  if (!context) {
    throw new Error('useCurrency must be used within a CurrencyProvider');
  }
  return context;
};