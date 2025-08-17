"""
Scientific RAG System - Main Pipeline

This script orchestrates the entire RAG pipeline from data acquisition
to system setup and testing.
"""

import logging
import argparse
from pathlib import Path
import sys

# Add current directory to path for imports
sys.path.append(str(Path(__file__).parent))

from data_processing.downloader import ArxivDownloader
from data_processing.parser import ScientificPDFParser
from data_processing.chunker import ScientificChunker
from retrieval.embedder import SentenceTransformerEmbedder
from retrieval.vector_store import ChromaVectorStore
from generation.llm import RAGGenerator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ScientificRAGPipeline:
    """Main pipeline for the Scientific RAG system."""
    
    def __init__(self):
        """Initialize the pipeline components."""
        self.downloader = ArxivDownloader()
        self.parser = ScientificPDFParser()
        self.chunker = ScientificChunker()
        self.embedder = SentenceTransformerEmbedder()
        self.vector_store = ChromaVectorStore()
        self.generator = RAGGenerator()
    
    def run_full_pipeline(self, category: str = "q-bio.NC", max_papers: int = 100):
        """
        Run the complete RAG pipeline.
        
        Args:
            category: arXiv category to download papers from
            max_papers: Maximum number of papers to process
        """
        logger.info("Starting Scientific RAG Pipeline")
        
        # Step 1: Download papers
        logger.info("Step 1: Downloading papers from arXiv")
        downloaded_count = self.downloader.download_papers(category=category, max_results=max_papers)
        
        if downloaded_count == 0:
            logger.warning("No papers downloaded. Exiting pipeline.")
            return False
        
        # Step 2: Parse PDFs
        logger.info("Step 2: Parsing PDFs")
        parsed_papers = self.parser.parse_all_pdfs()
        
        if not parsed_papers:
            logger.warning("No papers parsed. Exiting pipeline.")
            return False
        
        # Step 3: Chunk papers
        logger.info("Step 3: Chunking papers")
        all_chunks = self.chunker.chunk_all_papers()
        
        if not all_chunks:
            logger.warning("No chunks created. Exiting pipeline.")
            return False
        
        # Step 4: Build vector index
        logger.info("Step 4: Building vector index")
        success = self.vector_store.build_index(all_chunks, self.embedder)
        
        if not success:
            logger.error("Failed to build vector index. Exiting pipeline.")
            return False
        
        # Step 5: Test the system
        logger.info("Step 5: Testing the system")
        self.test_system()
        
        logger.info("Pipeline completed successfully!")
        return True
    
    def test_system(self):
        """Test the RAG system with sample queries."""
        test_queries = [
            "What are neural networks?",
            "How do activation functions work?",
            "What is computational neuroscience?"
        ]
        
        logger.info("Testing system with sample queries...")
        
        for query in test_queries:
            logger.info(f"Testing query: {query}")
            
            try:
                # Retrieve context
                context_chunks = self.vector_store.query(query, n_results=3)
                
                if context_chunks:
                    # Generate answer
                    answer = self.generator.generate_answer(query, context_chunks)
                    logger.info(f"Generated answer: {answer[:100]}...")
                else:
                    logger.warning("No context found for query")
                    
            except Exception as e:
                logger.error(f"Error testing query '{query}': {str(e)}")
    
    def get_system_stats(self):
        """Get statistics about the system."""
        stats = {}
        
        # Vector store stats
        collection_info = self.vector_store.get_collection_info()
        stats['vector_store'] = collection_info
        
        # Chunk stats
        chunks = self.vector_store.load_chunks_from_file()
        if chunks:
            chunk_stats = self.chunker.get_chunk_statistics(chunks)
            stats['chunks'] = chunk_stats
        
        # Model info
        stats['embedder'] = self.embedder.get_model_info()
        stats['generator'] = self.generator.get_model_info()
        
        return stats

def main():
    """Main function to run the pipeline."""
    parser = argparse.ArgumentParser(description="Scientific RAG Pipeline")
    parser.add_argument(
        "--category", 
        default="q-bio.NC", 
        help="arXiv category to download papers from"
    )
    parser.add_argument(
        "--max-papers", 
        type=int, 
        default=100, 
        help="Maximum number of papers to process"
    )
    parser.add_argument(
        "--test-only", 
        action="store_true", 
        help="Only test the system without downloading new papers"
    )
    parser.add_argument(
        "--stats", 
        action="store_true", 
        help="Show system statistics"
    )
    
    args = parser.parse_args()
    
    # Initialize pipeline
    pipeline = ScientificRAGPipeline()
    
    if args.stats:
        # Show system statistics
        stats = pipeline.get_system_stats()
        print("\n=== System Statistics ===")
        print(f"Vector Store: {stats.get('vector_store', {})}")
        print(f"Chunks: {stats.get('chunks', {})}")
        print(f"Embedder: {stats.get('embedder', {})}")
        print(f"Generator: {stats.get('generator', {})}")
        return
    
    if args.test_only:
        # Test existing system
        pipeline.test_system()
        return
    
    # Run full pipeline
    success = pipeline.run_full_pipeline(
        category=args.category,
        max_papers=args.max_papers
    )
    
    if success:
        print("\n✅ Pipeline completed successfully!")
        print("You can now run the Streamlit app with: streamlit run app/app.py")
    else:
        print("\n❌ Pipeline failed. Check the logs for details.")

if __name__ == "__main__":
    main()
