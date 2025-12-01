# Goalstone – AI Life Goals Management System

An AI-powered life goals and milestones planner that helps you transform dreams into achievable roadmaps with personalized guidance across career, finance, wellness, and learning.

A modern web application for managing life goals with AI-powered assistance.

---

## 🚀 Features

- User registration and authentication
- Secure password hashing
- Persistent user data storage
- Responsive design
- Production-ready deployment
- AI guidance across:
  - Career
  - Finance
  - Wellness
  - Learning

---

## ⚙️ Quick Start

### 🔧 Backend (FastAPI / Python)

```bash
cd Backend
pip install -r requirements.txt
uvicorn app:app --reload --port 8080
   ```

2. **Frontend**:
   ```bash
   cd Frontend
   npm install
   npm run dev
   ```

### Production Deployment

Using Docker Compose:

```bash
docker-compose up --build
```

The application will be available at:
- Frontend: http://localhost
- Backend API: http://localhost:8080

## Deployment Options

### 1. Vercel (Frontend) + Railway (Backend)
- Deploy frontend to Vercel
- Deploy backend to Railway
- Update API URLs in frontend

### 2. Netlify (Frontend) + Heroku (Backend)
- Deploy frontend to Netlify
- Deploy backend to Heroku
- Configure environment variables

### 3. AWS/Azure/GCP
- Use container services
- Deploy with docker-compose
- Configure load balancers

## Environment Variables

Backend:
- `PORT`: Server port (default: 8080)
- `HOST`: Server host (default: 0.0.0.0)

Frontend:
- `VITE_API_URL`: Backend API URL

## Security Features

- Password hashing with SHA-256
- CORS protection
- Input validation
- Secure token-based authentication
