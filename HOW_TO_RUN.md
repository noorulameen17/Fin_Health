# 🚀 How to Run the Financial Health Assessment App

## Prerequisites

✅ Python 3.13 installed
✅ Node.js 16+ installed
✅ PostgreSQL 14+ installed and running

---

## 📋 Step-by-Step Setup

### 1️⃣ Install Backend Dependencies

```cmd
cd backend
venv\Scripts\activate
install-packages.bat
```

**Wait for all packages to install.** This will take a few minutes.

---

### 2️⃣ Configure Environment Variables

```cmd
copy .env.example .env
notepad .env
```

**Edit the `.env` file with your settings:**

```env
# Database (IMPORTANT: Use postgresql+psycopg:// format)
DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/financial_health

# AI API Keys (Get from respective platforms)
OPENAI_API_KEY=sk-your-openai-api-key-here
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here

# Security Keys (Generate random strings)
SECRET_KEY=your-secret-key-minimum-32-characters-long
ENCRYPTION_KEY=your-encryption-key-32-chars-exactly

# Banking APIs (Optional)
RAZORPAY_KEY_ID=your-razorpay-key
RAZORPAY_KEY_SECRET=your-razorpay-secret
STRIPE_API_KEY=your-stripe-key
```

**To generate SECRET_KEY and ENCRYPTION_KEY:**

```cmd
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Run this twice to get two different keys.

---

### 3️⃣ Setup PostgreSQL Database

**Option A: Using psql command line**

```cmd
psql -U postgres
CREATE DATABASE financial_health;
\q
```

**Option B: Using pgAdmin**

1. Open pgAdmin
2. Right-click on "Databases" → Create → Database
3. Name: `financial_health`
4. Click Save

---

### 4️⃣ Run Database Migrations

```cmd
cd backend
venv\Scripts\activate
alembic upgrade head
```

This creates all the necessary tables in your database.

---

### 5️⃣ Start the Backend Server

```cmd
cd backend
venv\Scripts\activate
python main.py
```

You should see:

```
INFO:     Started server process
INFO:     Uvicorn running on http://127.0.0.1:8000
```

**Keep this terminal open!** The backend is now running.

---

### 6️⃣ Install Frontend Dependencies

**Open a NEW terminal window:**

```cmd
cd frontend
npm install
```

This will take a few minutes to download all React dependencies.

---

### 7️⃣ Start the Frontend

```cmd
cd frontend
npm start
```

Your browser should automatically open to `http://localhost:3000`

---

## 🎯 Quick Start (After Initial Setup)

Once everything is set up, you only need to run:

**Terminal 1 (Backend):**

```cmd
cd backend
venv\Scripts\activate
python main.py
```

**Terminal 2 (Frontend):**

```cmd
cd frontend
npm start
```

---

## 🧪 Testing the Application

### 1. Create a Company

1. Go to http://localhost:3000
2. Click "Add New Company"
3. Fill in the company details
4. Click "Create Company"

### 2. Upload Financial Data

1. Click on the company you just created
2. Click "Upload Document"
3. Select the sample file: `sample-data/sample_financial_data.csv`
4. Click "Process Document"

### 3. Generate Assessment

1. Click "Generate Assessment"
2. Wait for AI analysis to complete
3. View financial metrics, insights, and recommendations

---

## 🔧 Troubleshooting

### Backend won't start

**Error:** `ModuleNotFoundError: No module named 'fastapi'`

- **Solution:** Run `install-packages.bat` again

**Error:** `connection refused` or database errors

- **Solution:** Make sure PostgreSQL is running and DATABASE_URL is correct

### Frontend won't start

**Error:** `npm: command not found`

- **Solution:** Install Node.js from https://nodejs.org/

**Error:** `Cannot find module`

- **Solution:** Run `npm install` in the frontend folder

### Database migration fails

**Error:** `alembic.util.exc.CommandError`

- **Solution:** Make sure your `.env` has the correct DATABASE_URL format:
  ```
  DATABASE_URL=postgresql+psycopg://postgres:password@localhost:5432/financial_health
  ```

---

## 📝 API Documentation

Once the backend is running, visit:

- **Swagger UI:** http://127.0.0.1:8000/docs
- **ReDoc:** http://127.0.0.1:8000/redoc

---

## 🌐 Application URLs

- **Frontend:** http://localhost:3000
- **Backend API:** http://127.0.0.1:8000
- **API Docs:** http://127.0.0.1:8000/docs
- **Health Check:** http://127.0.0.1:8000/health

---

## 📊 Sample Data

Use the provided sample data for testing:

- **Location:** `sample-data/sample_financial_data.csv`
- **Contents:** 3 months of financial transactions (Jan-Mar 2025)
- **Format:** Date, Description, Amount, Type, Category

---

## 🛑 Stopping the Application

1. In the backend terminal: Press `Ctrl+C`
2. In the frontend terminal: Press `Ctrl+C`, then type `Y` and press Enter

---

## 💡 Tips

1. **Keep both terminals open** while using the app
2. **Backend must run first** before starting frontend
3. **Check logs** in terminals if something doesn't work
4. **Use sample data** to test features quickly
5. **Get API keys** from OpenAI/Anthropic for full AI features

---

## 📞 Need Help?

Check these files for more information:

- `README.md` - Project overview
- `QUICKSTART.md` - Quick setup guide
- `PYTHON313_SETUP.md` - Python 3.13 specific setup
- `COMMAND_REFERENCE.md` - Command cheat sheet
- `TESTING.md` - Testing instructions

---

## ✅ Verification Checklist

Before running, make sure:

- [ ] Python 3.13 installed (`python --version`)
- [ ] Node.js installed (`node --version`)
- [ ] PostgreSQL running (`psql -U postgres -c "SELECT version();"`)
- [ ] Virtual environment activated (`venv\Scripts\activate`)
- [ ] All packages installed (`install-packages.bat` completed)
- [ ] `.env` file configured with your settings
- [ ] Database created (`financial_health` database exists)
- [ ] Migrations run (`alembic upgrade head` completed)
- [ ] Frontend dependencies installed (`npm install` in frontend)

---

**You're all set! 🎉 Enjoy building your Financial Health Assessment Tool!**
