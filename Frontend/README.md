# AI Life Goals - Frontend

Modern React frontend for the AI Life Goal Management System built with Vite, Tailwind CSS, and TypeScript.

## Features

- **Modern UI**: Clean, responsive design with Tailwind CSS
- **Authentication**: JWT-based auth with protected routes
- **Agent Integration**: Interactive forms for all 4 AI agents
- **Real-time Dashboard**: Stats, activity, and health monitoring
- **State Management**: React Context for auth and data
- **Error Handling**: Toast notifications and loading states
- **Mobile Responsive**: Works on all device sizes

## Tech Stack

- **React 18** - UI framework
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **React Router** - Client-side routing
- **React Hook Form** - Form handling and validation
- **Axios** - HTTP client with interceptors
- **Heroicons** - Beautiful SVG icons
- **React Hot Toast** - Toast notifications

## Getting Started

### Prerequisites
- Node.js 16+ and npm
- Backend API running on http://localhost:8000

### Installation

1. **Install dependencies**
```bash
npm install
```

2. **Start development server**
```bash
npm run dev
```

3. **Open browser**
Navigate to http://localhost:3000

### Demo Login
- Username: `demo`
- Password: `password`

## Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── Header.jsx      # Navigation header
│   ├── StatsCard.jsx   # Dashboard stats cards
│   └── AgentForm.jsx   # Dynamic agent forms
├── pages/              # Page components
│   ├── Dashboard.jsx   # Main dashboard
│   ├── Agents.jsx      # Agent selection and forms
│   └── Login.jsx       # Authentication
├── hooks/              # Custom React hooks
│   └── useAuth.js      # Authentication context
├── services/           # API services
│   └── api.js          # Axios configuration and endpoints
├── utils/              # Utility functions
└── App.jsx             # Main app component
```

## API Integration

The frontend connects to the FastAPI backend with:

- **Authentication**: JWT tokens with automatic refresh
- **Agent Endpoints**: Career, Finance, Wellness, Learning
- **Data Management**: User profiles, milestones, progress
- **Error Handling**: Automatic retry and user feedback

### API Configuration

```javascript
// Base URL configuration
const API_BASE_URL = 'http://localhost:8000/api/v1'

// Automatic token injection
api.interceptors.request.use((config) => {
  const token = getToken()
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})
```

## Components

### AgentForm
Dynamic form component that adapts to different agent types:
- **Career**: Skills, experience, location
- **Finance**: Income, expenses, goals
- **Wellness**: Age, weight, activity level
- **Learning**: Skills, interests, learning style

### StatsCard
Reusable dashboard card with:
- Loading states
- Trend indicators
- Icon support
- Responsive design

### Header
Navigation component with:
- Responsive mobile menu
- User profile dropdown
- Active route highlighting
- Logout functionality

## Styling

### Tailwind Configuration
Custom theme with:
- Brand colors (primary, success, warning, danger)
- Custom animations
- Component utilities

### CSS Classes
```css
.btn-primary     /* Primary button style */
.btn-secondary   /* Secondary button style */
.card           /* Card container */
.input-field    /* Form input styling */
.loading-spinner /* Loading animation */
```

## State Management

### Authentication Context
```javascript
const { user, loading, isAuthenticated, login, logout } = useAuth()
```

### API State
- Loading states for all async operations
- Error handling with toast notifications
- Optimistic updates where appropriate

## Development

### Available Scripts
```bash
npm run dev      # Start development server
npm run build    # Build for production
npm run preview  # Preview production build
```

### Environment Variables
Create `.env.local` for custom configuration:
```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

### Code Style
- ESLint configuration for code quality
- Prettier for consistent formatting
- Component-based architecture
- Custom hooks for reusable logic

## Deployment

### Build for Production
```bash
npm run build
```

### Deploy Options
- **Vercel**: Connect GitHub repo for automatic deployments
- **Netlify**: Drag and drop `dist` folder
- **AWS S3**: Static website hosting
- **Docker**: Use provided Dockerfile

### Environment Configuration
Set production API URL:
```env
VITE_API_BASE_URL=https://your-api-domain.com/api/v1
```

## Contributing

1. Follow the existing code structure
2. Use TypeScript for new components
3. Add proper error handling
4. Include loading states
5. Test on mobile devices
6. Update documentation

## License

MIT License - see LICENSE file for details