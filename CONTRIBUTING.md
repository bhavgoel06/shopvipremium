# Contributing to Shop VIP Premium

Thank you for your interest in contributing to Shop VIP Premium! This document provides guidelines and instructions for contributing to our e-commerce platform.

## 🤝 How to Contribute

### Types of Contributions

We welcome various types of contributions:

- 🐛 **Bug Reports** - Help us identify and fix issues
- 💡 **Feature Requests** - Suggest new features or improvements
- 🔧 **Code Contributions** - Submit bug fixes or new features
- 📚 **Documentation** - Improve our documentation
- 🧪 **Testing** - Help us test new features and find bugs
- 🎨 **Design** - UI/UX improvements and design suggestions

### Getting Started

1. **Fork the Repository**
   ```bash
   git clone https://github.com/yourusername/shopvippremium.git
   cd shopvippremium
   ```

2. **Set Up Development Environment**
   ```bash
   # Backend setup
   cd backend
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   
   # Frontend setup
   cd ../frontend
   yarn install
   ```

3. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## 📝 Contribution Guidelines

### Code Style

#### Python (Backend)
- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Write docstrings for functions and classes
- Use meaningful variable and function names

```python
from typing import Optional, List
from pydantic import BaseModel

class ProductCreate(BaseModel):
    """Model for creating a new product."""
    name: str
    description: str
    price: float
    category: str
    
def create_product(product_data: ProductCreate) -> Optional[Product]:
    """
    Create a new product in the database.
    
    Args:
        product_data: Product information
        
    Returns:
        Created product or None if failed
    """
    pass
```

#### JavaScript/React (Frontend)
- Use ES6+ syntax
- Follow React best practices
- Use functional components with hooks
- Implement proper error handling

```javascript
import React, { useState, useEffect } from 'react';
import { toast } from 'react-toastify';

const ProductCard = ({ product, onAddToCart }) => {
  const [loading, setLoading] = useState(false);
  
  const handleAddToCart = async () => {
    try {
      setLoading(true);
      await onAddToCart(product);
      toast.success('Product added to cart!');
    } catch (error) {
      toast.error('Failed to add product');
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <div className="product-card">
      {/* Component JSX */}
    </div>
  );
};

export default ProductCard;
```

### Commit Messages

Follow conventional commit format:

```
type(scope): description

body (optional)

footer (optional)
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(payment): add cryptocurrency payment support

fix(auth): resolve JWT token expiration issue

docs(readme): update deployment instructions

style(frontend): improve mobile responsiveness
```

### Pull Request Process

1. **Before Creating PR**
   - Ensure your code follows the style guidelines
   - Add tests for new features
   - Update documentation if needed
   - Test your changes locally

2. **Creating PR**
   - Use a descriptive title
   - Fill out the PR template
   - Link related issues
   - Add screenshots for UI changes

3. **PR Template**
   ```markdown
   ## Description
   Brief description of the changes
   
   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Breaking change
   - [ ] Documentation update
   
   ## Testing
   - [ ] Local testing completed
   - [ ] Added unit tests
   - [ ] Manual testing performed
   
   ## Screenshots (if applicable)
   
   ## Related Issues
   Closes #issue_number
   ```

## 🧪 Testing

### Running Tests

#### Backend Tests
```bash
cd backend
source venv/bin/activate
python -m pytest tests/ -v
```

#### Frontend Tests
```bash
cd frontend
yarn test
```

### Writing Tests

#### Backend (Python)
```python
import pytest
from fastapi.testclient import TestClient
from server import app

client = TestClient(app)

def test_create_product():
    """Test product creation endpoint."""
    product_data = {
        "name": "Test Product",
        "description": "Test Description",
        "price": 99.99,
        "category": "software"
    }
    
    response = client.post("/api/products", json=product_data)
    assert response.status_code == 200
    assert response.json()["success"] is True
```

#### Frontend (JavaScript)
```javascript
import { render, screen, fireEvent } from '@testing-library/react';
import ProductCard from '../components/ProductCard';

test('renders product information', () => {
  const mockProduct = {
    id: '1',
    name: 'Test Product',
    price: 99.99,
    description: 'Test Description'
  };
  
  render(<ProductCard product={mockProduct} />);
  
  expect(screen.getByText('Test Product')).toBeInTheDocument();
  expect(screen.getByText('$99.99')).toBeInTheDocument();
});
```

## 🐛 Bug Reports

### Before Submitting a Bug Report

1. Check existing issues to avoid duplicates
2. Test with the latest version
3. Gather relevant information

### Bug Report Template

