import React, { createContext, useContext, useState, useEffect } from 'react';

const CurrencyContext = createContext();

export const CurrencyProvider = ({ children }) => {
  const [currency, setCurrency] = useState('INR');
  const [exchangeRate, setExchangeRate] = useState(83); // 1 USD = 83 INR (approximate)

  useEffect(() => {
    const savedCurrency = localStorage.getItem('currency');
    if (savedCurrency) {
      setCurrency(savedCurrency);
    }
  }, []);

  const switchCurrency = (newCurrency) => {
    setCurrency(newCurrency);
    localStorage.setItem('currency', newCurrency);
  };

  const formatPrice = (priceInINR) => {
    if (currency === 'USD') {
      const priceInUSD = priceInINR / exchangeRate;
      return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD',
      }).format(priceInUSD);
    } else {
      return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR',
      }).format(priceInINR);
    }
  };

  const convertPrice = (priceInINR) => {
    if (currency === 'USD') {
      return priceInINR / exchangeRate;
    }
    return priceInINR;
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