"""
Scientific PDF Parser

This module parses scientific PDFs using the unstructured library and extracts
structured content including text, tables, and equations.
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
from unstructured.partition.pdf import partition_pdf
from unstructured.documents.elements import (
    Title, NarrativeText, ListItem, Table, 
    Image, FigureCaption, Text
)
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ScientificPDFParser:
    """Parser for scientific PDF documents."""
    
    def __init__(self, output_dir: str = "data/parsed_json"):
        """
        Initialize the parser.
        
        Args:
            output_dir: Directory to save parsed JSON files
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def parse_scientific_pdf(self, pdf_path: str) -> Dict[str, Any]:
        """
        Parse a scientific PDF and extract structured content.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Dictionary containing structured representation of the paper
        """
        pdf_path = Path(pdf_path)
        logger.info(f"Parsing PDF: {pdf_path.name}")

        try:
            # Parse PDF using unstructured library
            # Try fast strategy first, fallback to hi_res if needed
            try:
                elements = partition_pdf(
                    str(pdf_path),
                    strategy="fast",
                    include_metadata=True
                )
            except Exception as fast_error:
                logger.warning(f"Fast parsing failed for {pdf_path.name}, trying hi_res: {str(fast_error)}")
                try:
                    elements = partition_pdf(
                        str(pdf_path),
                        strategy="hi_res",
                        include_metadata=True
                    )
                except Exception as hi_res_error:
                    logger.error(f"Both fast and hi_res parsing failed for {pdf_path.name}: {str(hi_res_error)}")
                    # Try with basic strategy as last resort
                    elements = partition_pdf(
                        str(pdf_path),
                        strategy="auto",
                        include_metadata=True
                    )

            # Extract paper structure
            paper_data = self._extract_paper_structure(elements, pdf_path.stem)

            # Save to JSON
            output_file = self.output_dir / f"{pdf_path.stem}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(paper_data, f, indent=2, ensure_ascii=False)

            logger.info(f"Parsed paper saved to: {output_file}")
            return paper_data

        except Exception as e:
            logger.error(f"Error parsing {pdf_path}: {str(e)}")
            return {}
    
    def _extract_paper_structure(self, elements: List, paper_id: str) -> Dict[str, Any]:
        """
        Extract structured content from parsed elements.
        
        Args:
            elements: List of parsed elements from unstructured
            paper_id: ID of the paper
            
        Returns:
            Structured dictionary representation
        """
        paper_data = {
            "paper_id": paper_id,
            "title": "",
            "authors": [],
            "abstract": "",
            "sections": [],
            "equations": [],
            "tables": []
        }
        
        current_section = None
        current_section_content = []
        
        for element in elements:
            element_text = str(element).strip()
            
            # Skip empty elements
            if not element_text:
                continue
            
            # Extract title (usually first Title element)
            if isinstance(element, Title) and not paper_data["title"]:
                paper_data["title"] = element_text
                continue
            
            # Extract abstract (look for "Abstract" or "ABSTRACT" followed by text)
            if self._is_abstract(element_text):
                paper_data["abstract"] = element_text
                continue
            
            # Extract section headers (Title elements that might be section headers)
            if isinstance(element, Title) and self._is_section_header(element_text):
                # Save previous section if exists
                if current_section:
                    paper_data["sections"].append({
                        "header": current_section,
                        "content": current_section_content
                    })
                
                # Start new section
                current_section = element_text
                current_section_content = []
                continue
            
            # Handle narrative text and other content types
            if isinstance(element, (NarrativeText, ListItem, Text)):
                # Add content to current section or create a default section
                if not current_section:
                    current_section = "Introduction"
                    current_section_content = []
                
                content_item = {
                    "type": type(element).__name__,
                    "text": element_text
                }
                current_section_content.append(content_item)
                continue
            
            # Extract tables
            if isinstance(element, Table):
                table_data = {
                    "content": element_text,
                    "section": current_section or "Unknown"
                }
                paper_data["tables"].append(table_data)
                continue
            
            # Extract equations (placeholder for vision-to-LaTeX model)
            if self._might_be_equation(element_text):
                equation_data = {
                    "text": element_text,
                    "section": current_section or "Unknown",
                    "needs_vision_processing": True
                }
                paper_data["equations"].append(equation_data)
                continue
            
            # Handle any other element types
            if not current_section:
                current_section = "Introduction"
                current_section_content = []
            
            content_item = {
                "type": type(element).__name__,
                "text": element_text
            }
            current_section_content.append(content_item)
        
        # Add final section
        if current_section:
            paper_data["sections"].append({
                "header": current_section,
                "content": current_section_content
            })
        
        return paper_data
    
    def _serialize_metadata(self, metadata: Any) -> Dict[str, Any]:
        """
        Convert metadata to JSON-serializable format.
        
        Args:
            metadata: Metadata object from unstructured
            
        Returns:
            JSON-serializable dictionary
        """
        if not metadata:
            return {}
        
        try:
            # Try to convert to dict if it's an object
            if hasattr(metadata, '__dict__'):
                return {k: str(v) for k, v in metadata.__dict__.items()}
            elif isinstance(metadata, dict):
                return {k: str(v) for k, v in metadata.items()}
            else:
                return {"raw": str(metadata)}
        except Exception:
            return {"raw": str(metadata)}
    
    def _is_abstract(self, text: str) -> bool:
        """Check if text is an abstract."""
        abstract_patterns = [
            r"^abstract\s*$",
            r"^abstract\s*:",
            r"^abstract\s*\n",
            r"^abstract\s*[A-Z]"
        ]
        return any(re.match(pattern, text.lower()) for pattern in abstract_patterns)
    
    def _is_section_header(self, text: str) -> bool:
        """Check if text is a section header."""
        # Common section headers in scientific papers
        section_patterns = [
            r"^\d+\.\s*[A-Z]",
            r"^[A-Z][A-Z\s]+$",
            r"^introduction\s*$",
            r"^methods?\s*$",
            r"^results?\s*$",
            r"^discussion\s*$",
            r"^conclusion\s*$",
            r"^references?\s*$",
            r"^bibliography\s*$",
            r"^acknowledgments?\s*$",
            r"^appendix\s*$"
        ]
        return any(re.match(pattern, text.lower()) for pattern in section_patterns)
    
    def _might_be_equation(self, text: str) -> bool:
        """Check if text might contain an equation."""
        # Look for mathematical symbols and patterns
        math_patterns = [
            r"\\[a-zA-Z]+",  # LaTeX commands
            r"[∑∫∂∇∞±×÷√]",  # Mathematical symbols
            r"\\[{}()\[\]]",  # LaTeX brackets
            r"\\frac\{",      # Fractions
            r"\\sum_",        # Summation
            r"\\int_",        # Integration
            r"\\partial",     # Partial derivative
            r"\\nabla",       # Nabla
            r"\\infty",       # Infinity
            r"\\alpha|\\beta|\\gamma|\\delta|\\epsilon|\\theta|\\lambda|\\mu|\\pi|\\sigma|\\phi|\\psi|\\omega"  # Greek letters
        ]
        return any(re.search(pattern, text) for pattern in math_patterns)
    
    def parse_all_pdfs(self, pdf_dir: str = "data/raw_pdfs") -> List[Dict[str, Any]]:
        """
        Parse all PDFs in a directory.
        
        Args:
            pdf_dir: Directory containing PDF files
            
        Returns:
            List of parsed paper data
        """
        pdf_dir = Path(pdf_dir)
        pdf_files = list(pdf_dir.glob("*.pdf"))
        
        parsed_papers = []
        
        for pdf_file in pdf_files:
            try:
                paper_data = self.parse_scientific_pdf(str(pdf_file))
                if paper_data:
                    parsed_papers.append(paper_data)
            except Exception as e:
                logger.error(f"Error parsing {pdf_file}: {str(e)}")
                continue
        
        logger.info(f"Parsed {len(parsed_papers)} papers successfully")
        return parsed_papers

def main():
    """Main function to run the parser."""
    parser = ScientificPDFParser()
    
    # Parse all PDFs in the raw_pdfs directory
    parsed_papers = parser.parse_all_pdfs()
    
    print(f"\nParsing Summary:")
    print(f"- Papers parsed: {len(parsed_papers)}")
    print(f"- Output directory: {parser.output_dir}")
    print(f"- JSON files created: {len(list(parser.output_dir.glob('*.json')))}")

if __name__ == "__main__":
    main()
