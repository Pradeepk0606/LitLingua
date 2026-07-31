# Contributing to LitLingua

Thank you for your interest in contributing to LitLingua! This document provides guidelines for contributing to the project.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and inclusive environment for all contributors.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in Issues
2. If not, create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable
   - Environment details (OS, browser, versions)

### Suggesting Features

1. Check existing feature requests
2. Create a new issue with:
   - Clear description of the feature
   - Use cases and benefits
   - Possible implementation approach

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Write or update tests
5. Ensure all tests pass
6. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
7. Push to the branch (`git push origin feature/AmazingFeature`)
8. Open a Pull Request

## Development Setup

### Prerequisites
- Python 3.9+
- Node.js 18+
- Tesseract OCR
- Git

### Setup Steps

```bash
# Clone the repository
git clone https://github.com/yourusername/LitLingua.git
cd LitLingua

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Frontend setup
cd ../frontend
npm install

# Run tests
cd ../backend
pytest

cd ../frontend
npm test
```

## Coding Standards

### Python (Backend)
- Follow PEP 8 style guide
- Use type hints where appropriate
- Write docstrings for functions and classes
- Maximum line length: 100 characters
- Use `black` for code formatting
- Use `flake8` for linting

### JavaScript/React (Frontend)
- Follow ESLint configuration
- Use functional components with hooks
- Write meaningful component and variable names
- Use Prettier for code formatting
- Add PropTypes or TypeScript types

### Commit Messages
- Use present tense ("Add feature" not "Added feature")
- Use imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit first line to 72 characters
- Reference issues and pull requests

Example:
```
Add Nepali language support for OCR

- Integrate Tesseract Nepali language pack
- Add language detection for Devanagari script
- Update tests for Nepali text extraction

Fixes #123
```

## Testing

### Backend Tests
```bash
cd backend
pytest tests/ -v
pytest tests/ --cov=. --cov-report=html
```

### Frontend Tests
```bash
cd frontend
npm test
npm run test:coverage
```

## Documentation

- Update README.md if adding new features
- Update API documentation in docs/api_reference.md
- Add inline comments for complex logic
- Update CHANGELOG.md

## Project Structure

```
LitLingua/
├── backend/          # FastAPI backend
│   ├── routers/      # API endpoints
│   ├── models/       # ML models
│   ├── utils/        # Utilities
│   └── tests/        # Backend tests
├── frontend/         # React frontend
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── hooks/
│   └── public/
└── docs/             # Documentation
```

## Questions?

Feel free to open an issue or reach out to the maintainers.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
