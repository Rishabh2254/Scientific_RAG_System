# 🚀 Streamlit Cloud Deployment Guide

## Complete Setup Guide for Scientific RAG System

This guide will walk you through deploying your Scientific RAG System on Streamlit Cloud step by step.

## 📋 Prerequisites

- ✅ GitHub repository: [https://github.com/Rishabh2254/Scientific_RAG_System](https://github.com/Rishabh2254/Scientific_RAG_System)
- ✅ Streamlit account (free)
- ✅ Hugging Face account (optional, for better models)

## 🎯 Step-by-Step Deployment

### Step 1: Create Streamlit Account

1. **Go to Streamlit Cloud**: Visit [https://share.streamlit.io](https://share.streamlit.io)
2. **Sign Up**: Click "Sign up" and create an account
3. **Connect GitHub**: Link your GitHub account when prompted

### Step 2: Deploy Your App

1. **Click "New app"** in Streamlit Cloud dashboard
2. **Fill in the deployment details**:
   - **Repository**: `Rishabh2254/Scientific_RAG_System`
   - **Branch**: `main`
   - **Main file path**: `app/app.py`
   - **App URL**: `scientific-rag-system` (or your preferred name)

3. **Click "Deploy!"**

### Step 3: Configure Environment Variables

1. **Go to your deployed app settings**
2. **Click "Secrets"** in the sidebar
3. **Add these secrets**:

```toml
[general]
HUGGINGFACE_TOKEN = "your_huggingface_token_here"
DEVICE = "cpu"
CHROMA_DB_PATH = "./chroma_db"
CHROMA_COLLECTION_NAME = "scientific_papers"
LOG_LEVEL = "INFO"
```

### Step 4: Wait for Deployment

- Streamlit will automatically:
  - Install dependencies from `requirements.txt`
  - Build your application
  - Deploy it to the cloud
- **Deployment time**: 2-5 minutes
- **Status**: Check the deployment logs for any errors

## 🔧 Configuration Files

### 1. Verify requirements.txt
Ensure your `requirements.txt` contains all dependencies:

```txt
streamlit>=1.29.0
sentence-transformers>=2.2.2
chromadb>=0.4.22
transformers>=4.36.2
torch>=2.6.0
arxiv>=2.1.0
unstructured[pdf]>=0.18.13
python-dotenv>=1.0.0
tqdm>=4.66.1
```

### 2. Check app/app.py
Ensure your Streamlit app is properly configured:

```python
# At the top of app/app.py
import streamlit as st
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure page
st.set_page_config(
    page_title="Scientific RAG System",
    page_icon="🔬",
    layout="wide"
)
```

## 🌐 Access Your Deployed App

Once deployed, your app will be available at:
```
https://scientific-rag-system-XXXXX.streamlit.app
```

Replace `XXXXX` with your actual deployment ID.

## 🔍 Troubleshooting

### Common Issues and Solutions

#### 1. **Build Fails**
**Error**: "Failed to install dependencies"
**Solution**:
- Check `requirements.txt` exists in root directory
- Verify all package names are correct
- Remove any version conflicts

#### 2. **Import Errors**
**Error**: "ModuleNotFoundError"
**Solution**:
- Ensure all imports are in `requirements.txt`
- Check file paths are correct
- Verify Python version compatibility

#### 3. **Model Loading Issues**
**Error**: "Model not found"
**Solution**:
- Set `HUGGINGFACE_TOKEN` in Streamlit secrets
- Use smaller models for faster loading
- Check internet connectivity

#### 4. **Memory Issues**
**Error**: "Out of memory"
**Solution**:
- Use smaller models (DialoGPT-small)
- Set `DEVICE=cpu` in secrets
- Optimize batch sizes

#### 5. **ChromaDB Errors**
**Error**: "Database connection failed"
**Solution**:
- Set `CHROMA_DB_PATH=./chroma_db` in secrets
- Ensure write permissions
- Clear database if corrupted

### Debugging Steps

1. **Check Deployment Logs**:
   - Go to your app in Streamlit Cloud
   - Click "Manage app" → "Deployment logs"
   - Look for error messages

2. **Test Locally First**:
   ```bash
   streamlit run app/app.py
   ```

3. **Verify Environment**:
   - Check all environment variables are set
   - Ensure secrets are properly formatted

## 📊 Monitoring Your App

### Health Check
Your app includes a health check endpoint:
```
https://your-app.streamlit.app/_stcore/health
```

### Performance Monitoring
- **Response Time**: Monitor query response times
- **Memory Usage**: Check resource utilization
- **Error Rates**: Track application errors

## 🔄 Updating Your App

### Automatic Updates
- Streamlit Cloud automatically redeploys when you push to GitHub
- Changes are reflected within 1-2 minutes

### Manual Redeploy
1. Go to your app in Streamlit Cloud
2. Click "Manage app" → "Redeploy"

## 🎯 Best Practices

### 1. **Optimize for Cloud**
- Use smaller models for faster loading
- Implement caching where possible
- Handle errors gracefully

### 2. **Security**
- Never commit API keys to GitHub
- Use Streamlit secrets for sensitive data
- Validate user inputs

### 3. **Performance**
- Cache expensive operations
- Use async operations where possible
- Optimize model loading

### 4. **User Experience**
- Add loading indicators
- Provide clear error messages
- Include helpful documentation

## 🚀 Advanced Configuration

### Custom Domain (Optional)
1. **Get a domain name**
2. **Configure DNS**:
   - Add CNAME record pointing to your Streamlit app
   - Wait for DNS propagation (24-48 hours)
3. **Contact Streamlit support** for custom domain setup

### Environment-Specific Settings
Create different configurations for development and production:

```python
# In your app
if st.secrets.get("ENVIRONMENT") == "production":
    # Production settings
    MODEL_NAME = "microsoft/DialoGPT-small"
else:
    # Development settings
    MODEL_NAME = "microsoft/DialoGPT-medium"
```

## 📞 Support

### Streamlit Cloud Support
- **Documentation**: [https://docs.streamlit.io/streamlit-community-cloud](https://docs.streamlit.io/streamlit-community-cloud)
- **Community**: [https://discuss.streamlit.io](https://discuss.streamlit.io)
- **GitHub Issues**: Report bugs in your repository

### Common Commands
```bash
# Test locally
streamlit run app/app.py

# Check requirements
pip install -r requirements.txt

# Run tests
python test_complete_pipeline.py
```

## 🎉 Success Checklist

- [ ] App deployed successfully
- [ ] All dependencies installed
- [ ] Environment variables configured
- [ ] Models loading correctly
- [ ] Queries working
- [ ] Error handling implemented
- [ ] Performance optimized

## 🌟 Your Deployed App Features

Once deployed, your Scientific RAG System will have:

- ✅ **Web Interface**: Modern Streamlit UI
- ✅ **Semantic Search**: Find relevant scientific papers
- ✅ **Answer Generation**: AI-powered responses with citations
- ✅ **Source Tracking**: Verifiable references
- ✅ **Real-time Updates**: Automatic redeployment
- ✅ **Scalability**: Cloud infrastructure
- ✅ **Security**: Environment variable protection

**Congratulations! Your Scientific RAG System is now live on Streamlit Cloud!** 🚀🔬

---

**Need Help?** Check the troubleshooting section above or open an issue in your GitHub repository.
