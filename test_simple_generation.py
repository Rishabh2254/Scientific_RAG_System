#!/usr/bin/env python3
"""
Simple test for generation component
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from generation.llm import RAGGenerator

def main():
    print("Testing simple generation...")
    
    # Initialize generator with a smaller model
    generator = RAGGenerator(model_name="microsoft/DialoGPT-small")
    
    # Simple test context
    test_context = [
        {
            "text_content": "Neural networks are computational models inspired by biological neural networks.",
            "metadata": {
                "source_paper_id": "test_paper_1",
                "section_header": "Introduction",
                "content_type": "narrativetext"
            }
        }
    ]
    
    # Test query
    query = "What are neural networks?"
    
    print(f"Query: {query}")
    print("Generating answer...")
    
    try:
        answer = generator.generate_answer(query, test_context)
        print(f"Answer: {answer}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
