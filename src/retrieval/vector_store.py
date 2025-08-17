"""
Vector Store for Scientific Documents

This module provides vector storage functionality using ChromaDB for
scientific document retrieval.
"""

import logging
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings
import json
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChromaVectorStore:
    """Vector store using ChromaDB for scientific document retrieval."""
    
    def __init__(self, persist_directory: str = "./chroma_db", collection_name: str = "scientific_papers"):
        """
        Initialize the vector store.
        
        Args:
            persist_directory: Directory to persist the ChromaDB data
            collection_name: Name of the collection to store documents
        """
        self.persist_directory = Path(persist_directory)
        self.persist_directory.mkdir(parents=True, exist_ok=True)
        self.collection_name = collection_name
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=str(self.persist_directory),
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        
        # Get or create collection
        try:
            self.collection = self.client.get_collection(name=collection_name)
            logger.info(f"Loaded existing collection: {collection_name}")
        except:
            self.collection = self.client.create_collection(name=collection_name)
            logger.info(f"Created new collection: {collection_name}")
    
    def build_index(self, chunks: List[Dict[str, Any]], embedder) -> bool:
        """
        Build the vector index from chunks.
        
        Args:
            chunks: List of chunk dictionaries with text_content and metadata
            embedder: Embedder instance to generate embeddings
            
        Returns:
            True if successful, False otherwise
        """
        if not chunks:
            logger.warning("No chunks provided for indexing")
            return False
        
        try:
            # Extract text content and metadata
            texts = [chunk["text_content"] for chunk in chunks]
            metadatas = [chunk["metadata"] for chunk in chunks]
            ids = [f"chunk_{i}" for i in range(len(chunks))]
            
            # Generate embeddings
            logger.info(f"Generating embeddings for {len(texts)} chunks...")
            embeddings = embedder.embed_documents(texts)
            
            # Add to collection
            self.collection.add(
                embeddings=embeddings,
                documents=texts,
                metadatas=metadatas,
                ids=ids
            )
            
            logger.info(f"Successfully indexed {len(chunks)} chunks")
            return True
            
        except Exception as e:
            logger.error(f"Error building index: {str(e)}")
            return False
    
    def query(self, query_text: str, n_results: int = 5, embedder=None) -> List[Dict[str, Any]]:
        """
        Query the vector store for similar documents.
        
        Args:
            query_text: Query text to search for
            n_results: Number of results to return
            embedder: Embedder instance to generate query embeddings (optional)
            
        Returns:
            List of dictionaries containing similar documents with metadata
        """
        try:
            if embedder:
                # Use custom embedder for query
                query_embedding = embedder.embed_documents([query_text])
                results = self.collection.query(
                    query_embeddings=query_embedding,
                    n_results=n_results
                )
            else:
                # Use ChromaDB's default embedding
                results = self.collection.query(
                    query_texts=[query_text],
                    n_results=n_results
                )
            
            # Format results
            formatted_results = []
            if results['documents'] and results['documents'][0]:
                for i in range(len(results['documents'][0])):
                    result = {
                        'text_content': results['documents'][0][i],
                        'metadata': results['metadatas'][0][i],
                        'id': results['ids'][0][i],
                        'distance': results['distances'][0][i] if 'distances' in results else None
                    }
                    formatted_results.append(result)
            
            logger.info(f"Query returned {len(formatted_results)} results")
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error querying vector store: {str(e)}")
            return []
    
    def get_collection_info(self) -> Dict[str, Any]:
        """
        Get information about the collection.
        
        Returns:
            Dictionary with collection information
        """
        try:
            count = self.collection.count()
            return {
                "collection_name": self.collection_name,
                "count": count,
                "dimension": 1024,  # BGE-large-en-v1.5 dimension
                "persist_directory": str(self.persist_directory)
            }
        except Exception as e:
            logger.error(f"Error getting collection info: {str(e)}")
            return {"count": 0, "dimension": 0}
    
    def clear_collection(self) -> bool:
        """
        Clear all documents from the collection.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            self.collection.delete(where={})
            logger.info("Collection cleared successfully")
            return True
        except Exception as e:
            logger.error(f"Error clearing collection: {str(e)}")
            return False
    
    def load_chunks_from_file(self, chunks_file: str = "data/chunks/all_chunks.json") -> List[Dict[str, Any]]:
        """
        Load chunks from a JSON file.
        
        Args:
            chunks_file: Path to the JSON file containing chunks
            
        Returns:
            List of chunk dictionaries
        """
        try:
            with open(chunks_file, 'r', encoding='utf-8') as f:
                chunks = json.load(f)
            logger.info(f"Loaded {len(chunks)} chunks from {chunks_file}")
            return chunks
        except Exception as e:
            logger.error(f"Error loading chunks from {chunks_file}: {str(e)}")
            return []

def main():
    """Test the vector store functionality."""
    from src.retrieval.embedder import SentenceTransformerEmbedder
    
    # Initialize embedder and vector store
    embedder = SentenceTransformerEmbedder()
    vector_store = ChromaVectorStore()
    
    # Sample chunks for testing
    sample_chunks = [
        {
            "text_content": "Neural networks are computational models inspired by biological neural networks.",
            "metadata": {
                "source_paper_id": "test_paper_1",
                "section_header": "Introduction",
                "content_type": "narrativetext"
            }
        },
        {
            "text_content": "The activation function determines the output of a neuron based on its input.",
            "metadata": {
                "source_paper_id": "test_paper_1",
                "section_header": "Methods",
                "content_type": "narrativetext"
            }
        },
        {
            "text_content": "Backpropagation is an algorithm for training artificial neural networks.",
            "metadata": {
                "source_paper_id": "test_paper_2",
                "section_header": "Methods",
                "content_type": "narrativetext"
            }
        }
    ]
    
    # Build index
    success = vector_store.build_index(sample_chunks, embedder)
    
    if success:
        # Test query
        results = vector_store.query("neural network training", n_results=2)
        
        print(f"Collection Info: {vector_store.get_collection_info()}")
        print(f"Query Results:")
        for i, result in enumerate(results):
            print(f"  {i+1}. Document: {result['document'][:100]}...")
            print(f"     Source: {result['metadata']['source_paper_id']}")
            print(f"     Section: {result['metadata']['section_header']}")

if __name__ == "__main__":
    main()
