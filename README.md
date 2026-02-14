# Autonomous Learning Agent - Extended Version

A full-stack AI-powered adaptive learning platform with authentication, progress tracking, and a professional UI.

## Features

- 🔐 **JWT Authentication** - Secure user registration and login
- 🧠 **AI-Powered Learning** - LLM-generated explanations and quizzes
- 📊 **Progress Tracking** - MongoDB-based attempt history and statistics
- 🎯 **70% Mastery Rule** - Clear learning objectives
- 🔄 **Smart Reteaching** - Feynman technique-based re-explanations
- 📈 **Dashboard Analytics** - Track your learning journey
- 🎨 **Professional UI** - Modern, clean Tailwind CSS design

## Tech Stack

### Backend
- FastAPI
- MongoDB (motor async driver)
- JWT Authentication (python-jose)
- Password hashing (bcrypt)
- LangChain + Groq LLM

### Frontend
- React 18
- React Router v6
- Axios
- Tailwind CSS
- Lucide React (icons)
- Framer Motion (animations)

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 16+
- MongoDB (local or Atlas)
- Groq API Key

### Quick Local Setup

For local development, follow these steps. For **production deployment to Render**, see [RENDER_GUIDE.md](RENDER_GUIDE.md).

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file:
```bash
cp .env.example .env
```

4. Update `.env` with your configuration:
```
MONGODB_URL=mongodb://localhost:27017
SECRET_KEY=your-secret-key-here
GROQ_API_KEY=your-groq-api-key
```

5. Start the backend server:
```bash
uvicorn main:app --reload --port 8000
```

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

4. Open browser at `http://localhost:5173`

## 🚀 Production Deployment

See [RENDER_GUIDE.md](RENDER_GUIDE.md) for step-by-step instructions to deploy to Render (free hosting).

## Usage Flow

1. **Register/Login** - Create an account or login
2. **Dashboard** - View your progress statistics
3. **Learn** - Select a topic and read the AI-generated explanation
4. **Quiz** - Take a 10-question quiz on the topic
5. **Results** - See your score and get reteaching if needed
6. **Progress** - View detailed attempt history

## API Endpoints

### Authentication
- `POST /register` - Create new user
- `POST /token` - Login (returns JWT)
- `GET /users/me` - Get current user info

### Learning (Protected)
- `POST /explain` - Get AI explanation for topic
- `POST /generate-quiz` - Generate 10 MCQs
- `POST /evaluate` - Submit quiz answers
- `POST /reteach` - Get simplified re-explanation
- `GET /progress` - Get user's attempt history

## Business Rules

- ✅ Maximum 3 attempts per topic per user
- ✅ 70% score required to pass
- ✅ Relevance score always 100 (as required)
- ✅ JWT token expires in 30 minutes
- ✅ All learning endpoints require authentication

## Project Structure

```
Autonomous-Learning-Agent/
├── backend/
│   ├── main.py              # FastAPI app + routes
│   ├── auth.py              # JWT & password utilities
│   ├── database.py          # MongoDB connection
│   ├── models.py            # Pydantic models
│   ├── context_manager.py   # LLM logic (preserved)
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/      # Reusable UI components
│   │   ├── context/         # Auth context
│   │   ├── pages/           # All route pages
│   │   ├── App.jsx          # Main router
│   │   └── index.css        # Tailwind styles
│   └── package.json
└── README.md
```

## License

MIT