```markdown
## Bug Description
A clear description of the bug

## Steps to Reproduce
1. Go to '...'
2. Click on '...'
3. See error

## Expected Behavior
What should happen

## Actual Behavior
What actually happens

## Environment
- OS: [e.g., Ubuntu 22.04]
- Browser: [e.g., Chrome 120]
- Version: [e.g., 1.0.0]

## Screenshots
If applicable, add screenshots

## Additional Context
Any other relevant information
```

## 💡 Feature Requests

### Before Submitting a Feature Request

1. Check if the feature already exists
2. Search existing feature requests
3. Consider the scope and feasibility

### Feature Request Template

```markdown
## Feature Description
A clear description of the feature

## Problem Statement
What problem does this solve?

## Proposed Solution
How would you implement this?

## Alternative Solutions
Any alternative approaches?

## Additional Context
Screenshots, mockups, or examples
```

## 📚 Documentation

### Documentation Guidelines

- Use clear, concise language
- Include code examples
- Add screenshots for UI features
- Keep documentation up-to-date
- Follow markdown formatting standards

### Areas Needing Documentation

- API endpoints and parameters
- Component usage and props
- Deployment procedures
- Configuration options
- Troubleshooting guides

## 🏗️ Architecture

### Project Structure

```
shopvippremium/
├── backend/
│   ├── models.py          # Pydantic models
│   ├── database.py        # Database operations
│   ├── server.py          # FastAPI application
│   ├── nowpayments_service.py # Payment processing
│   └── requirements.txt   # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── pages/         # Page components
│   │   ├── context/       # React context
│   │   └── styles/        # CSS files
│   └── package.json       # Node dependencies
├── master-deploy.sh       # Deployment script
└── README.md              # Project documentation
```

### Key Components

#### Backend Components
- **FastAPI Application** - Main server application
- **Database Layer** - MongoDB operations and models
- **Authentication** - JWT-based user authentication
- **Payment Processing** - NOWPayments integration
- **Admin Panel API** - Administrative endpoints

#### Frontend Components
- **Product Catalog** - Product display and filtering
- **Shopping Cart** - Cart management and checkout
- **User Authentication** - Login and registration
- **Admin Dashboard** - Store management interface
- **Payment Integration** - Cryptocurrency payment flow

## 🔐 Security

### Security Considerations

When contributing, please consider:

- Never commit API keys or secrets
- Validate all user inputs
- Use parameterized queries
- Implement proper error handling
- Follow OWASP security guidelines

### Reporting Security Issues

For security vulnerabilities:
1. **DO NOT** create public issues
2. Email security@shopvippremium.com
3. Include detailed information
4. Allow time for fixes before disclosure

## 🤔 Questions and Support

### Getting Help

- **Documentation** - Check existing docs first
- **Issues** - Search existing issues
- **Discussions** - Use GitHub Discussions for questions
- **Discord/Telegram** - Join our community channels

### Community Guidelines

- Be respectful and inclusive
- Help others when possible
- Follow our code of conduct
- Provide constructive feedback

## 📋 Development Setup

### Prerequisites

- **Python 3.11+** for backend development
- **Node.js 20+** for frontend development
- **MongoDB** for database
- **Git** for version control

### IDE Recommendations

#### VS Code Extensions
- Python
- ES7+ React/Redux/React-Native snippets
- Tailwind CSS IntelliSense
- GitLens
- Prettier
- ESLint

#### PyCharm/WebStorm
- Professional IDEs with built-in support
- Excellent debugging capabilities
- Integrated version control

### Environment Variables

Create `.env` files:

#### Backend `.env`
```env
MONGO_URL=mongodb://localhost:27017
DB_NAME=shopvippremium_dev
JWT_SECRET=your-dev-jwt-secret
NOWPAYMENTS_PRIVATE_KEY=your-dev-key
NOWPAYMENTS_PUBLIC_KEY=your-dev-key
NOWPAYMENTS_IPN_SECRET=your-dev-secret
```

#### Frontend `.env`
```env
REACT_APP_BACKEND_URL=http://localhost:8001/api
REACT_APP_NOWPAYMENTS_PUBLIC_KEY=your-dev-key
```

## 🚀 Release Process

### Versioning

We use Semantic Versioning (SemVer):
- **MAJOR** version for incompatible API changes
- **MINOR** version for new functionality
- **PATCH** version for bug fixes

### Release Checklist

- [ ] Update version numbers
- [ ] Update CHANGELOG.md
- [ ] Run all tests
- [ ] Update documentation
- [ ] Create release notes
- [ ] Tag the release
- [ ] Deploy to staging
- [ ] Deploy to production

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙏 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation
- Special thanks in commit messages

---

Thank you for contributing to Shop VIP Premium! Your contributions help make this project better for everyone. 🚀