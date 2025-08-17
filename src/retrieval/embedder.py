"""
Document Embedder

This module provides embedding functionality for scientific documents using
sentence transformers.
"""

import logging
from typing import List, Union
import numpy as np
from sentence_transformers import SentenceTransformer
import torch

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SentenceTransformerEmbedder:
    """Embedder using Sentence Transformers for scientific documents."""
    
    def __init__(self, model_name: str = "BAAI/bge-large-en-v1.5", device: str = None):
        """
        Initialize the embedder.
        
        Args:
            model_name: Name of the sentence transformer model to use
            device: Device to run the model on ('cpu', 'cuda', or None for auto)
        """
        self.model_name = model_name
        
        # Auto-detect device if not specified
        if device is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"
        
        self.device = device
        logger.info(f"Loading model {model_name} on device {device}")
        
        try:
            self.model = SentenceTransformer(model_name, device=device)
            logger.info(f"Model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise
    
    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Embed a list of text documents.
        
        Args:
            texts: List of text strings to embed
            
        Returns:
            List of embedding vectors
        """
        if not texts:
            return []
        
        try:
            # Encode texts to embeddings
            embeddings = self.model.encode(
                texts,
                convert_to_numpy=True,
                show_progress_bar=True,
                batch_size=32
            )
            
            # Convert to list of lists
            embeddings_list = embeddings.tolist()
            
            logger.info(f"Embedded {len(texts)} documents")
            return embeddings_list
            
        except Exception as e:
            logger.error(f"Error embedding documents: {str(e)}")
            raise
    
    def embed_single_document(self, text: str) -> List[float]:
        """
        Embed a single text document.
        
        Args:
            text: Text string to embed
            
        Returns:
            Embedding vector
        """
        embeddings = self.embed_documents([text])
        return embeddings[0] if embeddings else []
    
    def compute_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """
        Compute cosine similarity between two embeddings.
        
        Args:
            embedding1: First embedding vector
            embedding2: Second embedding vector
            
        Returns:
            Cosine similarity score
        """
        try:
            # Convert to numpy arrays
            vec1 = np.array(embedding1)
            vec2 = np.array(embedding2)
            
            # Compute cosine similarity
            similarity = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
            return float(similarity)
            
        except Exception as e:
            logger.error(f"Error computing similarity: {str(e)}")
            return 0.0
    
    def get_model_info(self) -> dict:
        """
        Get information about the loaded model.
        
        Returns:
            Dictionary with model information
        """
        return {
            "model_name": self.model_name,
            "device": self.device,
            "max_seq_length": self.model.max_seq_length,
            "embedding_dimension": self.model.get_sentence_embedding_dimension()
        }

def main():
    """Test the embedder with sample texts."""
    embedder = SentenceTransformerEmbedder()
    
    # Sample scientific texts
    sample_texts = [
        "Neural networks are computational models inspired by biological neural networks.",
        "The activation function determines the output of a neuron based on its input.",
        "Backpropagation is an algorithm for training artificial neural networks."
    ]
    
    # Embed the texts
    embeddings = embedder.embed_documents(sample_texts)
    
    print(f"Model Info: {embedder.get_model_info()}")
    print(f"Embedded {len(embeddings)} texts")
    print(f"Embedding dimension: {len(embeddings[0]) if embeddings else 0}")
    
    # Test similarity
    if len(embeddings) >= 2:
        similarity = embedder.compute_similarity(embeddings[0], embeddings[1])
        print(f"Similarity between first two texts: {similarity:.4f}")

if __name__ == "__main__":
    main()
