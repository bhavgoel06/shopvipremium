import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function ProductCard({ product }) {
  return (
    <div className="product-card">
      <img src={product.image_url} alt={product.name} />
      <div className="product-info">
        <h3>{product.name}</h3>
        <p>{product.short_description}</p>
        <div className="price">
          <span className="discounted">₹{product.discounted_price}</span>
          <span className="original">₹{product.original_price}</span>
          <span className="discount">{product.discount_percentage}% OFF</span>
        </div>
        <div className="rating">⭐ {product.rating} ({product.total_reviews} reviews)</div>
        <button className="buy-btn">Buy Now</button>
      </div>
    </div>
  );
}

function App() {
  const [products, setProducts] = useState([]);
  const [featured, setFeatured] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadData = async () => {
      try {
        const [productsRes, featuredRes] = await Promise.all([
          axios.get(`${process.env.REACT_APP_BACKEND_URL}/products?per_page=12`),
          axios.get(`${process.env.REACT_APP_BACKEND_URL}/products/featured`)
        ]);
        setProducts(productsRes.data.data || []);
        setFeatured(featuredRes.data.data || []);
      } catch (error) {
        console.error('Error:', error);
      } finally {
        setLoading(false);
      }
    };
    loadData();
  }, []);

  if (loading) return <div className="loading">Loading...</div>;

  return (
    <div className="App">
      <header className="header">
        <div className="container">
          <h1>Shop VIP Premium</h1>
          <p>Digital Workspace Toolkit - {products.length} Products Available</p>
        </div>
      </header>

      <section className="hero">
        <div className="container">
          <h2>Your Digital Workspace Toolkit</h2>
          <p>Curated access to digital productivity tools and professional utilities</p>
          <div className="stats">
            <div className="stat">
              <span>81+</span>
              <label>Premium Tools</label>
            </div>
            <div className="stat">
              <span>24/7</span>
              <label>Support</label>
            </div>
            <div className="stat">
              <span>Instant</span>
              <label>Access</label>
            </div>
          </div>
        </div>
      </section>

      <section className="featured">
        <div className="container">
          <h2>Featured Digital Tools</h2>
          <div className="products-grid">
            {featured.map(product => (
              <ProductCard key={product.id} product={product} />
            ))}
          </div>
        </div>
      </section>

      <section className="products">
        <div className="container">
          <h2>All Products</h2>
          <div className="products-grid">
            {products.map(product => (
              <ProductCard key={product.id} product={product} />
            ))}
          </div>
        </div>
      </section>

      <footer className="footer">
        <div className="container">
          <p>&copy; 2025 Shop VIP Premium. Digital workspace toolkit for professionals.</p>
          <p>Support: Telegram @shopvippremium | WhatsApp +91 98765 43210</p>
        </div>
      </footer>
    </div>
  );
}

export default App;