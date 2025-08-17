#!/usr/bin/env python3
"""
Test script to run the chunking process
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from data_processing.chunker import ScientificChunker

def main():
    print("Starting chunking process...")
    
    # Initialize chunker
    chunker = ScientificChunker()
    
    # Chunk all papers
    chunks = chunker.chunk_all_papers()
    
    print(f"Successfully created {len(chunks)} chunks")
    print(f"Chunks saved to: {chunker.output_dir}")
    
    # Show some sample chunks
    if chunks:
        print("\nSample chunks:")
        for i, chunk in enumerate(chunks[:3]):
            print(f"Chunk {i+1}:")
            print(f"  Content: {chunk['text_content'][:100]}...")
            print(f"  Metadata: {chunk['metadata']}")
            print()

if __name__ == "__main__":
    main()
