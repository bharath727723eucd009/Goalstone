# Docker Deployment Guide

## Quick Start

### Development Environment
```bash
# Clone and setup
git clone <repository-url>
cd Backend

# Copy environment file
cp .env.example .env

# Start development environment
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up -d

# View logs
docker-compose logs -f api
```

### Production Environment
```bash
# Set production environment variables
export JWT_SECRET_KEY="your-production-secret-key"
export MONGODB_USERNAME="admin"
export MONGODB_PASSWORD="secure-password"
export REDIS_PASSWORD="secure-redis-password"

# Start production environment
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Check status
docker-compose ps
```

## Environment Variables

### Required for Production
```env
JWT_SECRET_KEY=your-production-secret-key
MONGODB_USERNAME=admin
MONGODB_PASSWORD=secure-mongodb-password
REDIS_PASSWORD=secure-redis-password
```

### Optional Configuration
```env
API_PORT=8000
MONGODB_PORT=27017
REDIS_PORT=6379
LOG_LEVEL=INFO
PROMETHEUS_PORT=9090
GRAFANA_PORT=3000
GRAFANA_PASSWORD=admin
```

## Service Architecture

### Core Services
- **api**: FastAPI application (Port 8000)
- **mongodb**: MongoDB database (Port 27017)
- **redis**: Redis cache (Port 6379)

### Monitoring Services (Optional)
```bash
# Start with monitoring
docker-compose --profile monitoring up -d

# Access monitoring
# Prometheus: http://localhost:9090
# Grafana: http://localhost:3000 (admin/admin)
```

## Volume Management

### Persistent Data
- `mongodb_data`: MongoDB database files
- `redis_data`: Redis persistence files
- `app_logs`: Application log files

### Backup Data
```bash
# Backup MongoDB
docker-compose exec mongodb mongodump --out /data/backup

# Backup Redis
docker-compose exec redis redis-cli BGSAVE
```

## Network Configuration

### Internal Network
- Network: `ai-goals-network`
- Driver: bridge
- Services communicate via service names

### Port Mapping
- API: `localhost:8000`
- MongoDB: `localhost:27017` (dev only)
- Redis: `localhost:6379` (dev only)
- Prometheus: `localhost:9090` (monitoring)
- Grafana: `localhost:3000` (monitoring)

## Health Checks

### Service Health
```bash
# Check all services
docker-compose ps

# Check API health
curl http://localhost:8000/health

# Check individual service logs
docker-compose logs api
docker-compose logs mongodb
docker-compose logs redis
```

### Application Health
- API Health: `GET /health`
- Metrics: `GET /metrics`
- Agent Status: `GET /api/v1/status`

## Scaling

### Horizontal Scaling
```bash
# Scale API service
docker-compose up -d --scale api=3

# Use load balancer (nginx example)
docker-compose -f docker-compose.yml -f docker-compose.scale.yml up -d
```

### Resource Limits
Production configuration includes:
- CPU limits and reservations
- Memory limits and reservations
- Restart policies

## Troubleshooting

### Common Issues

**MongoDB Connection Failed**
```bash
# Check MongoDB logs
docker-compose logs mongodb

# Verify network connectivity
docker-compose exec api ping mongodb
```

**Redis Connection Failed**
```bash
# Check Redis logs
docker-compose logs redis

# Test Redis connection
docker-compose exec redis redis-cli ping
```

**API Not Starting**
```bash
# Check API logs
docker-compose logs api

# Verify environment variables
docker-compose exec api env | grep -E "(MONGODB|REDIS|JWT)"
```

### Debug Mode
```bash
# Start with debug logging
LOG_LEVEL=DEBUG docker-compose up -d

# Access container shell
docker-compose exec api bash

# View real-time logs
docker-compose logs -f --tail=100 api
```

## Security Considerations

### Production Security
- Change default passwords
- Use strong JWT secret keys
- Enable Redis authentication
- Configure MongoDB authentication
- Use HTTPS in production
- Implement network security groups

### Environment Isolation
- Use separate .env files for different environments
- Never commit secrets to version control
- Use Docker secrets for sensitive data
- Implement proper access controls

## Maintenance

### Updates
```bash
# Pull latest images
docker-compose pull

# Restart services
docker-compose up -d

# Clean unused resources
docker system prune -f
```

### Monitoring
- Monitor container resource usage
- Set up log aggregation
- Configure alerting for service failures
- Regular backup procedures