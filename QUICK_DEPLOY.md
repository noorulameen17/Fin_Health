# 🚀 QUICK DEPLOYMENT GUIDE (20 MINUTES)

## Step 1: Push to GitHub (5 minutes)

### Initialize Git and Push
```bash
# Navigate to project root
cd "c:\Users\nooru\OneDrive\Documents\VS Code\financial-health-assessment"

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Financial Health Assessment Platform"

# Add your GitHub remote (replace with your repo URL)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Push to main branch
git branch -M main
git push -u origin main
```

## Step 2: Deploy Backend to Railway (7 minutes)

### Railway Setup
1. Go to https://railway.app/
2. Sign in with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Railway will auto-detect the backend

### Backend Configuration
Add these environment variables in Railway:
```
DATABASE_URL=postgresql://user:password@host:5432/dbname
PERPLEXITY_API_KEY=your_perplexity_api_key
SECRET_KEY=your_secret_key_here
CORS_ORIGINS=https://your-frontend-url.vercel.app
```

### Backend Settings
- **Root Directory**: `backend`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

Railway will automatically provision PostgreSQL - use that DATABASE_URL!

## Step 3: Deploy Frontend to Vercel (5 minutes)

### Vercel Setup
1. Go to https://vercel.com/
2. Sign in with GitHub
3. Click "New Project"
4. Import your GitHub repository
5. Configure:
   - **Framework Preset**: Create React App
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `build`

### Frontend Environment Variables
Add in Vercel:
```
REACT_APP_API_URL=https://your-backend-url.railway.app
```

## Step 4: Update CORS (2 minutes)

After deployment, update backend `config.py`:
```python
CORS_ORIGINS = [
    "https://your-frontend.vercel.app",
    "http://localhost:3000"
]
```

Push the change:
```bash
git add backend/app/core/config.py
git commit -m "Update CORS for production"
git push
```

## Step 5: Run Database Migration (1 minute)

In Railway backend terminal:
```bash
alembic upgrade head
```

## ✅ DONE!

Your app should be live at:
- Frontend: https://your-app.vercel.app
- Backend: https://your-backend.railway.app

## 🆘 Quick Troubleshooting

**Backend not starting?**
- Check Railway logs
- Verify DATABASE_URL is set
- Ensure requirements.txt exists

**Frontend can't connect to backend?**
- Check REACT_APP_API_URL in Vercel
- Verify CORS_ORIGINS in backend config.py
- Check Railway backend URL is correct

**Database errors?**
- Run `alembic upgrade head` in Railway terminal
- Check DATABASE_URL is correct

## Alternative: Render (if Railway issues)

### Backend on Render
1. Go to https://render.com/
2. New → Web Service
3. Connect GitHub repo
4. Root Directory: `backend`
5. Build: `pip install -r requirements.txt`
6. Start: `uvicorn main:app --host 0.0.0.0 --port $PORT`
7. Add PostgreSQL database (free tier)

## Time Breakdown
- Git push: 3-5 minutes
- Railway backend: 5-7 minutes  
- Vercel frontend: 3-5 minutes
- CORS update: 1-2 minutes
- Migration: 1 minute

**Total: ~15-20 minutes**
