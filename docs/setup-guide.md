# Setup Guide

## Prerequisites
- Node.js 18.x or higher
- Python 3.11 or higher
- Git
- (Optional) Docker & Docker Compose
- (Optional) Google Cloud CLI (`gcloud`)

## Local Development Setup

### 1. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```
Create `.env` file based on `.env.example`.
Run the server:
```bash
python app.py
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## Docker Setup
To run the entire stack using Docker Compose:
```bash
docker-compose up --build
```
The frontend will be available at `http://localhost:80` and the backend at `http://localhost:5000`.

## Troubleshooting
- **Backend fails to start**: Ensure SQLite is installed and `backend/data` directory is writable.
- **GCP Connection Errors**: If Live Mode fails, ensure `gcloud auth application-default login` has been run or service account keys are properly mapped in `.env`.
- **Ports already in use**: Change `FRONTEND_PORT` or `BACKEND_PORT` in `.env` and `docker-compose.yml`.
- **NPM Install failures**: Clear node_modules and verify Node.js version.
