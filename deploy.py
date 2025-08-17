#!/usr/bin/env python3
"""
Scientific RAG System Deployment Script

This script helps users deploy and set up the Scientific RAG System.
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible."""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python {version.major}.{version.minor} detected. Python 3.8+ is required.")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def create_directories():
    """Create necessary directories."""
    print("📁 Creating directories...")
    directories = [
        "data/raw_pdfs",
        "data/parsed_json", 
        "data/chunks",
        "chroma_db",
        "logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created {directory}")

def install_dependencies():
    """Install Python dependencies."""
    print("📦 Installing dependencies...")
    if not run_command("pip install -r requirements.txt", "Installing Python packages"):
        return False
    return True

def setup_environment():
    """Set up environment variables."""
    print("🔧 Setting up environment...")
    
    env_file = Path(".env")
    if not env_file.exists():
        print("📝 Creating .env file...")
        with open(env_file, "w") as f:
            f.write("""# Scientific RAG System Environment Variables

# Hugging Face Token (Optional - for premium models)
# Get your token from: https://huggingface.co/settings/tokens
HUGGINGFACE_TOKEN=your_huggingface_token_here

# Device configuration
DEVICE=cpu  # or cuda if you have GPU support

# ChromaDB settings
CHROMA_DB_PATH=./chroma_db
CHROMA_COLLECTION_NAME=scientific_papers

# Logging level
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR
""")
        print("✅ .env file created")
    else:
        print("✅ .env file already exists")

def run_tests():
    """Run system tests."""
    print("🧪 Running system tests...")
    if not run_command("python test_complete_pipeline.py", "Running complete pipeline test"):
        return False
    return True

def main():
    """Main deployment function."""
    print("🚀 Scientific RAG System Deployment")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Setup environment
    setup_environment()
    
    # Run tests
    if not run_tests():
        print("❌ System tests failed")
        sys.exit(1)
    
    print("\n🎉 Deployment completed successfully!")
    print("\n📋 Next steps:")
    print("1. Start the web application: streamlit run app/app.py")
    print("2. Open your browser to: http://localhost:8501")
    print("3. Try asking questions about neural networks!")
    
    print("\n📚 Documentation:")
    print("- README.md: Complete usage guide")
    print("- PROJECT_SUMMARY.md: Technical details")
    print("- app/app.py: Web application code")

if __name__ == "__main__":
    main()
