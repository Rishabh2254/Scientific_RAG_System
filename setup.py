#!/usr/bin/env python3
"""
Setup script for Scientific RAG System
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")

def install_dependencies():
    """Install required dependencies."""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        sys.exit(1)

def create_env_file():
    """Create .env file if it doesn't exist."""
    env_file = Path(".env")
    if env_file.exists():
        print("✅ .env file already exists")
        return
    
    print("🔧 Creating .env file...")
    env_content = """# Scientific RAG System Environment Variables

# Hugging Face Token (Required for accessing models)
# Get your token from: https://huggingface.co/settings/tokens
HUGGINGFACE_TOKEN=your_huggingface_token_here

# Optional: Set device for model inference
# DEVICE=cpu  # or cuda if you have GPU support

# Optional: ChromaDB settings
# CHROMA_PERSIST_DIRECTORY=./chroma_db
# CHROMA_COLLECTION_NAME=scientific_papers

# Optional: Logging level
# LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR
"""
    
    with open(env_file, "w") as f:
        f.write(env_content)
    
    print("✅ .env file created")
    print("⚠️  Please edit .env file and add your Hugging Face token")

def check_huggingface_token():
    """Check if Hugging Face token is set."""
    from dotenv import load_dotenv
    load_dotenv()
    
    token = os.getenv("HUGGINGFACE_TOKEN")
    if not token or token == "your_huggingface_token_here":
        print("⚠️  Hugging Face token not set")
        print("   Please edit .env file and add your token")
        print("   Get your token from: https://huggingface.co/settings/tokens")
        return False
    
    print("✅ Hugging Face token found")
    return True

def create_directories():
    """Create necessary directories."""
    directories = [
        "data/raw_pdfs",
        "data/parsed_json", 
        "data/chunks",
        "notebooks",
        "chroma_db"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print("✅ Directories created")

def main():
    """Main setup function."""
    print("🔬 Scientific RAG System Setup")
    print("=" * 40)
    
    # Check Python version
    check_python_version()
    
    # Create directories
    create_directories()
    
    # Install dependencies
    install_dependencies()
    
    # Create .env file
    create_env_file()
    
    # Check Hugging Face token
    token_ok = check_huggingface_token()
    
    print("\n" + "=" * 40)
    print("🎉 Setup completed!")
    
    if token_ok:
        print("\n🚀 You can now run the system:")
        print("   python src/main.py --max-papers 10")
        print("   streamlit run app/app.py")
    else:
        print("\n⚠️  Please set your Hugging Face token in .env file before running the system")
    
    print("\n📖 For more information, see README.md")

if __name__ == "__main__":
    main()
