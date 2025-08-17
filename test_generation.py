#!/usr/bin/env python3
"""
Test script to test LLM generation with RAG integration
"""

import sys
from pathlib import Path
import json
import os

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from retrieval.vector_store import ChromaVectorStore
from retrieval.embedder import SentenceTransformerEmbedder
from generation.llm import RAGGenerator

def main():
    print("Starting RAG Generation Test...")
    
    # Check for Hugging Face token
    if not os.getenv('HUGGINGFACE_TOKEN'):
        print("Warning: HUGGINGFACE_TOKEN not set. Using a smaller model for testing.")
        print("Set your token in .env file for better performance.")
    
    # Initialize components
    print("Initializing components...")
    embedder = SentenceTransformerEmbedder()
    vector_store = ChromaVectorStore()
    
    # Initialize RAG generator
    print("Initializing RAG generator...")
    rag_generator = RAGGenerator()
    
    # Test queries
    test_queries = [
        "What are neural networks?",
        "How do neurons work in biological systems?",
        "What is the relationship between neural networks and biological neurons?"
    ]
    
    print("\n" + "="*60)
    print("TESTING RAG GENERATION")
    print("="*60)
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n--- Test Query {i} ---")
        print(f"Query: {query}")
        
        try:
            # Retrieve relevant context
            print("Retrieving relevant context...")
            context_chunks = vector_store.query(query, n_results=3, embedder=embedder)
            
            if not context_chunks:
                print("No relevant context found.")
                continue
            
            print(f"Found {len(context_chunks)} relevant chunks")
            
            # Generate answer
            print("Generating answer...")
            answer = rag_generator.generate_answer(query, context_chunks)
            
            print(f"\nAnswer: {answer}")
            
            # Show sources
            print("\nSources:")
            for j, chunk in enumerate(context_chunks, 1):
                print(f"  {j}. Paper: {chunk['metadata']['source_paper_id']}")
                print(f"     Section: {chunk['metadata']['section_header']}")
                print(f"     Type: {chunk['metadata']['content_type']}")
                print(f"     Relevance: {1 - chunk['distance']:.2f}")
            
        except Exception as e:
            print(f"Error processing query: {str(e)}")
        
        print("\n" + "-"*40)

if __name__ == "__main__":
    main()
