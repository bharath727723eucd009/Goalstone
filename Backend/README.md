# AI Life Goal Management System

A scalable, production-ready multi-agent AI backend for personalized life goal management and achievement tracking.

## 🎯 Problem Statement

Managing life goals across multiple domains (career, finance, wellness, learning) is complex and overwhelming. Traditional goal-setting tools lack personalization, domain expertise, and intelligent recommendations. This system provides AI-powered agents that understand each domain deeply and work together to create comprehensive, achievable life plans.

## ✨ Key Features

### Multi-Agent Architecture
- **CoordinatorAgent**: Orchestrates specialized agents and creates comprehensive plans
- **CareerAgent**: Job search, skill analysis, career guidance
- **FinanceAgent**: Budget analysis, investment advice, financial planning
- **WellnessAgent**: Fitness plans, nutrition advice, health assessments
- **LearningAgent**: Course recommendations, skill gap analysis, learning paths

### Authentication & Security
- JWT-based authentication with session management
- Redis session storage with fallback to in-memory
- Protected API endpoints with user context injection
- Secure middleware with request/response logging

### Database & Persistence
- MongoDB integration with Motor (async driver)
- User profiles, milestones, and agent outputs storage
- Real-time progress tracking across all goal categories
- Comprehensive data validation with Pydantic models

### Observability & Monitoring
- Structured logging with Loguru (JSON format)
- Prometheus metrics for API calls, agent runs, errors
- Performance monitoring and health checks
- Request tracing with user context

### Testing & Quality
- 95%+ test coverage with pytest
- Unit, integration, and performance tests
- Comprehensive error scenario testing
- Mock implementations for external dependencies

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Application                      │
├─────────────────────────────────────────────────────────────┤
│  Auth Middleware  │  Logging Middleware  │  CORS Middleware │
├─────────────────────────────────────────────────────────────┤
│                        API Routes                           │
│  /auth  │  /agents  │  /data  │  /metrics  │  /health      │
├─────────────────────────────────────────────────────────────┤
│                    Agent Layer                              │
│  CoordinatorAgent  │  CareerAgent  │  FinanceAgent         │
│  WellnessAgent     │  LearningAgent                        │
├─────────────────────────────────────────────────────────────┤
│                   Service Layer                             │
│  Session Manager  │  Message Broker  │  Workflow Engine    │
├─────────────────────────────────────────────────────────────┤
│                  Persistence Layer                          │
│  MongoDB (User Data, Milestones, Agent Outputs)            │
│  Redis (Sessions, Cache)                                    │
├─────────────────────────────────────────────────────────────┤
│                 Observability Layer                         │
│  Loguru Logging  │  Prometheus Metrics  │  Health Checks   │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 API Usage Examples

### Authentication
```bash
# Login
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "demo", "password": "password"}'

# Response: {"access_token": "jwt_token", "token_type": "bearer", "session_id": "session_123"}

# Access protected endpoint
curl -X GET "http://localhost:8000/api/v1/auth/me" \
  -H "Authorization: Bearer jwt_token"
```

### Agent Endpoints
```bash
# Career Agent - Job Search
curl -X POST "http://localhost:8000/api/v1/agents/career" \
  -H "Authorization: Bearer jwt_token" \
  -H "Content-Type: application/json" \
  -d '{
    "user_data": {
      "skills": ["Python", "Machine Learning"],
      "experience_years": 3,
      "location": "San Francisco"
    },
    "task_type": "job_search",
    "parameters": {
      "salary_range": [80000, 120000],
      "remote_ok": true
    }
  }'

# Finance Agent - Budget Analysis
curl -X POST "http://localhost:8000/api/v1/agents/finance" \
  -H "Authorization: Bearer jwt_token" \
  -H "Content-Type: application/json" \
  -d '{
    "user_data": {
      "income": 75000,
      "expenses": 50000,
      "age": 30
    },
    "task_type": "budget_analysis",
    "parameters": {
      "time_horizon": "5_years"
    }
  }'

# Wellness Agent - Fitness Plan
curl -X POST "http://localhost:8000/api/v1/agents/wellness" \
  -H "Authorization: Bearer jwt_token" \
  -H "Content-Type: application/json" \
  -d '{
    "user_data": {
      "age": 28,
      "weight": 70,
      "height": 175,
      "activity_level": "moderate"
    },
    "task_type": "fitness_plan",
    "parameters": {
      "workout_days": 4
    }
  }'

# Learning Agent - Course Recommendations
curl -X POST "http://localhost:8000/api/v1/agents/learning" \
  -H "Authorization: Bearer jwt_token" \
  -H "Content-Type: application/json" \
  -d '{
    "user_data": {
      "current_skills": ["Python", "SQL"],
      "interests": ["Machine Learning"],
      "learning_style": "hands_on"
    },
    "task_type": "course_recommendation",
    "parameters": {
      "budget": 500
    }
  }'
```

