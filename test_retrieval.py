#!/usr/bin/env python3
"""
Test script to build vector index and test retrieval engine
"""

import sys
from pathlib import Path
import json

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from retrieval.vector_store import ChromaVectorStore
from retrieval.embedder import SentenceTransformerEmbedder

def main():
    print("Starting retrieval engine setup...")
    
    # Load chunks
    chunks_file = Path("data/chunks/all_chunks.json")
    if not chunks_file.exists():
        print("Error: Chunks file not found!")
        return
    
    with open(chunks_file, 'r', encoding='utf-8') as f:
        chunks = json.load(f)
    
    print(f"Loaded {len(chunks)} chunks")
    
    # Initialize embedder
    print("Initializing embedder...")
    embedder = SentenceTransformerEmbedder()
    
    # Initialize vector store
    print("Initializing vector store...")
    vector_store = ChromaVectorStore()
    
    # Build index
    print("Building vector index...")
    vector_store.build_index(chunks, embedder)
    
    # Test query
    print("\nTesting retrieval with sample query...")
    test_query = "neural networks"
    results = vector_store.query(test_query, n_results=3, embedder=embedder)
    
    print(f"Query: '{test_query}'")
    print(f"Found {len(results)} results:")
    
    for i, result in enumerate(results, 1):
        print(f"\nResult {i}:")
        print(f"  Content: {result['text_content'][:200]}...")
        print(f"  Source: {result['metadata']['source_paper_id']}")
        print(f"  Section: {result['metadata']['section_header']}")
        print(f"  Type: {result['metadata']['content_type']}")
        print(f"  Distance: {result['distance']:.4f}")
    
    # Show collection info
    print(f"\nCollection info:")
    info = vector_store.get_collection_info()
    print(f"  Total documents: {info['count']}")
    print(f"  Embedding dimension: {info['dimension']}")

if __name__ == "__main__":
    main()
