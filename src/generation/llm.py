"""
RAG Generator

This module provides the RAG (Retrieval-Augmented Generation) functionality
using open-source language models for scientific question answering.
"""

import logging
from typing import List, Dict, Any, Optional
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RAGGenerator:
    """RAG generator using open-source language models."""
    
    def __init__(self, model_name: str = "microsoft/DialoGPT-medium", device: str = None):
        """
        Initialize the RAG generator.
        
        Args:
            model_name: Name of the language model to use
            device: Device to run the model on ('cpu', 'cuda', or None for auto)
        """
        self.model_name = model_name
        
        # Auto-detect device if not specified
        if device is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"
        
        self.device = device
        logger.info(f"Loading model {model_name} on device {device}")
        
        try:
            # Load tokenizer and model
            self.tokenizer = AutoTokenizer.from_pretrained(
                model_name,
                trust_remote_code=True
            )
            
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                torch_dtype=torch.float16 if device == "cuda" else torch.float32,
                device_map="auto" if device == "cuda" else None,
                trust_remote_code=True
            )
            
            # Set pad token if not set
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            logger.info(f"Model loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise
    
    def generate_answer(self, query: str, context_chunks: List[Dict[str, Any]]) -> str:
        """
        Generate an answer based on the query and retrieved context.
        
        Args:
            query: User's question
            context_chunks: List of retrieved context chunks with metadata
            
        Returns:
            Generated answer with citations
        """
        try:
            # Construct the prompt
            prompt = self._construct_prompt(query, context_chunks)
            
            # Generate response
            response = self._generate_text(prompt)
            
            return response
            
        except Exception as e:
            logger.error(f"Error generating answer: {str(e)}")
            return f"Error generating answer: {str(e)}"
    
    def _construct_prompt(self, query: str, context_chunks: List[Dict[str, Any]]) -> str:
        """
        Construct a detailed prompt for the LLM.
        
        Args:
            query: User's question
            context_chunks: List of retrieved context chunks
            
        Returns:
            Formatted prompt string
        """
        # Format context
        context_text = ""
        for i, chunk in enumerate(context_chunks, 1):
            source_id = chunk['metadata']['source_paper_id']
            section = chunk['metadata']['section_header']
            content = chunk['text_content']
            
            context_text += f"Source {i} (Paper: {source_id}, Section: {section}):\n{content}\n\n"
        
        # Construct the prompt
        prompt = f"""You are an expert scientific researcher and educator. Your task is to answer questions about scientific literature based ONLY on the provided context. 

IMPORTANT INSTRUCTIONS:
1. Answer the question using ONLY the information provided in the context
2. If the context doesn't contain enough information to answer the question, say so clearly
3. Cite your sources using the format [Source X] where X is the source number
4. Be precise, accurate, and scientific in your response
5. If you mention specific findings, methods, or results, always cite the source
6. Use clear, academic language appropriate for scientific communication

CONTEXT:
{context_text}

QUESTION: {query}

ANSWER:"""
        
        return prompt
    
    def _generate_text(self, prompt: str, max_length: int = 2048) -> str:
        """
        Generate text using the language model.
        
        Args:
            prompt: Input prompt
            max_length: Maximum length of generated text
            
        Returns:
            Generated text
        """
        try:
            # Tokenize input
            inputs = self.tokenizer(
                prompt,
                return_tensors="pt",
                truncation=True,
                max_length=max_length
            )
            
            # Move to device
            if self.device == "cuda":
                inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Generate response
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=512,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id,
                    eos_token_id=self.tokenizer.eos_token_id
                )
            
            # Decode response
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract only the generated part (after the prompt)
            response = response[len(prompt):].strip()
            
            return response
            
        except Exception as e:
            logger.error(f"Error in text generation: {str(e)}")
            return f"Error generating response: {str(e)}"
    
    def get_model_info(self) -> dict:
        """
        Get information about the loaded model.
        
        Returns:
            Dictionary with model information
        """
        return {
            "model_name": self.model_name,
            "device": self.device,
            "vocab_size": self.tokenizer.vocab_size,
            "max_length": self.tokenizer.model_max_length
        }

def main():
    """Test the RAG generator with sample data."""
    # Check for Hugging Face token
    if not os.getenv("HUGGINGFACE_TOKEN"):
        print("Warning: HUGGINGFACE_TOKEN not found in environment variables.")
        print("Please set your Hugging Face token to access the model.")
        return
    
    generator = RAGGenerator()
    
    # Sample context chunks
    sample_context = [
        {
            "document": "Neural networks are computational models inspired by biological neural networks. They consist of interconnected nodes that process information.",
            "metadata": {
                "source_paper_id": "paper_001",
                "section_header": "Introduction",
                "content_type": "narrativetext"
            }
        },
        {
            "document": "The activation function determines the output of a neuron based on its input. Common activation functions include ReLU, sigmoid, and tanh.",
            "metadata": {
                "source_paper_id": "paper_001",
                "section_header": "Methods",
                "content_type": "narrativetext"
            }
        }
    ]
    
    # Test query
    query = "What are neural networks and how do activation functions work?"
    
    # Generate answer
    answer = generator.generate_answer(query, sample_context)
    
    print(f"Model Info: {generator.get_model_info()}")
    print(f"\nQuery: {query}")
    print(f"\nAnswer: {answer}")

if __name__ == "__main__":
    main()
