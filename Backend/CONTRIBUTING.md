# Contributing to AI Life Goal Management System

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## Development Setup

1. **Fork and Clone**
```bash
git clone https://github.com/yourusername/ai-life-goals.git
cd ai-life-goals/Backend
```

2. **Create Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Set Up Environment**
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. **Start Services**
```bash
docker-compose up -d mongodb redis
```

## Code Standards

### Python Style
- Follow PEP 8
- Use type hints for all functions
- Maximum line length: 100 characters
- Use meaningful variable and function names

### Documentation
- Add docstrings to all classes and functions
- Include parameter and return type descriptions
- Provide usage examples for complex functions

### Testing
- Write tests for all new features
- Maintain minimum 90% test coverage
- Include both positive and negative test cases
- Test error scenarios and edge cases

## Commit Guidelines

### Commit Message Format
```
type(scope): brief description

Detailed explanation if needed

Fixes #issue_number
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples
```
feat(agents): add wellness agent health assessment
fix(auth): resolve JWT token expiration handling
docs(api): update endpoint documentation
test(agents): add integration tests for career agent
```

## Pull Request Process

1. **Create Feature Branch**
```bash
git checkout -b feature/your-feature-name
```

2. **Make Changes**
- Write code following the style guidelines
- Add comprehensive tests
- Update documentation if needed

3. **Test Your Changes**
```bash
pytest --cov=Backend --cov-report=term-missing
```

4. **Commit and Push**
```bash
git add .
git commit -m "feat(scope): your feature description"
git push origin feature/your-feature-name
```

5. **Create Pull Request**
- Use the PR template
- Provide clear description of changes
- Link related issues
- Ensure all checks pass

## Areas for Contribution

### High Priority
- Additional specialized agents (e.g., RelationshipAgent, TravelAgent)
- Enhanced external API integrations
- Advanced workflow orchestration
- Machine learning model integration

### Medium Priority
- Performance optimizations
- Additional authentication providers
- Enhanced monitoring and alerting
- Mobile API optimizations

### Documentation
- API usage examples
- Architecture documentation
- Deployment guides
- Troubleshooting guides

## Code Review Process

1. **Automated Checks**
- All tests must pass
- Code coverage must be maintained
- Linting checks must pass

2. **Manual Review**
- Code quality and style
- Architecture consistency
- Security considerations
- Performance implications

3. **Approval Process**
- At least one maintainer approval required
- Address all review comments
- Ensure CI/CD pipeline passes

## Getting Help

- **Documentation**: Check `/docs` directory
- **Issues**: Search existing GitHub issues
- **Discussions**: Use GitHub Discussions for questions
- **Contact**: Reach out to maintainers directly

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes for significant contributions
- Project documentation

Thank you for contributing to making life goal management more accessible and effective!