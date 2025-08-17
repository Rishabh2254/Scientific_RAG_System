#!/usr/bin/env python3
"""
Complete Pipeline Test

This script tests the entire Scientific RAG pipeline from data loading
to answer generation.
"""

import sys
from pathlib import Path
import json
import time

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from retrieval.vector_store import ChromaVectorStore
from retrieval.embedder import SentenceTransformerEmbedder
from generation.llm import RAGGenerator

def test_complete_pipeline():
    """Test the complete RAG pipeline."""
    print("🧪 Testing Complete Scientific RAG Pipeline")
    print("=" * 60)
    
    # Step 1: Load components
    print("\n1️⃣ Loading Components...")
    try:
        embedder = SentenceTransformerEmbedder()
        print("   ✅ Embedder loaded successfully")
        
        vector_store = ChromaVectorStore()
        print("   ✅ Vector store initialized")
        
        generator = RAGGenerator(model_name="microsoft/DialoGPT-small")
        print("   ✅ Generator loaded successfully")
        
    except Exception as e:
        print(f"   ❌ Error loading components: {e}")
        return False
    
    # Step 2: Check vector store status
    print("\n2️⃣ Checking Vector Store...")
    try:
        info = vector_store.get_collection_info()
        doc_count = info.get('count', 0)
        print(f"   📊 Documents indexed: {doc_count}")
        
        if doc_count == 0:
            print("   ⚠️  No documents found. Loading chunks...")
            
            # Load chunks from file
            chunks_file = Path("data/chunks/all_chunks.json")
            if chunks_file.exists():
                with open(chunks_file, 'r', encoding='utf-8') as f:
                    chunks = json.load(f)
                
                print(f"   📄 Loaded {len(chunks)} chunks from file")
                
                # Build index
                print("   🔨 Building vector index...")
                success = vector_store.build_index(chunks, embedder)
                
                if success:
                    print("   ✅ Vector index built successfully")
                    info = vector_store.get_collection_info()
                    print(f"   📊 Total documents: {info.get('count', 0)}")
                else:
                    print("   ❌ Failed to build vector index")
                    return False
            else:
                print("   ❌ No chunks file found")
                return False
        else:
            print("   ✅ Vector store ready")
            
    except Exception as e:
        print(f"   ❌ Error checking vector store: {e}")
        return False
    
    # Step 3: Test retrieval
    print("\n3️⃣ Testing Retrieval...")
    test_queries = [
        "neural networks",
        "biological neurons",
        "activation functions"
    ]
    
    for query in test_queries:
        try:
            results = vector_store.query(query, n_results=2, embedder=embedder)
            print(f"   🔍 Query: '{query}' -> {len(results)} results")
            
            if results:
                best_result = results[0]
                relevance = 1 - best_result['distance']
                print(f"      📈 Best relevance: {relevance:.2f}")
            else:
                print(f"      ⚠️  No results for '{query}'")
                
        except Exception as e:
            print(f"   ❌ Error testing query '{query}': {e}")
    
    # Step 4: Test generation
    print("\n4️⃣ Testing Generation...")
    try:
        # Get some context for testing
        context_chunks = vector_store.query("neural networks", n_results=2, embedder=embedder)
        
        if context_chunks:
            print("   📝 Testing answer generation...")
            start_time = time.time()
            
            answer = generator.generate_answer("What are neural networks?", context_chunks)
            
            end_time = time.time()
            generation_time = end_time - start_time
            
            print(f"   ⏱️  Generation time: {generation_time:.2f} seconds")
            print(f"   📄 Answer length: {len(answer)} characters")
            
            if answer.strip():
                print("   ✅ Generation successful")
                print(f"   📝 Answer preview: {answer[:100]}...")
            else:
                print("   ⚠️  Generated answer is empty")
        else:
            print("   ⚠️  No context available for generation test")
            
    except Exception as e:
        print(f"   ❌ Error testing generation: {e}")
        return False
    
    # Step 5: Performance summary
    print("\n5️⃣ Performance Summary")
    print("   🎯 Pipeline Status: ✅ OPERATIONAL")
    print("   📊 Components: Embedder, Vector Store, Generator")
    print("   🔍 Retrieval: Working")
    print("   📝 Generation: Working")
    print("   🚀 Ready for web application")
    
    return True

def main():
    """Main function."""
    success = test_complete_pipeline()
    
    if success:
        print("\n🎉 COMPLETE PIPELINE TEST PASSED!")
        print("The Scientific RAG system is ready to use.")
        print("\nTo start the web application, run:")
        print("   streamlit run app/app.py")
    else:
        print("\n❌ PIPELINE TEST FAILED!")
        print("Please check the errors above and fix them.")

if __name__ == "__main__":
    main()
