# 🚀 Deployment Guide - Autonomous Learning Agent

This guide provides step-by-step instructions for deploying your Autonomous Learning Agent project to various platforms.

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Development Deployment](#local-development-deployment)
3. [Production Deployment Options](#production-deployment-options)
   - [Option 1: Render (Recommended for Beginners)](#option-1-render-recommended)
   - [Option 2: Railway](#option-2-railway)
   - [Option 3: Vercel + Render](#option-3-vercel--render)
   - [Option 4: Docker Deployment](#option-4-docker-deployment)
4. [MongoDB Setup](#mongodb-setup)
5. [Environment Variables](#environment-variables)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before deploying, ensure you have:

- ✅ **Python 3.8+** installed
- ✅ **Node.js 16+** installed
- ✅ **Git** installed
- ✅ **Groq API Key** (Get from [https://console.groq.com/](https://console.groq.com/))
- ✅ **MongoDB** (Local or MongoDB Atlas account)

---

## Local Development Deployment

### Step 1: Clone the Repository (if not already done)

```bash
cd c:\Users\govin\Desktop\Autonomous-Learning-Agent
```

### Step 2: Set Up MongoDB

#### Option A: Local MongoDB
1. Download and install MongoDB from [mongodb.com/try/download/community](https://www.mongodb.com/try/download/community)
2. Start MongoDB service:
   ```bash
   # Windows
   net start MongoDB
   ```

#### Option B: MongoDB Atlas (Cloud - Recommended)
1. Go to [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
2. Create a free account
3. Create a new cluster (M0 Free Tier)
4. Click "Connect" → "Connect your application"
5. Copy the connection string (looks like: `mongodb+srv://username:password@cluster.mongodb.net/`)

### Step 3: Configure Backend Environment

1. Navigate to backend directory:
   ```bash
   cd backend
   ```

2. Create `.env` file:
   ```bash
   copy .env.example .env
   ```

3. Edit `.env` file and add your credentials:
   ```env
   MONGODB_URL=mongodb://localhost:27017
   # OR for MongoDB Atlas:
   # MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/learning_agent?retryWrites=true&w=majority
   
   SECRET_KEY=your-secret-key-here-use-strong-random-string
   GROQ_API_KEY=your_groq_api_key_here
   ```

   > **💡 Tip**: Generate a secure SECRET_KEY using:
   > ```bash
   > python -c "import secrets; print(secrets.token_hex(32))"
   > ```

4. Create Python virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

5. Install backend dependencies:
   ```bash
   pip install -r requirements.txt
   ```

6. Start the backend server:
   ```bash
   cd backend
   uvicorn main:app --reload --port 8000
   ```

   ✅ Backend should now be running at `http://localhost:8000`

### Step 4: Configure and Run Frontend

1. Open a **new terminal** and navigate to frontend:
   ```bash
   cd c:\Users\govin\Desktop\Autonomous-Learning-Agent\frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

   ✅ Frontend should now be running at `http://localhost:5173`

### Step 5: Test the Application

1. Open your browser and go to `http://localhost:5173`
2. Register a new account
3. Login and test the learning features

---

## Production Deployment Options

### Option 1: Render (Recommended)

Render offers free hosting for web services with easy deployment.

#### Step 1: Prepare Your Repository

1. Make sure your code is pushed to GitHub:
   ```bash
   git add .
   git commit -m "Prepare for deployment"
   git push origin main
   ```

#### Step 2: Deploy Backend on Render

1. Go to [render.com](https://render.com) and sign up
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure the backend service:
   - **Name**: `autonomous-learning-backend`
   - **Region**: Choose closest to you
   - **Root Directory**: `backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Instance Type**: Free

5. Add environment variables (click "Advanced" → "Add Environment Variable"):
   ```
   MONGODB_URL=your_mongodb_atlas_connection_string
   SECRET_KEY=your_generated_secret_key
   GROQ_API_KEY=your_groq_api_key
   ```

6. Click **"Create Web Service"**
7. Wait for deployment (5-10 minutes)
8. Copy the service URL (e.g., `https://autonomous-learning-backend.onrender.com`)

#### Step 3: Deploy Frontend on Render

1. Click **"New +"** → **"Static Site"**
2. Connect the same GitHub repository
3. Configure the frontend:
   - **Name**: `autonomous-learning-frontend`
   - **Root Directory**: `frontend`
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `dist`

4. Add environment variable:
   ```
   VITE_API_URL=https://autonomous-learning-backend.onrender.com
   ```

5. **IMPORTANT**: Update frontend API configuration
   - Before deploying, update `frontend/src` to use the backend URL

6. Click **"Create Static Site"**

#### Step 4: Update CORS Settings

After deployment, update your backend's `main.py` CORS settings:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "https://your-frontend-url.onrender.com"  # Add your frontend URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

### Option 2: Railway

Railway offers $5 free credit per month.

#### Deploy Backend

1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click **"New Project"** → **"Deploy from GitHub repo"**
4. Select your repository
5. Add environment variables (same as Render)
6. Railway will auto-detect Python and deploy

#### Deploy Frontend

1. In the same project, click **"New Service"**
2. Select the same repository
3. Configure build settings for frontend
4. Deploy

---

### Option 3: Vercel + Render

Use Vercel for frontend (better for React) and Render for backend.

#### Deploy Frontend on Vercel

1. Go to [vercel.com](https://vercel.com)
2. Sign up with GitHub
3. Click **"Add New Project"**
4. Import your repository
5. Configure:
   - **Framework Preset**: Vite
   - **Root Directory**: frontend
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
6. Add environment variable:
   ```
   VITE_API_URL=your_backend_url
   ```
7. Deploy

#### Deploy Backend on Render
(Follow Option 1 Step 2)

---

### Option 4: Docker Deployment

For those who want to use Docker for containerized deployment.

#### Step 1: Create Dockerfiles

I'll create Docker configuration files for you in the next steps.

#### Step 2: Build and Run

```bash
# Build and run with Docker Compose
docker-compose up --build
```

---

## MongoDB Setup

### MongoDB Atlas Setup (Recommended for Production)

1. **Create Account**: Go to [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
2. **Create Cluster**:
   - Choose **M0 Free Tier**
   - Select region closest to your users
   - Click "Create Cluster"
3. **Create Database User**:
   - Go to "Database Access"
   - Click "Add New Database User"
   - Choose "Password" authentication
   - Set username and strong password
   - Set role to "Read and write to any database"
4. **Whitelist IP**:
   - Go to "Network Access"
   - Click "Add IP Address"
   - Choose "Allow Access from Anywhere" (0.0.0.0/0) for now
   - In production, restrict to your server's IP
5. **Get Connection String**:
   - Go to "Clusters" → Click "Connect"
   - Choose "Connect your application"
   - Copy the connection string
   - Replace `<password>` with your database user password
   - Add database name: `mongodb+srv://username:password@cluster.mongodb.net/learning_agent?retryWrites=true&w=majority`

---

## Environment Variables

### Backend Environment Variables (.env)

```env
# MongoDB Connection
MONGODB_URL=mongodb+srv://user:pass@cluster.mongodb.net/learning_agent?retryWrites=true&w=majority

# JWT Secret (Generate with: python -c "import secrets; print(secrets.token_hex(32))")
SECRET_KEY=your_64_character_secret_key_here

# Groq API Key (Get from https://console.groq.com/)
GROQ_API_KEY=gsk_your_groq_api_key_here
```

### Frontend Environment Variables

Create `frontend/.env`:

```env
VITE_API_URL=http://localhost:8000
# For production, change to your deployed backend URL:
# VITE_API_URL=https://your-backend.onrender.com
```

> **Note**: You'll need to update the frontend code to use this environment variable. Create an API configuration file.

---

## Troubleshooting

### Common Issues

#### 1. **CORS Errors**
- **Problem**: Frontend can't connect to backend
- **Solution**: Update `backend/main.py` CORS settings to include your frontend URL

#### 2. **MongoDB Connection Failed**
- **Problem**: Backend can't connect to MongoDB
- **Solutions**:
  - Check MongoDB Atlas IP whitelist
  - Verify connection string format
  - Ensure password doesn't contain special characters (URL encode if needed)
  - Check MongoDB cluster is running

#### 3. **Module Not Found Errors**
- **Problem**: Missing Python packages
- **Solution**: 
  ```bash
  pip install -r backend/requirements.txt
  ```

#### 4. **Port Already in Use**
- **Problem**: Port 8000 or 5173 already in use
- **Solution**:
  ```bash
  # For backend, use different port:
  uvicorn main:app --port 8001
  
  # For frontend, Vite will automatically suggest next available port
  ```

#### 5. **Build Errors on Deployment Platform**
- **Problem**: Build fails on Render/Vercel
- **Solutions**:
  - Check Python/Node version requirements
  - Verify all dependencies in requirements.txt/package.json
  - Check build logs for specific errors

#### 6. **Groq API Errors**
- **Problem**: LLM not working
- **Solutions**:
  - Verify GROQ_API_KEY is correct
  - Check API quota/limits at console.groq.com
  - Test API key with a simple request

### Get Help

- Check the logs:
  - **Render**: Click on service → "Logs" tab
  - **Railway**: Click on deployment → "Build Logs"
  - **Local**: Check terminal output
- Review README.md for setup instructions
- Check MongoDB connection status

---

## Quick Deployment Checklist

Before deploying to production:

- [ ] MongoDB Atlas cluster created and configured
- [ ] Database user created with strong password
- [ ] IP whitelist configured (0.0.0.0/0 for testing, specific IPs for production)
- [ ] Groq API key obtained from console.groq.com
- [ ] SECRET_KEY generated using secure random method
- [ ] All environment variables configured correctly
- [ ] CORS settings updated with production frontend URL
- [ ] Code pushed to GitHub repository
- [ ] Frontend environment variable for API URL configured
- [ ] Test registration, login, and learning flow after deployment
- [ ] Monitor logs for any errors

---

## Next Steps After Deployment

1. **Domain Setup** (Optional):
   - Most platforms allow custom domains
   - Configure DNS settings
   - Enable HTTPS (usually automatic)

2. **Monitoring**:
   - Check application logs regularly
   - Monitor MongoDB usage
   - Track API usage

3. **Security**:
   - Use strong SECRET_KEY
   - Restrict MongoDB IP whitelist in production
   - Keep dependencies updated
   - Use environment-specific configurations

4. **Scaling**:
   - Monitor response times
   - Consider upgrading to paid tiers if needed
   - Implement caching for better performance

---

## Platform Comparison

| Platform | Backend | Frontend | Free Tier | Pros | Cons |
|----------|---------|----------|-----------|------|------|
| **Render** | ✅ | ✅ | Yes | Easy setup, auto-deploy | Free tier sleeps after inactivity |
| **Railway** | ✅ | ✅ | $5 credit | Fast deploys, good DX | Credit-based |
| **Vercel** | ❌ | ✅ | Yes | Best for Next.js/React | Backend needs separate hosting |
| **Railway** | ✅ | ✅ | $5 credit | Simple, good logs | Limited free tier |
| **Docker** | ✅ | ✅ | N/A | Full control, portable | Requires server/VPS |

---

## Support

If you encounter any issues during deployment, please:
1. Check the troubleshooting section
2. Review platform-specific documentation
3. Check environment variables are set correctly
4. Review application logs for error messages

Good luck with your deployment! 🚀
