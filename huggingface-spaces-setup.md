# 🌐 Hugging Face Spaces Deployment Guide

## Quick Setup for Scientific RAG System

### Step 1: Go to Hugging Face Spaces
1. Visit [https://huggingface.co/spaces](https://huggingface.co/spaces)
2. Click "Create new Space"

### Step 2: Configure Your Space
- **Owner**: Your Hugging Face username
- **Space name**: `scientific-rag-system`
- **License**: MIT
- **SDK**: **Streamlit** (Important!)
- **Visibility**: Public or Private

### Step 3: Connect Your GitHub Repository
1. Choose "Repository" tab
2. Select "Clone from repository"
3. Enter: `https://github.com/Rishabh2254/Scientific_RAG_System.git`
4. Click "Create Space"

### Step 4: Configure Environment Variables
1. Go to Space Settings
2. Add these environment variables:
   ```
   HUGGINGFACE_TOKEN=your_token_here
   DEVICE=cpu
   CHROMA_DB_PATH=./chroma_db
   ```

### Step 5: Deploy
- The space will automatically build and deploy
- Access your app at: `https://huggingface.co/spaces/YOUR_USERNAME/scientific-rag-system`

## Alternative: Manual Upload
If GitHub connection doesn't work:
1. Download your repository as ZIP
2. Upload files manually to the Space
3. Ensure `requirements.txt` is in the root directory

## Troubleshooting
- **Build fails**: Check that `requirements.txt` exists
- **Import errors**: Ensure all dependencies are listed
- **Model loading**: Verify Hugging Face token is set