### Data & Milestone Management
```bash
# Create User Profile
curl -X POST "http://localhost:8000/api/v1/data/users/profile" \
  -H "Authorization: Bearer jwt_token" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "skills": ["Python", "FastAPI"],
    "experience_years": 3,
    "income": 75000
  }'

# Create Milestone
curl -X POST "http://localhost:8000/api/v1/data/milestones" \
  -H "Authorization: Bearer jwt_token" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Learn Machine Learning",
    "description": "Complete ML course and build projects",
    "category": "learning",
    "priority": 3
  }'

# Get User Progress
curl -X GET "http://localhost:8000/api/v1/data/progress" \
  -H "Authorization: Bearer jwt_token"

# Get Agent History
curl -X GET "http://localhost:8000/api/v1/data/agent-outputs?agent_type=career&limit=10" \
  -H "Authorization: Bearer jwt_token"
```

### Metrics & Monitoring
```bash
# Prometheus Metrics
curl -X GET "http://localhost:8000/metrics"

# System Health
curl -X GET "http://localhost:8000/api/v1/status"

# Agent Health Checks
curl -X GET "http://localhost:8000/api/v1/agents/career/health"
```

## 🛠️ Setup & Installation

### Prerequisites
- Python 3.11+
- MongoDB 7.0+
- Redis 7.0+
- Docker & Docker Compose (optional)

### Environment Configuration
Create `.env` file in the Backend directory:
```env
# Database
MONGODB_URL=mongodb://localhost:27017
REDIS_URL=redis://localhost:6379

# API
API_HOST=0.0.0.0
API_PORT=8000

# Authentication
JWT_SECRET_KEY=your-secret-key-change-in-production

# External APIs (Mock keys for development)
JOB_API_KEY=mock_job_key
FINANCE_API_KEY=mock_finance_key
WELLNESS_API_KEY=mock_wellness_key
LEARNING_API_KEY=mock_learning_key

# Logging
LOG_LEVEL=INFO
```

### Local Development Setup

1. **Clone and Install Dependencies**
```bash
cd Backend
pip install -r requirements.txt
```

2. **Start Required Services**
```bash
# MongoDB
docker run -d -p 27017:27017 --name mongodb mongo:7

# Redis
docker run -d -p 6379:6379 --name redis redis:7-alpine
```

3. **Run the Application**
```bash
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

4. **Access the API**
- API Documentation: http://localhost:8000/docs
- Metrics: http://localhost:8000/metrics
- Health Check: http://localhost:8000/health

### Docker Deployment

1. **Using Docker Compose**
```bash
docker-compose up -d
```

2. **Individual Container**
```bash
# Build image
docker build -t ai-life-goals .

# Run container
docker run -d -p 8000:8000 --env-file .env ai-life-goals
```

The Docker setup includes:
- FastAPI application
- MongoDB database
- Redis cache
- Automatic service orchestration

## 🧪 Testing

### Run All Tests
```bash
# Basic test run
pytest

# With coverage report
pytest --cov=Backend --cov-report=html --cov-report=term-missing

# Run specific test categories
pytest -m "not slow"  # Skip performance tests
pytest tests/test_agents.py  # Test specific module
pytest -v  # Verbose output
```

### Test Categories
- **Unit Tests**: Individual component testing
- **Integration Tests**: Multi-component interaction testing
- **Performance Tests**: Load and stress testing (marked as "slow")
- **Error Scenario Tests**: Edge cases and error handling

### Coverage Report
After running tests with coverage, open `htmlcov/index.html` to view detailed coverage report.

### Test Structure
```
tests/
├── conftest.py              # Shared fixtures and configuration
├── test_comprehensive.py    # Full endpoint testing
├── test_agents.py          # Agent functionality tests
├── test_auth.py            # Authentication tests
├── test_database.py        # Database operation tests
├── test_wellness_agent.py  # Wellness agent specific tests
├── test_learning_agent.py  # Learning agent specific tests
└── test_performance.py     # Performance and load tests
```

## 📊 Performance & Scalability

### Metrics Tracked
- API request/response times
- Agent execution duration
- Database operation performance
- Error rates and types
- Active session counts
- Memory and CPU usage

### Scalability Features
- Async/await throughout the application
- Connection pooling for databases
- Stateless agent design
- Horizontal scaling ready
- Comprehensive caching strategy

### Production Considerations
- Environment-based configuration
- Structured logging with correlation IDs
- Health checks for all components
- Graceful shutdown handling
- Error recovery mechanisms

## 🤝 Contributing

### Development Workflow
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes with tests
4. Ensure all tests pass (`pytest`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Code Standards
- Follow PEP 8 style guidelines
- Add type hints for all functions
- Write comprehensive docstrings
- Maintain test coverage above 90%
- Use structured logging for all operations

### Areas for Contribution
- Additional specialized agents
- Enhanced external API integrations
- Advanced workflow orchestration
- Machine learning model integration
- Performance optimizations

## 📞 Contact & Support

**Project Maintainer**: [Your Name]
- Email: your.email@example.com
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/yourprofile)

**Project Repository**: [GitHub Link](https://github.com/yourusername/ai-life-goals)

**Documentation**: Available in the `/docs` directory and at `/docs` endpoint when running the application.

**Issue Reporting**: Please use GitHub Issues for bug reports and feature requests.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- FastAPI for the excellent async web framework
- MongoDB and Redis for robust data storage
- Prometheus for comprehensive metrics
- The open-source community for inspiration and tools

---

**Built with ❤️ for better life goal management**