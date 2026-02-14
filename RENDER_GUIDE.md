# 🚀 Render Deployment Guide

Quick step-by-step guide to deploy the Autonomous Learning Agent on Render.

## Prerequisites

1. **GitHub Repository**: Push your code to GitHub
2. **MongoDB Atlas**: Create a free MongoDB cluster at [mongodb.com/cloud/atlas](https://mongodb.com/cloud/atlas)
3. **Groq API Key**: Get from [console.groq.com](https://console.groq.com/)
4. **Render Account**: Sign up at [render.com](https://render.com)

---

## Step 1: Set Up MongoDB Atlas

1. Go to [MongoDB Atlas](https://mongodb.com/cloud/atlas)
2. Create a **FREE M0 cluster**
3. Create database user:
   - Username: `learningagent`
   - Password: (use strong password)
4. Whitelist IP: Click **Network Access** → **Add IP Address** → **Allow Access from Anywhere** (0.0.0.0/0)
5. Get connection string:
   - Click **Connect** → **Connect your application**
   - Copy connection string (looks like: `mongodb+srv://user:password@cluster.mongodb.net/`)
   - Replace `<password>` with your actual password
   - Add database name: `mongodb+srv://user:password@cluster.mongodb.net/learning_agent?retryWrites=true&w=majority`

---

## Step 2: Generate Secret Key

Run this command in PowerShell to generate a secure secret key:

```powershell
python -c "import secrets; print(secrets.token_hex(32))"
```

Copy the output - you'll need it for environment variables.

---

## Step 3: Deploy Using render.yaml (Recommended)

### Option A: Automatic Deployment with Blueprint

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **New** → **Blueprint**
3. Connect your GitHub repository
4. Render will detect `render.yaml` automatically
5. Set environment variables for **backend**:
   - `MONGODB_URL`: Your MongoDB Atlas connection string
   - `SECRET_KEY`: Generated secret key from Step 2
   - `GROQ_API_KEY`: Your Groq API key
6. Set environment variables for **frontend**:
   - `VITE_API_URL`: Will be your backend URL (e.g., `https://autonomous-learning-backend.onrender.com`)
   - **Note**: After backend deploys, copy its URL and update this variable
7. Click **Apply** and wait for deployment

---

## Step 4: Deploy Manually (Alternative)

If you prefer manual setup:

### Deploy Backend

1. Go to Render Dashboard → **New** → **Web Service**
2. Connect your GitHub repository
3. Configure:
   - **Name**: `autonomous-learning-backend`
   - **Region**: Choose closest to you
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Add Environment Variables:
   ```
   MONGODB_URL=mongodb+srv://user:password@cluster.mongodb.net/learning_agent?retryWrites=true&w=majority
   SECRET_KEY=your_generated_secret_key_here
   GROQ_API_KEY=gsk_your_groq_api_key_here
   ```
5. Click **Create Web Service**
6. **Copy the backend URL** (e.g., `https://autonomous-learning-backend.onrender.com`)

### Deploy Frontend

1. Go to Render Dashboard → **New** → **Static Site**
2. Connect the same GitHub repository
3. Configure:
   - **Name**: `autonomous-learning-frontend`
   - **Root Directory**: `frontend`
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `dist`
4. Add Environment Variable:
   ```
   VITE_API_URL=https://autonomous-learning-backend.onrender.com
   ```
   (Use the backend URL from previous step)
5. Click **Create Static Site**

---

## Step 5: Update CORS Settings (After First Deploy)

After your frontend deploys, update backend CORS:

1. Copy your frontend URL (e.g., `https://autonomous-learning-frontend.onrender.com`)
2. Edit `backend/main.py` line 25:
   ```python
   allow_origins=["*"],  # Update this to your frontend URL for security
   ```
   Change to:
   ```python
   allow_origins=[
       "http://localhost:5173",  # For local development
       "https://your-frontend-url.onrender.com"  # Your deployed frontend
   ],
   ```
3. Commit and push to GitHub - Render will auto-redeploy

---

## Step 6: Test Your Deployment

1. Visit your frontend URL
2. Register a new account
3. Login
4. Test the learning flow:
   - Enter a topic (e.g., "Python")
   - Read the explanation
   - Take the quiz
   - View results
   - Check progress page

---

## 🎉 You're Done!

Your application is now live on Render!

- **Frontend**: `https://your-frontend.onrender.com`
- **Backend**: `https://your-backend.onrender.com`
- **API Docs**: `https://your-backend.onrender.com/docs`

---

## ⚠️ Important Notes

### Free Tier Limitations
- Services **sleep after 15 minutes** of inactivity
- First request after sleep takes ~30-60 seconds (cold start)
- 750 hours/month free (enough for 1 service running 24/7)

### Keeping Services Awake
To prevent sleeping (optional):
1. Use [UptimeRobot](https://uptimerobot.com/) to ping your backend every 10 minutes
2. Or upgrade to paid plan ($7/month) for always-on services

### MongoDB Connection Issues
If backend fails to connect:
- Verify IP whitelist is set to `0.0.0.0/0`
- Check connection string format
- Ensure password doesn't have special characters (or URL-encode them)

### Build Failures
If build fails:
- Check logs in Render dashboard
- Verify `requirements.txt` and `package.json` are correct
- Ensure Python 3.11+ and Node 18+ are being used

---

## Troubleshooting

### Backend Health Check Fails
- Check environment variables are set correctly
- Verify MongoDB connection string
- Check logs: Dashboard → Service → Logs

### Frontend Can't Connect to Backend
- Verify `VITE_API_URL` environment variable is set correctly
- Check CORS settings in `backend/main.py`
- Clear browser cache and try again

### 502 Bad Gateway
- Service is likely sleeping (free tier) - wait 30-60 seconds and retry
- Or service crashed - check logs

---

## Need Help?

1. Check Render logs for error messages
2. Verify all environment variables are set
3. Test backend health: `https://your-backend.onrender.com/`
4. Test API docs: `https://your-backend.onrender.com/docs`
