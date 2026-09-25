# Contributing to Telegram Avito Bot

First off, thanks for taking the time to contribute! ❤️

## 🌟 Code of Conduct

This project and everyone participating in it is governed by the Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to the maintainers.

## 🚀 How to Contribute

### Reporting Bugs

Before creating bug reports, please check existing issues. When creating a bug report, include:

- **Issue Template** - Use the provided template
- **Clear Description** - Describe what happened
- **Steps to Reproduce** - Clear steps to reproduce the issue
- **Expected vs Actual** - What you expected vs what happened
- **Environment** - Python version, OS, etc.

### Suggesting Features

Feature suggestions are welcome! Please provide:

- **Use Case** - Why would this feature be useful?
- **Implementation Ideas** - Any thoughts on how to implement
- **Alternatives Considered** - Other approaches you thought about

### Pull Requests

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📋 Development Guidelines

### Code Style

- Follow PEP 8 style guidelines
- Use type hints for function parameters and return values
- Write clear, descriptive variable names
- Add docstrings for public modules, functions, classes, and methods

### Testing

- Write tests for new features
- Ensure all tests pass before submitting PR
- Aim for high test coverage

```bash
pytest tests/ -v
```

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/) format:

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Example:
```
feat(search): add city filter option

Implemented dropdown selection for Russian cities
Added validation for empty city input

Closes #42
```

## 🛠 Setting Up Development Environment

```bash
# Clone repository
git clone https://github.com/yourusername/tg-avito-bot.git
cd tg-avito-bot

# Setup virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install
```

## 🔍 Code Review

All submissions require review. We use pull requests for reviews. The community will review your submission and may request changes.

Reviewers should check:

- Code quality and style
- Test coverage
- Security implications
- Performance impact
- Documentation updates

## 📚 Documentation

Please update documentation for:

- New features
- Changed behavior
- API changes
- Configuration options

Keep docs in sync with code changes.

## 🎯 Good First Issues

Look for issues labeled `good first issue` - perfect for newcomers!

## ❓ Questions

Questions? Feel free to:

- Open an issue with `question` label
- Ask in existing issue threads
- Contact the maintainers directly

Thank you for contributing! 💚
