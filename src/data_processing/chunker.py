"""
Scientific Paper Chunker

This module implements structural element chunking for scientific papers,
creating meaningful chunks from parsed paper data.
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any
from tqdm import tqdm

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ScientificChunker:
    """Chunks scientific papers into meaningful segments."""
    
    def __init__(self, output_dir: str = "data/chunks"):
        """
        Initialize the chunker.
        
        Args:
            output_dir: Directory to save chunked data
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def chunk_parsed_paper(self, json_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Chunk a parsed paper into meaningful segments.
        
        Args:
            json_data: Structured paper data from parser
            
        Returns:
            List of chunks with text content and metadata
        """
        chunks = []
        paper_id = json_data.get("paper_id", "unknown")
        
        # Chunk 1: Abstract
        if json_data.get("abstract"):
            abstract_chunk = {
                "text_content": json_data["abstract"],
                "metadata": {
                    "source_paper_id": paper_id,
                    "section_header": "Abstract",
                    "content_type": "abstract",
                    "chunk_id": f"{paper_id}_abstract"
                }
            }
            chunks.append(abstract_chunk)
        
        # Chunk 2: Title
        if json_data.get("title"):
            title_chunk = {
                "text_content": json_data["title"],
                "metadata": {
                    "source_paper_id": paper_id,
                    "section_header": "Title",
                    "content_type": "title",
                    "chunk_id": f"{paper_id}_title"
                }
            }
            chunks.append(title_chunk)
        
        # Chunk 3: Section content
        for section_idx, section in enumerate(json_data.get("sections", [])):
            section_header = section.get("header", f"Section_{section_idx}")
            section_content = section.get("content", [])
            
            # Process each content element in the section
            for content_idx, content_item in enumerate(section_content):
                content_type = content_item.get("type", "Unknown")
                text = content_item.get("text", "")
                
                if not text.strip():
                    continue
                
                # Create chunk for this content element
                chunk = {
                    "text_content": text,
                    "metadata": {
                        "source_paper_id": paper_id,
                        "section_header": section_header,
                        "content_type": content_type.lower(),
                        "chunk_id": f"{paper_id}_{section_idx}_{content_idx}",
                        "original_metadata": content_item.get("metadata", {})
                    }
                }
                chunks.append(chunk)
        
        # Chunk 4: Tables
        for table_idx, table in enumerate(json_data.get("tables", [])):
            table_content = table.get("content", "")
            table_section = table.get("section", "Unknown")
            
            if table_content.strip():
                table_chunk = {
                    "text_content": table_content,
                    "metadata": {
                        "source_paper_id": paper_id,
                        "section_header": table_section,
                        "content_type": "table",
                        "chunk_id": f"{paper_id}_table_{table_idx}",
                        "table_metadata": table.get("metadata", {})
                    }
                }
                chunks.append(table_chunk)
        
        # Chunk 5: Equations
        for eq_idx, equation in enumerate(json_data.get("equations", [])):
            eq_text = equation.get("text", "")
            eq_section = equation.get("section", "Unknown")
            
            if eq_text.strip():
                equation_chunk = {
                    "text_content": eq_text,
                    "metadata": {
                        "source_paper_id": paper_id,
                        "section_header": eq_section,
                        "content_type": "equation",
                        "chunk_id": f"{paper_id}_equation_{eq_idx}",
                        "needs_vision_processing": equation.get("needs_vision_processing", False)
                    }
                }
                chunks.append(equation_chunk)
        
        logger.info(f"Created {len(chunks)} chunks for paper {paper_id}")
        return chunks
    
    def chunk_all_papers(self, json_dir: str = "data/parsed_json") -> List[Dict[str, Any]]:
        """
        Chunk all parsed papers in a directory.
        
        Args:
            json_dir: Directory containing parsed JSON files
            
        Returns:
            List of all chunks from all papers
        """
        json_dir = Path(json_dir)
        json_files = list(json_dir.glob("*.json"))
        
        all_chunks = []
        
        for json_file in tqdm(json_files, desc="Chunking papers"):
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    paper_data = json.load(f)
                
                chunks = self.chunk_parsed_paper(paper_data)
                all_chunks.extend(chunks)
                
            except Exception as e:
                logger.error(f"Error chunking {json_file}: {str(e)}")
                continue
        
        # Save all chunks to a single file
        output_file = self.output_dir / "all_chunks.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_chunks, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved {len(all_chunks)} total chunks to {output_file}")
        return all_chunks
    
    def get_chunk_statistics(self, chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Get statistics about the chunks.
        
        Args:
            chunks: List of chunks
            
        Returns:
            Dictionary with chunk statistics
        """
        if not chunks:
            return {}
        
        # Count by content type
        content_type_counts = {}
        section_counts = {}
        paper_counts = {}
        
        total_text_length = 0
        
        for chunk in chunks:
            content_type = chunk["metadata"]["content_type"]
            section = chunk["metadata"]["section_header"]
            paper_id = chunk["metadata"]["source_paper_id"]
            
            content_type_counts[content_type] = content_type_counts.get(content_type, 0) + 1
            section_counts[section] = section_counts.get(section, 0) + 1
            paper_counts[paper_id] = paper_counts.get(paper_id, 0) + 1
            
            total_text_length += len(chunk["text_content"])
        
        stats = {
            "total_chunks": len(chunks),
            "unique_papers": len(paper_counts),
            "content_type_distribution": content_type_counts,
            "section_distribution": section_counts,
            "average_chunk_length": total_text_length / len(chunks),
            "total_text_length": total_text_length
        }
        
        return stats

def main():
    """Main function to run the chunker."""
    chunker = ScientificChunker()
    
    # Chunk all parsed papers
    all_chunks = chunker.chunk_all_papers()
    
    # Get statistics
    stats = chunker.get_chunk_statistics(all_chunks)
    
    print(f"\nChunking Summary:")
    print(f"- Total chunks created: {stats.get('total_chunks', 0)}")
    print(f"- Unique papers processed: {stats.get('unique_papers', 0)}")
    print(f"- Average chunk length: {stats.get('average_chunk_length', 0):.1f} characters")
    print(f"- Output file: {chunker.output_dir}/all_chunks.json")
    
    print(f"\nContent Type Distribution:")
    for content_type, count in stats.get('content_type_distribution', {}).items():
        print(f"  - {content_type}: {count}")

if __name__ == "__main__":
    main()
