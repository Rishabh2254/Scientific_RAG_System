#!/usr/bin/env python3
"""
Scientific RAG Web Application

A Streamlit web application for querying scientific literature using RAG.
"""

import streamlit as st
import sys
from pathlib import Path
import json
import os

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from retrieval.vector_store import ChromaVectorStore
from retrieval.embedder import SentenceTransformerEmbedder
from generation.llm import RAGGenerator

# Page configuration
st.set_page_config(
    page_title="Scientific RAG System",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .source-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .metric-box {
        background-color: #e8f4fd;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_components():
    """Load and cache the RAG components."""
    try:
        with st.spinner("Loading models and vector store..."):
            embedder = SentenceTransformerEmbedder()
            vector_store = ChromaVectorStore()
            generator = RAGGenerator(model_name="microsoft/DialoGPT-small")
        return embedder, vector_store, generator
    except Exception as e:
        st.error(f"Error loading components: {str(e)}")
        return None, None, None

def main():
    """Main application function."""
    
    # Header
    st.markdown('<h1 class="main-header">🔬 Scientific RAG System</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Query Quantitative Biology Literature with AI-Powered Retrieval</p>', unsafe_allow_html=True)
    
    # Load components
    embedder, vector_store, generator = load_components()
    
    if embedder is None:
        st.error("Failed to load system components. Please check the logs.")
        return
    
    # Sidebar
    with st.sidebar:
        st.header("📊 System Information")
        
        # Get collection info
        try:
            info = vector_store.get_collection_info()
            st.metric("Papers Indexed", info.get('count', 0))
            st.metric("Embedding Dimension", info.get('dimension', 0))
        except:
            st.metric("Papers Indexed", "N/A")
        
        st.header("🔧 Settings")
        num_results = st.slider("Number of sources to retrieve", 1, 10, 3)
        
        st.header("💡 Example Queries")
        example_queries = [
            "What are neural networks?",
            "How do neurons work in biological systems?",
            "What is the relationship between neural networks and biological neurons?",
            "Explain the concept of neural plasticity",
            "What are the different types of neural activation functions?"
        ]
        
        for query in example_queries:
            if st.button(query, key=f"example_{query}"):
                st.session_state.query = query
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("🤔 Ask a Question")
        
        # Query input
        query = st.text_input(
            "Enter your question about quantitative biology:",
            value=st.session_state.get('query', ''),
            placeholder="e.g., What are neural networks and how do they work?"
        )
        
        if st.button("🔍 Search and Generate Answer", type="primary"):
            if query.strip():
                with st.spinner("Processing your question..."):
                    try:
                        # Retrieve relevant context
                        context_chunks = vector_store.query(
                            query, 
                            n_results=num_results, 
                            embedder=embedder
                        )
                        
                        if not context_chunks:
                            st.warning("No relevant documents found for your query.")
                            return
                        
                        # Generate answer
                        answer = generator.generate_answer(query, context_chunks)
                        
                        # Display results
                        st.header("📝 Generated Answer")
                        st.write(answer)
                        
                        # Display sources
                        st.header("📚 Sources")
                        for i, chunk in enumerate(context_chunks, 1):
                            with st.expander(f"Source {i}: {chunk['metadata']['source_paper_id']}"):
                                st.markdown(f"""
                                **Paper ID:** {chunk['metadata']['source_paper_id']}  
                                **Section:** {chunk['metadata']['section_header']}  
                                **Type:** {chunk['metadata']['content_type']}  
                                **Relevance:** {1 - chunk['distance']:.2f}
                                """)
                                st.markdown(f"**Content:** {chunk['text_content'][:500]}...")
                        
                    except Exception as e:
                        st.error(f"Error processing query: {str(e)}")
            else:
                st.warning("Please enter a question.")
    
    with col2:
        st.header("📈 Statistics")
        
        # Display some statistics
        try:
            info = vector_store.get_collection_info()
            st.metric("Total Documents", info.get('count', 0))
            st.metric("Vector Dimension", info.get('dimension', 0))
        except:
            st.metric("Total Documents", "N/A")
        
        st.header("🎯 Tips")
        st.markdown("""
        - Ask specific questions about neural networks, neurons, or biological systems
        - The system searches through scientific papers from arXiv's q-bio category
        - Results are ranked by relevance to your query
        - Each answer includes citations to source papers
        """)
        
        st.header("🔬 About")
        st.markdown("""
        This Scientific RAG system uses:
        - **Embeddings:** BGE-large-en-v1.5
        - **Vector Store:** ChromaDB
        - **Generation:** DialoGPT
        - **Data:** arXiv q-bio papers
        """)

if __name__ == "__main__":
    main()
