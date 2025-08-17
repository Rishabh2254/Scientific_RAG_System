# 🎨 Render Deployment Guide

## Deploy Scientific RAG System on Render

### Step 1: Sign Up for Render
1. Go to [https://render.com](https://render.com)
2. Sign up with GitHub account

### Step 2: Create New Web Service
1. Click "New +"
2. Select "Web Service"
3. Connect your GitHub repository: `Rishabh2254/Scientific_RAG_System`

### Step 3: Configure Service
- **Name**: `scientific-rag-system`
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `streamlit run app/app.py --server.port=$PORT --server.address=0.0.0.0`

### Step 4: Environment Variables
Add these in Render dashboard:
```
HUGGINGFACE_TOKEN=your_token_here
DEVICE=cpu
CHROMA_DB_PATH=./chroma_db
```

### Step 5: Deploy
- Render will build and deploy automatically
- Your app will be available at the provided URL

## Advantages of Render
- ✅ Free tier available
- ✅ Automatic deployments
- ✅ Custom domains
- ✅ SSL certificates
- ✅ Good Python support
