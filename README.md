# Financial Health Assessment Tool for SMEs

A comprehensive AI-powered platform for analyzing financial health of Small and Medium Enterprises (SMEs).

## Features

- 📊 Financial Statement Analysis (CSV/XLSX/PDF)
- 🤖 AI-Powered Insights using GPT-5/Claude
- 💰 Creditworthiness Evaluation
- ⚠️ Risk Assessment & Identification
- 📈 Financial Forecasting
- 💡 Cost Optimization Recommendations
- 🏦 Banking API Integration
- 📋 GST Integration Support
- 🌐 Multilingual Support (English, Hindi)
- 🔒 Enterprise-Grade Security

## Tech Stack

### Backend
- Python 3.11+
- FastAPI
- PostgreSQL
- pandas, numpy
- OpenAI GPT-5 / Claude AI
- SQLAlchemy ORM
- Cryptography for encryption

### Frontend
- React.js 18+
- TypeScript
- Tailwind CSS
- Recharts for visualizations
- Axios for API calls

## Project Structure

```
financial-health-assessment/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── services/
│   │   └── utils/
│   ├── requirements.txt
│   └── main.py
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   └── utils/
│   └── package.json
└── README.md
```

## Setup Instructions

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables (create `.env` file):
```
DATABASE_URL=postgresql://user:password@localhost:5432/financial_health
OPENAI_API_KEY=your_openai_api_key
ENCRYPTION_KEY=your_encryption_key
SECRET_KEY=your_secret_key
```

5. Run database migrations:
```bash
python -m alembic upgrade head
```

6. Start the server:
```bash
uvicorn main:app --reload
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

3. Create `.env` file:
```
REACT_APP_API_URL=http://localhost:8000
```

4. Start development server:
```bash
npm start
```

## API Documentation

Once the backend is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Security

- All financial data encrypted at rest using AES-256
- TLS/SSL for data in transit
- JWT-based authentication
- Role-based access control
- Audit logging for all operations

## License

Proprietary - HCL GUVI Career Carnival Hackathon Project

## Author

Built for Level 2 Hackathon Round
