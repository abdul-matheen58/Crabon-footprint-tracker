# ──────────────────────────────────────────────────────────
#  Carbon Footprint Platform
#  Smart carbon footprint tracking with AI assistant
# ──────────────────────────────────────────────────────────

## 🌍 Project Overview

The Carbon Footprint Platform is a full-stack web application designed to help users track, understand, and reduce their carbon footprint. It features:

- 📊 **Real-time Emission Tracking** - Log activities and see immediate carbon impact
- 🎯 **Goal Setting** - Set and track carbon reduction goals
- 💡 **Smart Tips** - AI-powered suggestions for reducing emissions
- 🤖 **AI Assistant** - Chat-based guidance on sustainability
- 📈 **Analytics Dashboard** - Visualize emissions trends
- 🔐 **Secure Authentication** - User accounts with JWT tokens

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)

**Windows:**
```bash
setup.bat
```

**macOS/Linux:**
```bash
bash setup.sh
```

### Option 2: Manual Setup

See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed instructions.

## 📁 Project Structure

```
carbon-footprint-platform/
├── backend/                    # FastAPI application
│   ├── main.py                # Entry point
│   ├── config.py              # Configuration
│   ├── database.py            # Database setup
│   ├── requirements.txt       # Dependencies
│   ├── models/                # Database models
│   ├── routers/               # API endpoints
│   ├── schemas/               # Request/response schemas
│   ├── services/              # Business logic
│   └── tests/                 # Unit tests
├── frontend/                   # Next.js application
│   ├── package.json           # Dependencies
│   ├── src/
│   │   ├── app/               # Pages and layout
│   │   ├── components/        # React components
│   │   ├── lib/               # Utilities
│   │   └── styles/            # CSS files
│   └── Dockerfile             # Docker configuration
├── docker-compose.yml         # Multi-container setup
├── DEPLOYMENT.md              # Complete deployment guide
└── README.md                  # This file
```

## 🏗️ Architecture

### Backend Stack
- **Framework**: FastAPI
- **Database**: SQLite (dev) / PostgreSQL (production)
- **Authentication**: JWT tokens
- **ORM**: SQLAlchemy 2.0
- **Async**: AsyncIO + aiosqlite

### Frontend Stack
- **Framework**: Next.js 14
- **UI Library**: React 18
- **Styling**: Tailwind CSS
- **State Management**: Zustand
- **HTTP Client**: Axios + SWR
- **UI Components**: Lucide React, Recharts

## 🔧 Requirements

- Python 3.13+
- Node.js 18+
- npm or yarn
- Docker (optional, for containerized deployment)

## 📖 API Documentation

Once the backend is running, visit: `http://localhost:8000/docs`

This provides an interactive API explorer powered by Swagger UI.

### Key Endpoints

- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `GET /api/emissions` - List user emissions
- `POST /api/emissions` - Log new emission
- `GET /api/analytics` - Get analytics data
- `GET /api/tips` - Get sustainability tips
- `POST /api/goals` - Create goals
- `POST /api/chat` - Chat with AI assistant

## 🧪 Testing

### Backend Tests
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
pytest
pytest --cov  # With coverage
```

### Frontend Tests
```bash
cd frontend
npm test
npm run test:coverage
```

## 🐳 Docker Deployment

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

Services will be available at:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

## ☁️ Production Deployment

See [DEPLOYMENT.md](./DEPLOYMENT.md) for comprehensive deployment guides including:
- Heroku
- AWS
- DigitalOcean
- Docker
- Vercel

## 🔐 Security

### Environment Variables

All sensitive configuration is managed via environment variables:

**Backend (.env)**
```env
SECRET_KEY=your-secret-key
DATABASE_URL=your-database-url
CORS_ORIGINS=http://localhost:3000
```

**Frontend (.env.local)**
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**Never commit `.env` files** - use `.env.example` templates instead.

## 📝 Development Workflow

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature
   ```

2. **Make changes**
   - Backend: Update models, routers, services
   - Frontend: Update components, pages

3. **Test**
   ```bash
   # Backend
   cd backend && pytest

   # Frontend
   cd frontend && npm test
   ```

4. **Commit and push**
   ```bash
   git add .
   git commit -m "Add: your feature description"
   git push origin feature/your-feature
   ```

5. **Create Pull Request**

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check if port 8000 is in use
lsof -i :8000
# Kill the process
kill -9 <PID>
```

### Frontend showing blank page
- Check `NEXT_PUBLIC_API_URL` in `.env.local`
- Verify backend is running
- Check browser console for errors

### Database errors
```bash
# Reset database (development only)
rm backend/carbon_footprint.db
# Restart backend to reinitialize
```

See [DEPLOYMENT.md](./DEPLOYMENT.md#-troubleshooting) for more solutions.

## 📚 Documentation

- [Deployment Guide](./DEPLOYMENT.md)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

## 🎯 Project Status

- ✅ Core functionality (emission tracking, goals)
- ✅ Authentication system
- ✅ Analytics dashboard
- ✅ AI assistant integration
- ✅ Docker support
- 🔄 Deployment automation
- 📋 CI/CD pipeline setup

## 📄 License

This project is provided for evaluation purposes.

## 👥 Support

For issues, questions, or suggestions:
1. Check the [DEPLOYMENT.md](./DEPLOYMENT.md) troubleshooting section
2. Review API docs at `/docs`
3. Check backend logs for errors
4. Verify all environment variables are set

---

**Version**: 1.0.0  
**Last Updated**: 2024
