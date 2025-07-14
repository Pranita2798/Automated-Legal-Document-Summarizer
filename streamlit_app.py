"""
Streamlit Web Application for Legal Document Summarizer

This application provides a web interface for legal document analysis including
text chunking, summarization, and keyword extraction.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
from collections import Counter
from typing import List, Dict, Any
import io
import base64

# Import our custom modules
from scripts.text_chunking import TextChunker
from scripts.summarization import LegalDocumentSummarizer
from scripts.keyword_extraction import LegalKeywordExtractor


def main():
    """Main Streamlit application."""
    st.set_page_config(
        page_title="Legal Document Summarizer",
        page_icon="⚖️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("⚖️ Legal Document Summarizer")
    st.markdown("AI-powered legal document analysis with text chunking, summarization, and keyword extraction")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("Configuration")
        
        # File upload
        uploaded_file = st.file_uploader(
            "Upload Legal Document",
            type=['txt'],
            help="Upload a plain text file containing your legal document"
        )
        
        # Analysis options
        st.subheader("Analysis Options")
        analysis_type = st.selectbox(
            "Select Analysis Type",
            ["Text Chunking", "Summarization", "Keyword Extraction", "Complete Analysis"]
        )
        
        # Configuration based on analysis type
        if analysis_type in ["Text Chunking", "Complete Analysis"]:
            st.subheader("Chunking Settings")
            chunk_method = st.selectbox("Chunking Method", ["words", "sentences", "paragraphs"])
            chunk_size = st.number_input("Chunk Size", min_value=1, max_value=1000, value=200)
            chunk_overlap = st.number_input("Overlap", min_value=0, max_value=chunk_size-1, value=20)
        
        if analysis_type in ["Summarization", "Complete Analysis"]:
            st.subheader("Summarization Settings")
            summary_type = st.selectbox("Summary Type", ["abstractive", "extractive"])
            summary_length = st.selectbox("Summary Length", ["short", "medium", "long"])
        
        if analysis_type in ["Keyword Extraction", "Complete Analysis"]:
            st.subheader("Keyword Settings")
            min_frequency = st.number_input("Minimum Frequency", min_value=1, max_value=10, value=2)
            max_keywords = st.number_input("Maximum Keywords", min_value=10, max_value=100, value=50)
    
    # Main content area
    if uploaded_file is not None:
        # Read the uploaded file
        text = uploaded_file.read().decode('utf-8')
        
        # Display document info
        st.subheader("Document Information")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Words", len(text.split()))
        with col2:
            st.metric("Characters", len(text))
        with col3:
            st.metric("Sentences", len(re.split(r'[.!?]+', text)))
        with col4:
            st.metric("Paragraphs", len(text.split('\n\n')))
        
        # Process based on analysis type
        if analysis_type == "Text Chunking":
            process_text_chunking(text, chunk_method, chunk_size, chunk_overlap)
        
        elif analysis_type == "Summarization":
            process_summarization(text, summary_type, summary_length)
        
        elif analysis_type == "Keyword Extraction":
            process_keyword_extraction(text, min_frequency, max_keywords)
        
        elif analysis_type == "Complete Analysis":
            process_complete_analysis(
                text, chunk_method, chunk_size, chunk_overlap,
                summary_type, summary_length, min_frequency, max_keywords
            )
    
    else:
        st.info("Please upload a legal document to begin analysis.")
        
        # Show sample document option
        if st.button("Try Sample Document"):
            sample_text = get_sample_legal_document()
            st.session_state.sample_text = sample_text
            st.experimental_rerun()


def process_text_chunking(text: str, method: str, size: int, overlap: int):
    """Process text chunking analysis."""
    st.subheader("Text Chunking Analysis")
    
    with st.spinner("Processing text chunks..."):
        chunker = TextChunker(chunk_size=size, overlap=overlap, method=method)
        chunks = chunker.process_document(text)
    
    # Display chunking results
    st.success(f"Generated {len(chunks)} chunks")
    
    # Visualization
    chunk_sizes = [chunk['word_count'] for chunk in chunks]
    fig = px.bar(
        x=range(1, len(chunks) + 1),
        y=chunk_sizes,
        title="Chunk Size Distribution",
        labels={'x': 'Chunk Number', 'y': 'Word Count'}
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Display chunks
    for i, chunk in enumerate(chunks):
        with st.expander(f"Chunk {chunk['id']} ({chunk['word_count']} words)"):
            st.text(chunk['content'])
    
    # Download option
    if st.button("Download Chunks"):
        download_chunks(chunks, "chunks.txt")


def process_summarization(text: str, summary_type: str, length: str):
    """Process summarization analysis."""
    st.subheader("Document Summarization")
    
    with st.spinner("Generating summary..."):
        summarizer = LegalDocumentSummarizer()
        summary_data = summarizer.generate_summary(text, summary_type, length)
    
    # Display summary
    st.success("Summary generated successfully!")
    
    # Metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Original Words", summary_data['original_words'])
    with col2:
        st.metric("Summary Words", summary_data['summary_words'])
    with col3:
        st.metric("Compression", f"{summary_data['compression_ratio']:.1f}%")
    
    # Summary text
    st.subheader("Generated Summary")
    st.text_area("Summary", summary_data['summary'], height=200)
    
    # Download option
    if st.button("Download Summary"):
        download_summary(summary_data, "summary.txt")


def process_keyword_extraction(text: str, min_freq: int, max_keywords: int):
    """Process keyword extraction analysis."""
    st.subheader("Keyword Extraction")
    
    with st.spinner("Extracting keywords..."):
        extractor = LegalKeywordExtractor()
        results = extractor.extract_all_keywords(text)
    
    # Display results
    st.success(f"Extracted {len(results['keywords'])} keywords and {len(results['key_phrases'])} phrases")
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Keywords", len(results['keywords']))
    with col2:
        st.metric("Key Phrases", len(results['key_phrases']))
    with col3:
        st.metric("Named Entities", len(results['named_entities']))
    with col4:
        st.metric("Categories", len(results['statistics']['category_distribution']))
    
    # Keyword visualization
    if results['keywords']:
        # Word cloud
        wordcloud_data = {kw['term']: kw['frequency'] for kw in results['keywords']}
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(wordcloud_data)
        
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        st.pyplot(fig)
        
        # Category distribution
        category_counts = results['statistics']['category_distribution']
        fig_pie = px.pie(
            values=list(category_counts.values()),
            names=list(category_counts.keys()),
            title="Keyword Category Distribution"
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # Display keywords
    st.subheader("Keywords")
    keywords_df = pd.DataFrame(results['keywords'])
    st.dataframe(keywords_df)
    
    # Display key phrases
    st.subheader("Key Phrases")
    for phrase in results['key_phrases']:
        st.write(f"• {phrase}")
    
    # Download option
    if st.button("Download Keywords"):
        download_keywords(results, "keywords.txt")


def process_complete_analysis(text: str, chunk_method: str, chunk_size: int, chunk_overlap: int,
                            summary_type: str, summary_length: str, min_freq: int, max_keywords: int):
    """Process complete analysis."""
    st.subheader("Complete Document Analysis")
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Text chunking
    status_text.text("Processing text chunks...")
    chunker = TextChunker(chunk_size=chunk_size, overlap=chunk_overlap, method=chunk_method)
    chunks = chunker.process_document(text)
    progress_bar.progress(25)
    
    # Summarization
    status_text.text("Generating summary...")
    summarizer = LegalDocumentSummarizer()
    summary_data = summarizer.generate_summary(text, summary_type, summary_length)
    progress_bar.progress(50)
    
    # Keyword extraction
    status_text.text("Extracting keywords...")
    extractor = LegalKeywordExtractor()
    keyword_results = extractor.extract_all_keywords(text)
    progress_bar.progress(75)
    
    # Complete
    status_text.text("Analysis complete!")
    progress_bar.progress(100)
    
    # Display results in tabs
    tab1, tab2, tab3 = st.tabs(["Summary", "Keywords", "Chunks"])
    
    with tab1:
        st.metric("Compression Ratio", f"{summary_data['compression_ratio']:.1f}%")
        st.text_area("Summary", summary_data['summary'], height=200)
    
    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Keywords", len(keyword_results['keywords']))
            keywords_df = pd.DataFrame(keyword_results['keywords'])
            st.dataframe(keywords_df)
        
        with col2:
            st.metric("Key Phrases", len(keyword_results['key_phrases']))
            for phrase in keyword_results['key_phrases'][:10]:  # Show first 10
                st.write(f"• {phrase}")
    
    with tab3:
        st.metric("Total Chunks", len(chunks))
        for chunk in chunks[:5]:  # Show first 5 chunks
            with st.expander(f"Chunk {chunk['id']} ({chunk['word_count']} words)"):
                st.text(chunk['content'][:300] + "..." if len(chunk['content']) > 300 else chunk['content'])


def get_sample_legal_document():
    """Return a sample legal document for testing."""
    return """
