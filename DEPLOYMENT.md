# 🚀 Deployment Guide - Scientific RAG System

This guide provides step-by-step instructions for deploying the Scientific RAG System on various platforms.

## 📋 Prerequisites

- Python 3.8 or higher
- Git
- Internet connection for model downloads
- At least 4GB RAM (8GB recommended)
- 10GB+ free disk space

## 🏠 Local Deployment

### Quick Start (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/scientific-rag-system.git
cd scientific-rag-system

# 2. Run the deployment script
python deploy.py

# 3. Start the web application
streamlit run app/app.py
```

### Manual Setup

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/scientific-rag-system.git
cd scientific-rag-system

# 2. Create virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create necessary directories
mkdir -p data/raw_pdfs data/parsed_json data/chunks chroma_db logs

# 5. Set up environment variables
cp env_example.txt .env
# Edit .env file with your settings

# 6. Run tests
python test_complete_pipeline.py

# 7. Start the application
streamlit run app/app.py
```

## 🐳 Docker Deployment

### Using Docker Compose (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/scientific-rag-system.git
cd scientific-rag-system

# 2. Create .env file
cp env_example.txt .env

# 3. Build and run with Docker Compose
docker-compose up --build

# 4. Access the application at http://localhost:8501
```

### Using Docker directly

```bash
# 1. Build the Docker image
docker build -t scientific-rag .

# 2. Run the container
docker run -p 8501:8501 -v $(pwd)/data:/app/data -v $(pwd)/chroma_db:/app/chroma_db scientific-rag

# 3. Access the application at http://localhost:8501
```

## ☁️ Cloud Deployment

### Heroku

1. **Install Heroku CLI**
2. **Create Heroku app**:
   ```bash
   heroku create your-scientific-rag-app
   ```

3. **Add buildpacks**:
   ```bash
   heroku buildpacks:add heroku/python
   ```

4. **Deploy**:
   ```bash
   git push heroku main
   ```

5. **Open the app**:
   ```bash
   heroku open
   ```

### Google Cloud Run

1. **Install Google Cloud SDK**
2. **Build and deploy**:
   ```bash
   gcloud builds submit --tag gcr.io/YOUR_PROJECT/scientific-rag
   gcloud run deploy scientific-rag --image gcr.io/YOUR_PROJECT/scientific-rag --platform managed
   ```

### AWS ECS

1. **Create ECR repository**
2. **Build and push image**:
   ```bash
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com
   docker build -t scientific-rag .
   docker tag scientific-rag:latest YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/scientific-rag:latest
   docker push YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/scientific-rag:latest
   ```

3. **Create ECS service using the pushed image**

## 🌐 Hugging Face Spaces

1. **Go to [Hugging Face Spaces](https://huggingface.co/spaces)**
2. **Create new Space**:
   - Choose **Streamlit** as the SDK
   - Set visibility (Public/Private)
   - Clone your repository or upload files

3. **Configure Space**:
   - Add `requirements.txt` to the root
   - Set up environment variables in Space settings
   - Deploy automatically

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Hugging Face Token (Optional)
HUGGINGFACE_TOKEN=your_token_here

# Device Configuration
DEVICE=cpu  # or cuda

# ChromaDB Settings
CHROMA_DB_PATH=./chroma_db
CHROMA_COLLECTION_NAME=scientific_papers

# Logging
LOG_LEVEL=INFO
```

### Model Configuration

The system uses these models by default:
- **Embeddings**: `BAAI/bge-large-en-v1.5`
- **Generation**: `microsoft/DialoGPT-small`

To change models, edit the respective files:
- `src/retrieval/embedder.py` - Change embedding model
- `src/generation/llm.py` - Change generation model

## 🧪 Testing

### Run all tests
```bash
python test_complete_pipeline.py
```

### Run individual component tests
```bash
python test_chunker.py      # Test data processing
python test_retrieval.py    # Test retrieval engine
python test_generation.py   # Test generation system
```

### Test web application
```bash
streamlit run app/app.py
```

## 📊 Monitoring

### Health Check
The application includes a health check endpoint:
- **URL**: `http://your-domain:8501/_stcore/health`
- **Expected Response**: `{"status": "healthy"}`

### Logs
- **Application logs**: Check console output
- **Error logs**: Look for error messages in the terminal
- **ChromaDB logs**: Check `chroma_db/` directory

## 🔍 Troubleshooting

### Common Issues

1. **Model Download Fails**:
   - Check internet connection
   - Verify Hugging Face token (if using premium models)
   - Clear cache: `rm -rf ~/.cache/huggingface/`

2. **Memory Issues**:
   - Use smaller models
   - Increase system RAM
   - Use CPU instead of GPU

3. **Port Already in Use**:
   - Change port: `streamlit run app/app.py --server.port 8502`
   - Kill existing process: `lsof -ti:8501 | xargs kill -9`

4. **ChromaDB Errors**:
   - Clear database: `rm -rf chroma_db/`
   - Rebuild index: Run `python test_retrieval.py`

### Performance Optimization

1. **Use GPU** (if available):
   - Install CUDA
   - Set `DEVICE=cuda` in `.env`

2. **Increase Memory**:
   - Use larger RAM instance
   - Optimize batch sizes

3. **Caching**:
   - Models are cached automatically
   - ChromaDB provides persistent storage

## 🔒 Security

### Best Practices

1. **Environment Variables**: Never commit `.env` files
2. **API Keys**: Use secure key management
3. **Network Security**: Use HTTPS in production
4. **Access Control**: Implement authentication if needed

### Production Checklist

- [ ] HTTPS enabled
- [ ] Environment variables secured
- [ ] Logging configured
- [ ] Monitoring set up
- [ ] Backup strategy implemented
- [ ] Error handling tested

## 📞 Support

If you encounter issues:

1. **Check the logs** for error messages
2. **Review this documentation**
3. **Open an issue** on GitHub
4. **Check the troubleshooting section**

## 🎉 Success!

Once deployed, you can:

1. **Access the web interface** at your deployment URL
2. **Ask questions** about neural networks and biological systems
3. **Explore the source code** and documentation
4. **Contribute** to the project

**Happy exploring!** 🔬🚀
