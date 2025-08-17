"""
Scientific Paper Downloader

This module downloads scientific papers from arXiv's q-bio.NC (Neurons and Cognition) 
category and saves them as PDF files.
"""

import arxiv
import os
from pathlib import Path
from tqdm import tqdm
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ArxivDownloader:
    """Downloads scientific papers from arXiv."""
    
    def __init__(self, output_dir: str = "data/raw_pdfs"):
        """
        Initialize the downloader.
        
        Args:
            output_dir: Directory to save downloaded PDFs
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def download_papers(self, category: str = "q-bio.NC", max_results: int = 100):
        """
        Download papers from arXiv.
        
        Args:
            category: arXiv category to search (default: q-bio.NC for Neurons and Cognition)
            max_results: Maximum number of papers to download
        """
        logger.info(f"Searching for papers in category: {category}")
        
        # Search for papers in the specified category
        search = arxiv.Search(
            query=f"cat:{category}",
            max_results=max_results,
            sort_by=arxiv.SortCriterion.SubmittedDate,
            sort_order=arxiv.SortOrder.Descending
        )
        
        downloaded_count = 0
        
        for result in tqdm(search.results(), total=max_results, desc="Downloading papers"):
            try:
                # Create filename from entry ID
                filename = f"{result.entry_id.split('/')[-1]}.pdf"
                filepath = self.output_dir / filename
                
                # Skip if file already exists
                if filepath.exists():
                    logger.info(f"File already exists: {filename}")
                    continue
                
                # Download the PDF
                result.download_pdf(filename=str(filepath))
                downloaded_count += 1
                logger.info(f"Downloaded: {filename}")
                
            except Exception as e:
                logger.error(f"Error downloading {result.entry_id}: {str(e)}")
                continue
        
        logger.info(f"Download completed. {downloaded_count} papers downloaded to {self.output_dir}")
        return downloaded_count

def main():
    """Main function to run the downloader."""
    downloader = ArxivDownloader()
    
    # Download 100 most recent papers from q-bio.NC
    count = downloader.download_papers(category="q-bio.NC", max_results=100)
    
    print(f"\nDownload Summary:")
    print(f"- Papers downloaded: {count}")
    print(f"- Output directory: {downloader.output_dir}")
    print(f"- Category: q-bio.NC (Neurons and Cognition)")

if __name__ == "__main__":
    main()