SAMPLE LEASE AGREEMENT

This Lease Agreement ("Agreement") is entered into on January 1, 2024, between ABC Properties LLC ("Landlord") and John Smith ("Tenant") for the rental of property located at 123 Main Street, Anytown, State 12345.

TERMS AND CONDITIONS:

1. TERM: This lease shall commence on January 1, 2024, and shall continue for a period of twelve (12) months, ending on December 31, 2024.

2. RENT: Tenant agrees to pay monthly rent of $1,200, due on the first day of each month. Late fees of $50 will be charged for payments received after the 5th day of the month.

3. SECURITY DEPOSIT: Tenant shall pay a security deposit of $1,200 upon signing this agreement. The deposit will be returned within 30 days of lease termination, less any damages.

4. UTILITIES: Tenant is responsible for all utilities including electricity, gas, water, and internet services.

5. MAINTENANCE: Landlord shall maintain the property in habitable condition. Tenant shall be responsible for minor repairs and maintenance.

6. TERMINATION: Either party may terminate this lease with 30 days written notice. Early termination by tenant may result in forfeiture of security deposit.

This agreement constitutes the entire agreement between the parties and may only be modified in writing signed by both parties.

Landlord: ABC Properties LLC
Tenant: John Smith
Date: January 1, 2024
"""


def download_chunks(chunks: List[Dict], filename: str):
    """Create download link for chunks."""
    content = "TEXT CHUNKS\n" + "="*50 + "\n\n"
    for chunk in chunks:
        content += f"CHUNK {chunk['id']}\n"
        content += f"Words: {chunk['word_count']}\n"
        content += f"Content: {chunk['content']}\n\n"
        content += "="*50 + "\n\n"
    
    st.download_button(
        label="Download Chunks",
        data=content,
        file_name=filename,
        mime="text/plain"
    )


def download_summary(summary_data: Dict, filename: str):
    """Create download link for summary."""
    content = f"DOCUMENT SUMMARY\n{'='*50}\n\n"
    content += f"Type: {summary_data['summary_type']}\n"
    content += f"Length: {summary_data['length']}\n"
    content += f"Compression: {summary_data['compression_ratio']:.1f}%\n\n"
    content += f"SUMMARY:\n{summary_data['summary']}\n"
    
    st.download_button(
        label="Download Summary",
        data=content,
        file_name=filename,
        mime="text/plain"
    )


def download_keywords(results: Dict, filename: str):
    """Create download link for keywords."""
    content = f"KEYWORD EXTRACTION RESULTS\n{'='*50}\n\n"
    content += f"KEYWORDS:\n"
    for kw in results['keywords']:
        content += f"{kw['term']} ({kw['frequency']}) - {kw['category']}\n"
    
    content += f"\nKEY PHRASES:\n"
    for phrase in results['key_phrases']:
        content += f"• {phrase}\n"
    
    st.download_button(
        label="Download Keywords",
        data=content,
        file_name=filename,
        mime="text/plain"
    )


if __name__ == "__main__":
    main()